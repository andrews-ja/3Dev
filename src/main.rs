use glam::DVec3;
use itertools::Itertools;
use rand::prelude::*;
use std::{fs, io, ops::Range, sync::Arc};

fn main() -> io::Result<()> {
    let mut world = HittableList { objects: vec![] };

    // Materials
    let material_ground = Arc::new(Lambertian {
        albedo: DVec3::new(0.8, 0.8, 0.0), // Matte yellow ground
    });
    let material_matte_sphere = Arc::new(Lambertian {
        albedo: DVec3::new(0.7, 0.3, 0.3), // Matte red sphere
    });
    let material_hollow_glass = Arc::new(Dielectric {
        albedo: DVec3::new(1.0, 1.0, 1.0), // Clear glass
        index_of_refraction: 1.0 / 1.5, // Inverted IOR for hollow glass effect
    });

    // Ground sphere
    world.add(Sphere {
        center: DVec3::new(0.0, -100.5, -1.0),
        radius: 100.0,
        material: material_ground,
    });

    // Solid matte sphere behind
    world.add(Sphere {
        center: DVec3::new(-0.25, 0.0, -2.0),
        radius: 0.5,
        material: material_matte_sphere,
    });

    // Hollow glass sphere in front
    world.add(Sphere {
        center: DVec3::new(0.25, 0.0, -1.0),
        radius: 0.5,
        material: material_hollow_glass,
    });

    let camera = Camera::new(400, 16.0 / 9.0);
    camera.render_to_disk(world)?;
    Ok(())
}

trait Material {
    fn scatter(&self, ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)>;
}

struct Dielectric {
    albedo: DVec3,
    index_of_refraction: f64,
}

fn schlick(cosine: f64, refraction_ratio: f64) -> f64 {
    let r0 = ((1.0 - refraction_ratio) / (1.0 + refraction_ratio)).powi(2);
    r0 + (1.0 - r0) * (1.0 - cosine).powi(5)
}

fn refract(uv: DVec3, n: DVec3, etai_over_etat: f64) -> DVec3 {
    let cos_theta = (-uv).dot(n).min(1.0);
    let r_out_perp = etai_over_etat * (uv + cos_theta * n);
    let r_out_parallel = - (1.0 - r_out_perp.length_squared()).abs().sqrt() * n;
    r_out_perp + r_out_parallel
}

impl Material for Dielectric {
    fn scatter(&self, ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)> {
        let refraction_ratio = if rec.front_face {
            1.0 / self.index_of_refraction
        } else {
            self.index_of_refraction
        };

        let unit_direction = ray_in.direction.normalize();
        let cos_theta = (-unit_direction).dot(rec.normal).min(1.0);
        let sin_theta = (1.0 - cos_theta * cos_theta).sqrt();

        let cannot_refract = refraction_ratio * sin_theta > 1.0;
        let mut rng = rand::rng();
        let reflectance = schlick(cos_theta, refraction_ratio);

        let direction = if cannot_refract || reflectance > rng.random::<f64>() {
            // Reflect
            reflect(unit_direction, rec.normal)
        } else {
            // Refract
            refract(unit_direction, rec.normal, refraction_ratio)
        };

        Some((
            self.albedo,
            Ray {
                origin: rec.point,
                direction,
            },
        ))
    }
}

struct Lambertian {
    albedo: DVec3,
}

impl Material for Lambertian {
    fn scatter(&self, _ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)> {
        let mut scatter_direction = rec.normal + random_unit_vector();
        
        // Catch derandomerate scatter direction
        if scatter_direction.abs().length_squared() < 1e-8 {
            scatter_direction = rec.normal;
        }

        let scattered = Ray {
            origin: rec.point,
            direction: scatter_direction,
        };

        Some((self.albedo, scattered))
    }
}

struct Metal {
    albedo: DVec3,
    fuzz: f64,
}

impl Metal {
    fn new(albedo: DVec3, fuzz: f64) -> Self {
        Metal {
            albedo,
            fuzz: if fuzz < 1.0 { fuzz } else { 1.0 },
        }
    }
}

impl Material for Metal {
    fn scatter(&self, ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)> {
        let reflected = reflect(ray_in.direction.normalize(), rec.normal);
        let scattered = Ray {
            origin: rec.point,
            direction: reflected + self.fuzz * random_in_unit_sphere(),
        };

        if scattered.direction.dot(rec.normal) > 0.0 {
            Some((self.albedo, scattered))
        } else {
            None
        }
    }
}

struct Camera {
    image_width: u32,
    image_height: u32,
    max_value: u8,
    aspect_ratio: f64,
    center: DVec3,
    pixel_delta_u: DVec3,
    pixel_delta_v: DVec3,
    pixel00_loc: DVec3,
    samples_per_pixel: u32,
    max_depth: u32,
}

impl Camera {
    fn new(image_width: u32, aspect_ratio: f64) -> Self {
        let max_value: u8 = 255;
        let image_height: u32 = (image_width as f64 / aspect_ratio) as u32;
        let viewport_height: f64 = 2.0;
        let viewport_width: f64 = viewport_height * (image_width as f64 / image_height as f64);
        let focal_length: f64 = 1.0;
        let center: DVec3 = DVec3::ZERO;

        let viewport_u: DVec3 = DVec3::new(viewport_width, 0., 0.);
        let viewport_v: DVec3 = DVec3::new(0., -viewport_height, 0.);

        let pixel_delta_u: DVec3 = viewport_u / image_width as f64;
        let pixel_delta_v: DVec3 = viewport_v / image_height as f64;

        let viewport_upper_left: DVec3 = center
            - DVec3::new(0., 0., focal_length)
            - viewport_u / 2.
            - viewport_v / 2.;

        let pixel00_loc: DVec3 = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v);

        Self {
            image_width,
            image_height,
            max_value,
            aspect_ratio,
            center,
            pixel_delta_u,
            pixel_delta_v,
            pixel00_loc,
            samples_per_pixel: 100,
            max_depth: 50,
        }
    }

    fn get_ray(&self, i: i32, j: i32) -> Ray {
        let pixel_center = self.pixel00_loc
            + (i as f64 * self.pixel_delta_u)
            + (j as f64 * self.pixel_delta_v);
        let pixel_sample = pixel_center + self.pixel_sample_square();
        let ray_origin = self.center;
        let ray_direction = pixel_sample - ray_origin;
        Ray {
            origin: self.center,
            direction: ray_direction,
        }
    }

    fn pixel_sample_square(&self) -> DVec3 {
        let mut rng = rand::rng();
        let px = -0.5 + rng.random::<f64>();
        let py = -0.5 + rng.random::<f64>();
        (px * self.pixel_delta_u) + (py * self.pixel_delta_v)
    }

    fn render_to_disk<T>(&self, world: T) -> io::Result<()>
    where
        T: Hittable,
    {
        let pixels = (0..self.image_height)
            .cartesian_product(0..self.image_width)
            .map(|(y, x)| {
                let scale_factor = (self.samples_per_pixel as f64).recip();
                let pixel_color = (0..self.samples_per_pixel)
                    .into_iter()
                    .map(|_| {
                        self.get_ray(x as i32, y as i32)
                            .color(self.max_depth as i32, &world)
                    })
                    .sum::<DVec3>() * scale_factor;

                // Apply gamma correction (gamma 2)
                let r = (pixel_color.x.sqrt()).clamp(0.0, 0.999);
                let g = (pixel_color.y.sqrt()).clamp(0.0, 0.999);
                let b = (pixel_color.z.sqrt()).clamp(0.0, 0.999);

                format!(
                    "{} {} {}",
                    (r * 255.999) as i32,
                    (g * 255.999) as i32,
                    (b * 255.999) as i32
                )
            })
            .join("\n");

        fs::write(
            "output1.ppm",
            format!(
                "P3\n{} {}\n{}\n{}",
                self.image_width,
                self.image_height,
                self.max_value,
                pixels
            ),
        )
    }
}

struct Ray {
    origin: DVec3,
    direction: DVec3,
}

impl Ray {
    fn at(&self, t: f64) -> DVec3 {
        self.origin + t * self.direction
    }

    fn color<T>(&self, depth: i32, world: &T) -> DVec3
    where
        T: Hittable,
    {
        if depth <= 0 {
            return DVec3::ZERO;
        }

        if let Some(rec) = world.hit(self, 0.001..f64::INFINITY) {
            if let Some((attenuation, scattered)) = rec.material.scatter(self, &rec) {
                return attenuation * scattered.color(depth - 1, world);
            }
            return DVec3::ZERO;
        }

        let unit_direction = self.direction.normalize();
        let a = 0.5 * (unit_direction.y + 1.0);
        (1.0 - a) * DVec3::ONE + a * DVec3::new(0.5, 0.7, 1.0)
    }
}

trait Hittable {
    fn hit(&self, ray: &Ray, interval: Range<f64>) -> Option<HitRecord>;
}

struct HitRecord {
    point: DVec3,
    normal: DVec3,
    material: Arc<dyn Material>,
    t: f64,
    front_face: bool,
}

impl HitRecord {
    fn with_face_normal(
        point: DVec3,
        outward_normal: DVec3,
        t: f64,
        material: Arc<dyn Material>,
        ray: &Ray,
    ) -> Self {
        let (front_face, normal) = HitRecord::calc_face_normal(ray, &outward_normal);
        HitRecord {
            point,
            normal,
            material,
            t,
            front_face,
        }
    }

    fn calc_face_normal(ray: &Ray, outward_normal: &DVec3) -> (bool, DVec3) {
        let front_face = ray.direction.dot(*outward_normal) < 0.;
        let normal = if front_face {
            *outward_normal
        } else {
            -*outward_normal
        };
        (front_face, normal)
    }
}

struct Sphere {
    center: DVec3,
    radius: f64,
    material: Arc<dyn Material>,
}

impl Hittable for Sphere {
    fn hit(&self, ray: &Ray, interval: Range<f64>) -> Option<HitRecord> {
        let oc = ray.origin - self.center;
        let a = ray.direction.length_squared();
        let half_b = oc.dot(ray.direction);
        let c = oc.length_squared() - self.radius * self.radius;
        let discriminant = half_b * half_b - a * c;

        if discriminant < 0. {
            return None;
        }

        let sqrtd = discriminant.sqrt();
        let mut root = (-half_b - sqrtd) / a;
        if !interval.contains(&root) {
            root = (-half_b + sqrtd) / a;
            if !interval.contains(&root) {
                return None;
            }
        }

        let t = root;
        let point = ray.at(t);
        let outward_normal = (point - self.center) / self.radius;
        let rec = HitRecord::with_face_normal(
            point,
            outward_normal,
            t,
            Arc::clone(&self.material),
            ray,
        );
        Some(rec)
    }
}

struct HittableList {
    objects: Vec<Box<dyn Hittable>>,
}

impl HittableList {
    fn add<T>(&mut self, object: T)
    where
        T: Hittable + 'static,
    {
        self.objects.push(Box::new(object));
    }
}

impl Hittable for HittableList {
    fn hit(&self, ray: &Ray, interval: Range<f64>) -> Option<HitRecord> {
        let (_closest, hit_record) = self
            .objects
            .iter()
            .fold((interval.end, None), |acc, item| {
                if let Some(temp_rec) = item.hit(ray, interval.start..acc.0) {
                    (temp_rec.t, Some(temp_rec))
                } else {
                    acc
                }
            });
        hit_record
    }
}

fn random_in_unit_sphere() -> DVec3 {
    let mut rng = rand::rng();
    loop {
        let vec = DVec3::new(
            rng.random_range(-1.0..1.0),
            rng.random_range(-1.0..1.0),
            rng.random_range(-1.0..1.0),
        );
        if vec.length_squared() < 1. {
            break vec;
        }
    }
}

fn random_unit_vector() -> DVec3 {
    random_in_unit_sphere().normalize()
}

fn reflect(v: DVec3, n: DVec3) -> DVec3 {
    v - 2.0 * v.dot(n) * n
}
