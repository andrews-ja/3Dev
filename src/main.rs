use glam::DVec3;
use itertools::Itertools;
use std::{fs, io, ops::Range};

fn main() -> io::Result<()> {
    let mut scene = HittableList { objects: vec![] };

    scene.add(Sphere {
        center: DVec3::new(0., -100.5, -1.),
        radius: 100.,
    });

    scene.add(Sphere {
        center: DVec3::new(0.0, 0.0, -1.0),
        radius: 0.5,
    });

    let camera = Camera::new(400, 16.0 / 9.0);
    camera.render_to_disk(scene)?;

    Ok(())
}

struct Camera {
    img_width: u32,
    img_height: u32,
    max_val: u8,
    aspect_ratio: f64,
    center: DVec3,
    pixel_delta_x: DVec3,
    pixel_delta_y: DVec3,
    pixel00_loc: DVec3,
}
impl Camera {
    fn new(img_width: u32, aspect_ratio: f64) -> Self {
        let max_val: u8 = 255;
        let img_height: u32 =
            (img_width as f64 / aspect_ratio) as u32;
        let viewport_height: f64 = 2.0;
        let viewport_width: f64 = viewport_height
            * (img_width as f64 / img_height as f64);
        let focal_length: f64 = 1.0;
        let center: DVec3 = DVec3::ZERO;

        // Calculate the vectors across the horizontal and down the vertical viewport edges.
        let viewport_x: DVec3 =
            DVec3::new(viewport_width, 0., 0.);
        let viewport_y: DVec3 =
            DVec3::new(0., -viewport_height, 0.);

        // Calculate the horizontal and vertical delta vectors from pixel to pixel.
        let pixel_delta_x: DVec3 =
            viewport_x / img_width as f64;
        let pixel_delta_y: DVec3 =
            viewport_y / img_height as f64;

        // Calculate the location of the upper left pixel.
        let viewport_xpper_left: DVec3 = center
            - DVec3::new(0., 0., focal_length)
            - viewport_x / 2.
            - viewport_y / 2.;
        let pixel00_loc: DVec3 = viewport_xpper_left
            + 0.5 * (pixel_delta_x + pixel_delta_y);

        Self {
            img_width,
            img_height,
            max_val,
            aspect_ratio,
            center,
            pixel_delta_x,
            pixel_delta_y,
            pixel00_loc,
        }
    }
    fn render_to_disk<T>(&self, scene: T) -> io::Result<()>
    where
        T: Hittable,
    {
        let pixels = (0..self.img_height)
            .cartesian_product(0..self.img_width)
            .map(|(y, x)| {
                let pixel_center = self.pixel00_loc
                    + (x as f64 * self.pixel_delta_x)
                    + (y as f64 * self.pixel_delta_y);
                let ray_direction =
                    pixel_center - self.center;
                let ray = Ray {
                    origin: self.center,
                    direction: ray_direction,
                };

                let pixel_colour = ray.colour(&scene) * 255.0;

                format!(
                    "{} {} {}",
                    pixel_colour.x,
                    pixel_colour.y,
                    pixel_colour.z
                )
            })
            .join("\n");
        fs::write(
            "output.ppm",
            format!(
                "P3
                {} {}
                {}
                {pixels}",
                self.img_width,
                self.img_height,
                self.max_val
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
    fn colour<T>(&self, scene: &T) -> DVec3
    where
        T: Hittable,
    {
        if let Some(rec) =
            scene.hit(&self, (0.)..f64::INFINITY)
        {
            return 0.5
                * (rec.normal + DVec3::new(1., 1., 1.));
        }

        let unit_direction: DVec3 =
            self.direction.normalize();
        let a = 0.5 * (unit_direction.y + 1.0);
        return (1.0 - a) * DVec3::new(1.0, 1.0, 1.0)
            + a * DVec3::new(0.5, 0.7, 1.0);
    }
}

trait Hittable {
    fn hit(
        &self,
        ray: &Ray,
        interval: Range<f64>,
    ) -> Option<HitRecord>;
}

struct HitRecord {
    point: DVec3,
    normal: DVec3,
    t: f64,
    front_face: bool,
}
impl HitRecord {
    fn with_face_normal(
        point: DVec3,
        out_normal: DVec3,
        t: f64,
        ray: &Ray,
    ) -> Self {
        let (front_face, normal) =
            HitRecord::calc_face_normal(
                ray,
                &out_normal,
            );
        HitRecord {
            point,
            normal,
            t,
            front_face,
        }
    }
    fn calc_face_normal(
        ray: &Ray,
        out_normal: &DVec3,
    ) -> (bool, DVec3) {
        let front_face =
            ray.direction.dot(*out_normal) < 0.;
        let normal = if front_face {
            *out_normal
        } else {
            -*out_normal
        };
        (front_face, normal)
    }
    fn set_face_normal(
        &mut self,
        ray: &Ray,
        out_normal: &DVec3,
    ) {
        let (front_face, normal) =
            HitRecord::calc_face_normal(
                ray,
                out_normal,
            );

        self.front_face = front_face;
        self.normal = normal;
    }
}

struct Sphere {
    center: DVec3,
    radius: f64,
}

impl Hittable for Sphere {
    fn hit(
        &self,
        ray: &Ray,
        interval: Range<f64>,
    ) -> Option<HitRecord> {
        let oc = ray.origin - self.center;
        let a = ray.direction.length_squared();
        let half_b = oc.dot(ray.direction);
        let c =
            oc.length_squared() - self.radius * self.radius;

        let discriminant = half_b * half_b - a * c;
        if discriminant < 0. {
            return None;
        }
        let sqrtd = discriminant.sqrt();

        // Find the nearest root that lies in the acceptable range.
        let mut root = (-half_b - sqrtd) / a;
        if !interval.contains(&root) {
            root = (-half_b + sqrtd) / a;
            if !interval.contains(&root) {
                return None;
            }
        }

        let t = root;
        let point = ray.at(t);
        let out_normal =
            (point - self.center) / self.radius;

        let rec = HitRecord::with_face_normal(
            point,
            out_normal,
            t,
            ray,
        );

        Some(rec)
    }
}

struct HittableList {
    objects: Vec<Box<dyn Hittable>>,
}
impl HittableList {
    fn clear(&mut self) {
        self.objects = vec![]
    }

    fn add<T>(&mut self, object: T)
    where
        T: Hittable + 'static,
    {
        self.objects.push(Box::new(object));
    }
}

impl Hittable for HittableList {
    fn hit(
        &self,
        ray: &Ray,
        interval: Range<f64>,
    ) -> Option<HitRecord> {
        let (_closest, hit_record) = self
            .objects
            .iter()
            .fold((interval.end, None), |acc, item| {
                if let Some(temp_rec) = item.hit(
                    ray,
                    interval.start..acc.0,
                ) {
                    (temp_rec.t, Some(temp_rec))
                } else {
                    acc
                }
            });

        hit_record
    }
}