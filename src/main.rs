use glam::DVec3;
use itertools::Itertools;
use rand::Rng;
use std::{fs, io, ops::Range, sync::Arc};

trait Texture: Send + Sync {
    fn color(&self, u: f64, v: f64, p: DVec3) -> DVec3;
}

struct SolidColor {
    color: DVec3,
}

impl Texture for SolidColor {
    fn color(&self, _u: f64, _v: f64, _p: DVec3) -> DVec3 {
        self.color
    }
}

struct ImageTexture {
    image: image::RgbImage,
}

impl ImageTexture {
    fn new(path: &str) -> io::Result<Self> {
        let img = image::open(path)
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?
            .to_rgb8();
        Ok(Self { image: img })
    }
}

impl Texture for ImageTexture {
    fn color(&self, u: f64, v: f64, _p: DVec3) -> DVec3 {
        let u = u.clamp(0.0, 1.0);
        let v = 1.0 - v.clamp(0.0, 1.0); // Flip V

        let x = (u * (self.image.width() - 1) as f64) as u32;
        let y = (v * (self.image.height() - 1) as f64) as u32;

        let pixel = self.image.get_pixel(x, y);
        DVec3::new(
            pixel[0] as f64 / 255.0,
            pixel[1] as f64 / 255.0,
            pixel[2] as f64 / 255.0,
        )
    }
}

// Materials ------------------------------------------------------------------
trait Material {
    fn scatter(&self, ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)>;
}

struct Lambertian {
    albedo: Arc<dyn Texture>,
}

impl Material for Lambertian {
    fn scatter(&self, _: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)> {
        let mut scatter_dir = rec.normal + random_unit_vector();
        if scatter_dir.abs_diff_eq(DVec3::ZERO, 1e-8) {
            scatter_dir = rec.normal;
        }
        let attenuation = self.albedo.color(rec.u, rec.v, rec.point);
        Some((attenuation, Ray::new(rec.point, scatter_dir)))
    }
}

impl Lambertian {
    fn new(color: DVec3) -> Self {
        Self {
            albedo: Arc::new(SolidColor { color })
        }
    }

    fn from_texture(texture: Arc<dyn Texture>) -> Self {
        Self { albedo: texture }
    }
}

struct Metal {
    albedo: DVec3,
    fuzz: f64,
}

impl Metal {
    fn new(albedo: DVec3, fuzz: f64) -> Self {
        Metal { albedo, fuzz: fuzz.clamp(0.0, 1.0) }
    }
}

impl Material for Metal {
    fn scatter(&self, ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)> {
        let reflected = reflect(ray_in.direction.normalize(), rec.normal);
        let scattered = Ray::new(
            rec.point,
            reflected + self.fuzz * random_in_unit_sphere(),
        );
        (scattered.direction.dot(rec.normal) > 0.0).then_some((self.albedo, scattered))
    }
}

struct Dielectric {
    albedo: DVec3,
    refractive_index: f64,
}

// Utility functions ---------------------------------------------------------
fn schlick(cosine: f64, refraction_ratio: f64) -> f64 {
    let r0 = ((1.0 - refraction_ratio) / (1.0 + refraction_ratio)).powi(2);
    r0 + (1.0 - r0) * (1.0 - cosine).powi(5)
}

fn refract(uv: DVec3, n: DVec3, etai_over_etat: f64) -> DVec3 {
    let cos_theta = (-uv).dot(n).min(1.0);
    let r_out_perp = etai_over_etat * (uv + cos_theta * n);
    let r_out_parallel = -(1.0 - r_out_perp.length_squared()).abs().sqrt() * n;
    r_out_perp + r_out_parallel
}

impl Material for Dielectric {
    fn scatter(&self, ray_in: &Ray, rec: &HitRecord) -> Option<(DVec3, Ray)> {
        let refraction_ratio = if rec.front_face { 1.0 / self.refractive_index } else { self.refractive_index };
        let unit_dir = ray_in.direction.normalize();
        let cos_theta = (-unit_dir).dot(rec.normal).min(1.0);
        let sin_theta = (1.0 - cos_theta.powi(2)).sqrt();

        let cannot_refract = refraction_ratio * sin_theta > 1.0;
        let reflectance = schlick(cos_theta, refraction_ratio);
        let direction = if cannot_refract || reflectance > rand::rng().random() {
            reflect(unit_dir, rec.normal)
        } else {
            refract(unit_dir, rec.normal, refraction_ratio)
        };

        Some((self.albedo, Ray::new(rec.point, direction)))
    }
}

fn reflect(v: DVec3, n: DVec3) -> DVec3 {
    v - 2.0 * v.dot(n) * n
}

fn random_in_unit_sphere() -> DVec3 {
    let mut rng = rand::rng();
    loop {
        let p = DVec3::new(
            rng.random_range(-1.0..1.0),
            rng.random_range(-1.0..1.0),
            rng.random_range(-1.0..1.0),
        );
        if p.length_squared() < 1.0 {
            return p;
        }
    }
}

fn random_unit_vector() -> DVec3 {
    random_in_unit_sphere().normalize()
}

// Geometry -------------------------------------------------------------------
struct Ray {
    origin: DVec3,
    direction: DVec3,
}

impl Ray {
    fn new(origin: DVec3, direction: DVec3) -> Self {
        Self { origin, direction }
    }

    fn at(&self, t: f64) -> DVec3 {
        self.origin + t * self.direction
    }

    fn color<T: Hittable>(&self, depth: u32, world: &T) -> DVec3 {
        if depth == 0 {
            return DVec3::ZERO;
        }

        if let Some(rec) = world.hit(self, 0.001..f64::INFINITY) {
            return match rec.material.scatter(self, &rec) {
                Some((attenuation, scattered)) => attenuation * scattered.color(depth - 1, world),
                None => DVec3::ZERO,
            };
        }

        let t = 0.5 * (self.direction.normalize().y + 1.0);
        DVec3::ONE.lerp(DVec3::new(0.5, 0.7, 1.0), t)
    }
}

// Hit detection -------------------------------------------------------------
struct HitRecord {
    point: DVec3,
    normal: DVec3,
    t: f64,
    front_face: bool,
    material: Arc<dyn Material>,
    u: f64,
    v: f64,
}

impl HitRecord {
    fn new(ray: &Ray, point: DVec3, t: f64, outward_normal: DVec3, material: Arc<dyn Material>, u: f64, v: f64) -> Self {
        let front_face = ray.direction.dot(outward_normal) < 0.0;
        let normal = if front_face { outward_normal } else { -outward_normal };
        Self { point, normal, t, front_face, material, u, v }
    }
}

trait Hittable {
    fn hit(&self, ray: &Ray, interval: Range<f64>) -> Option<HitRecord>;
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
        let c = oc.length_squared() - self.radius.powi(2);
        let discriminant = half_b.powi(2) - a * c;

        if discriminant < 0.0 {
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

        let point = ray.at(root);
        let outward_normal = (point - self.center) / self.radius;

        // Calculate UV coordinates for texture mapping
        let dir = outward_normal;
        let phi = (-dir.z).atan2(dir.x) + std::f64::consts::PI;
        let theta = (-dir.y).acos();
        let u = phi / (2.0 * std::f64::consts::PI);
        let v = theta / std::f64::consts::PI;

        Some(HitRecord::new(
            ray,
            point,
            root,
            outward_normal,
            Arc::clone(&self.material),
            u,
            v,
        ))
    }
}

struct Quad {
    origin: DVec3,
    u_vec: DVec3,
    v_vec: DVec3,
    material: Arc<dyn Material>,
    normal: DVec3,
    d: f64,
    w: DVec3,
}

impl Quad {
    fn new(origin: DVec3, u_vec: DVec3, v_vec: DVec3, material: Arc<dyn Material>) -> Self {
        // Calculate the normal vector (pointing outward by right-hand rule)
        let normal = u_vec.cross(v_vec).normalize();
        let d = normal.dot(origin);
        let w = u_vec.cross(v_vec) / u_vec.cross(v_vec).dot(u_vec.cross(v_vec));
        
        Self {
            origin,
            u_vec,
            v_vec,
            material,
            normal,
            d,
            w,
        }
    }
}

impl Hittable for Quad {
    fn hit(&self, ray: &Ray, interval: Range<f64>) -> Option<HitRecord> {
        // Calculate intersection with the plane containing the quad
        let denom = self.normal.dot(ray.direction);
        
        // Ray is parallel to the plane
        if denom.abs() < 1e-8 {
            return None;
        }

        // Calculate the intersection distance
        let t = (self.d - self.normal.dot(ray.origin)) / denom;
        if !interval.contains(&t) {
            return None;
        }

        // Calculate the intersection point
        let intersection = ray.at(t);
        let planar_hitpt = intersection - self.origin;

        // Calculate barycentric coordinates
        let alpha = self.w.dot(planar_hitpt.cross(self.v_vec));
        let beta = self.w.dot(self.u_vec.cross(planar_hitpt));

        // Check if the point lies within the quad
        if alpha < 0.0 || alpha > 1.0 || beta < 0.0 || beta > 1.0 {
            return None;
        }

        let alpha = self.w.dot(planar_hitpt.cross(self.v_vec));
        let beta = self.w.dot(self.u_vec.cross(planar_hitpt));

        if alpha < 0.0 || alpha > 1.0 || beta < 0.0 || beta > 1.0 {
            return None;
        }

        Some(HitRecord::new(
            ray,
            intersection,
            t,
            self.normal,
            Arc::clone(&self.material),
            alpha,
            beta,
        ))

    }
}

fn create_cuboid(
    center: DVec3,
    dimensions: DVec3,
    material: Arc<dyn Material>,
    world: &mut HittableList,
) {
    // Calculate half-dimensions for easier positioning
    let half_width = dimensions.x / 2.0;
    let half_height = dimensions.y / 2.0;
    let half_depth = dimensions.z / 2.0;

    // Front face
    world.add(Quad::new(
        center + DVec3::new(-half_width, -half_height, half_depth),
        DVec3::new(0.0, dimensions.y, 0.0),
        DVec3::new(dimensions.x, 0.0, 0.0),
        Arc::clone(&material),
    ));

    // Back face
    world.add(Quad::new(
        center + DVec3::new(-half_width, -half_height, -half_depth),
        DVec3::new(0.0, dimensions.y, 0.0),
        DVec3::new(-dimensions.x, 0.0, 0.0),
        Arc::clone(&material),
    ));

    // Right face - ERROR 1: Incorrect starting position (using half_width instead of -half_width)
    world.add(Quad::new(
        center + DVec3::new(-half_width, -half_height, half_depth),
        DVec3::new(0.0, dimensions.y, 0.0),
        DVec3::new(0.0, 0.0, -dimensions.z),
        Arc::clone(&material),
    ));

    // Left face
    world.add(Quad::new(
        center + DVec3::new(-half_width, -half_height, -half_depth),
        DVec3::new(0.0, dimensions.y, 0.0),
        DVec3::new(0.0, 0.0, dimensions.z),
        Arc::clone(&material),
    ));

    // Top face - ERROR 2: Swapped vector parameters (u and v vectors mixed up)
    world.add(Quad::new(
        center + DVec3::new(-half_width, half_height, -half_depth),
        DVec3::new(0.0, 0.0, dimensions.z),
        DVec3::new(dimensions.x, 0.0, 0.0),
        Arc::clone(&material),
    ));

    // Bottom face
    world.add(Quad::new(
        center + DVec3::new(-half_width, -half_height, -half_depth),
        DVec3::new(dimensions.x, 0.0, 0.0),
        DVec3::new(0.0, 0.0, dimensions.z),
        material,
    ));
}

struct HittableList {
    objects: Vec<Box<dyn Hittable>>,
}

impl HittableList {
    fn add(&mut self, object: impl Hittable + 'static) {
        self.objects.push(Box::new(object));
    }
}

impl Hittable for HittableList {
    fn hit(&self, ray: &Ray, interval: Range<f64>) -> Option<HitRecord> {
        self.objects.iter()
            .filter_map(|obj| obj.hit(ray, interval.clone()))
            .min_by(|a, b| a.t.partial_cmp(&b.t).unwrap())
    }
}

// Camera ---------------------------------------------------------------------
struct Camera {
    image_width: u32,
    image_height: u32,
    samples_per_pixel: u32,
    max_depth: u32,
    position: DVec3,
    basis_u: DVec3,
    basis_v: DVec3,
    basis_w: DVec3,
    pixel_delta_u: DVec3,
    pixel_delta_v: DVec3,
    pixel00_loc: DVec3,
    defocus_radius: f64,
    focus_distance: f64,
}

impl Camera {
    fn new(
        image_width: u32,
        aspect_ratio: f64,
        samples_per_pixel: u32,
        max_depth: u32,
        position: DVec3,
        look_at: DVec3,
        up: DVec3,
        focus_distance: f64,
        aperture: f64,
    ) -> Self {
        let image_height = (image_width as f64 / aspect_ratio) as u32;
        let defocus_radius = aperture / 2.0;

        // Calculate camera basis vectors
        let w = (position - look_at).normalize();
        let u = up.cross(w).normalize();
        let v = w.cross(u);

        // Viewport dimensions
        let viewport_height = 2.0;
        let viewport_width = viewport_height * (image_width as f64 / image_height as f64);

        // Calculate pixel vectors
        let viewport_u = viewport_width * u;
        let viewport_v = viewport_height * -v;
        let pixel_delta_u = viewport_u / image_width as f64;
        let pixel_delta_v = viewport_v / image_height as f64;

        // Calculate viewport positions
        let viewport_upper_left = position - focus_distance * w - viewport_u/2.0 - viewport_v/2.0;
        let pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v);

        Self {
            image_width,
            image_height,
            samples_per_pixel,
            max_depth,
            position,
            basis_u: u,
            basis_v: v,
            basis_w: w,
            pixel_delta_u,
            pixel_delta_v,
            pixel00_loc,
            defocus_radius,
            focus_distance,
        }
    }

    fn render<T: Hittable>(&self, world: &T) -> io::Result<()> {
        let mut rng = rand::rng();
        let mut pixels = vec![DVec3::ZERO; (self.image_width * self.image_height) as usize];

        // Parallel pixel processing would go here
        for y in 0..self.image_height {
            for x in 0..self.image_width {
                let mut pixel_color = DVec3::ZERO;
                for _ in 0..self.samples_per_pixel {
                    let ray = self.get_ray(x, y, &mut rng);
                    pixel_color += ray.color(self.max_depth, world);
                }
                pixels[(y * self.image_width + x) as usize] = pixel_color;
            }
        }

        self.save_ppm(pixels)
    }

    fn get_ray<R: Rng>(&self, x: u32, y: u32, rng: &mut R) -> Ray {
        let pixel_center = self.pixel00_loc
            + x as f64 * self.pixel_delta_u
            + y as f64 * self.pixel_delta_v;
        
        let defocus = self.defocus_radius * random_in_unit_disk(rng);
        let ray_origin = self.position + self.basis_u * defocus.x + self.basis_v * defocus.y;
        let ray_direction = pixel_center - ray_origin;

        Ray::new(ray_origin, ray_direction)
    }

    fn save_ppm(&self, pixels: Vec<DVec3>) -> io::Result<()> {
        let scale = 1.0 / self.samples_per_pixel as f64;
        let mut output = format!(
            "P3\n{} {}\n255\n",
            self.image_width, self.image_height
        );

        for color in pixels {
            let scaled = color * scale;
            let rgb = DVec3::new(
                scaled.x.sqrt().clamp(0.0, 0.999),
                scaled.y.sqrt().clamp(0.0, 0.999),
                scaled.z.sqrt().clamp(0.0, 0.999),
            ) * 256.0;

            output += &format!(
                "{} {} {}\n",
                rgb.x as u8, rgb.y as u8, rgb.z as u8
            );
        }

        fs::write("output.ppm", output)
    }
}

fn random_in_unit_disk<R: Rng>(rng: &mut R) -> DVec3 {
    loop {
        let p = DVec3::new(rng.random_range(-1.0..1.0), rng.random_range(-1.0..1.0), 0.0);
        if p.length_squared() < 1.0 {
            return p;
        }
    }
}

// Main -----------------------------------------------------------------------
fn main() -> io::Result<()> {
    let mut world = HittableList { objects: vec![] };

    // --- Materials ---
    // Ground Material (Lambertian Solid Color)
    let ground_material = Arc::new(Lambertian::new(DVec3::new(0.5, 0.5, 0.5)));

    // Lambertian (Solid Color)
    let lambertian_red = Arc::new(Lambertian::new(DVec3::new(0.7, 0.1, 0.1)));

    // Lambertian (Image Texture) - Requires earth.jpg or similar
    let earth_texture = Arc::new(ImageTexture::new("earth.jpg")
        .expect("Failed to load earth.jpg. Make sure the file exists.")); // Using expect for simplicity here
    let earth_material = Arc::new(Lambertian::from_texture(earth_texture));

    // Metal (Smooth)
    let metal_smooth = Arc::new(Metal::new(DVec3::new(0.8, 0.8, 0.9), 0.0)); // Low fuzz

    // Metal (Fuzzy)
    let metal_fuzzy = Arc::new(Metal::new(DVec3::new(0.8, 0.6, 0.2), 0.6)); // High fuzz

    // Dielectric (Glass)
    let dielectric_glass = Arc::new(Dielectric {
        albedo: DVec3::ONE, // White/clear, albedo tints the refracted/reflected light
        refractive_index: 1.5,
    });
    let dielectric_glass_hollow = Arc::new(Dielectric {
        albedo: DVec3::ONE, // White/clear, albedo tints the refracted/reflected light
        refractive_index: -1.5,
    });



    // --- Scene Objects ---

    // Ground Plane (Large Sphere)
    world.add(Sphere {
        center: DVec3::new(0.0, -1000.0, 0.0), // Center it far below
        radius: 1000.0,
        material: ground_material,
    });

    // Central Sphere (Smooth Metal) - Will be in focus
    world.add(Sphere {
        center: DVec3::new(0.0, 1.0, 0.0),
        radius: 1.0,
        material: metal_smooth,
    });


    // Left Sphere (Dielectric/Glass)
    world.add(Sphere {
        center: DVec3::new(-4.0, 1.0, 0.0),
        radius: 1.0,
        material: dielectric_glass, // Use Arc::clone
    });
    // Inner sphere for hollow effect (Optional, demonstrates internal reflection better)
    world.add(Sphere {
        center: DVec3::new(-4.0, 1.0, 0.0),
        radius: -0.9, // Negative radius flips normals for hollow effect
        material: dielectric_glass_hollow,
    });


    // Right Sphere (Textured Lambertian)
    world.add(Sphere {
        center: DVec3::new(4.0, 1.0, 0.0),
        radius: 1.0,
        material: earth_material,
    });

    // Foreground Sphere (Fuzzy Metal) - Should appear slightly blurred due to DoF
    world.add(Sphere {
        center: DVec3::new(2.0, 0.5, 2.0),
        radius: 0.5,
        material: metal_fuzzy,
    });

    // Background Quad (Solid Lambertian) - Demonstrates Quad geometry
    world.add(Quad::new(
        DVec3::new(-2.0, 0.01, -3.0), // Origin corner
        DVec3::new(4.0, 0.0, 0.0),    // U vector (width)
        DVec3::new(0.0, 4.0, 0.0),    // V vector (height)
        lambertian_red,             // Material
    ));


    // Cuboid - Demonstrates create_cuboid (potentially with visual errors)
    let cuboid_mat = Arc::new(Lambertian::new(DVec3::new(0.1, 0.7, 0.1))); // Green
    create_cuboid(
        DVec3::new(-1.5, 0.75, 2.5), // Center position
        DVec3::new(1.5, 1.5, 1.5),   // Dimensions (width, height, depth)
        cuboid_mat,
        &mut world,
    );


    // --- Camera ---
    let aspect_ratio = 16.0 / 9.0;
    let image_width = 1000; // Use a smaller width (e.g., 400) for faster testing
    let samples_per_pixel = 100; // Lower (e.g., 10-50) for faster testing, higher (100-500+) for quality
    let max_depth = 50;        // Max ray bounces

    let look_from = DVec3::new(13.0, 2.0, 3.0); // Camera position
    let look_at = DVec3::new(0.0, 0.0, 0.0);    // Point camera looks at
    let up_vector = DVec3::new(0.0, 1.0, 0.0);  // Camera orientation

    let focus_dist = 10.0; // Distance to the plane in perfect focus (distance from look_from to look_at)
    let aperture = 0.1;   // Controls the size of the lens opening (larger aperture = more blur)

    let camera = Camera::new(
        image_width,
        aspect_ratio,
        samples_per_pixel,
        max_depth,
        look_from,
        look_at,
        up_vector,
        focus_dist,
        aperture,
    );

    // Render the scene
    camera.render(&world)
}