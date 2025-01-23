use itertools::Itertools;
use std::{fs, io};
use glam::DVec3;

// Constants
const IMG_WIDTH: u32 = 400;
const ASPECT_RATIO: f64 = 16.0 / 9.0;
const IMG_HEIGHT: u32 =
    (IMG_WIDTH as f64 / ASPECT_RATIO) as u32;
const MAX_VAL: u8 = 255;

const VIEWPRT_HEIGHT: f64 = 2.0;
const VIEWPRT_WIDTH: f64 = VIEWPRT_HEIGHT
    * (IMG_WIDTH as f64 / IMG_HEIGHT as f64);
const VIEWPORT_U: DVec3 =
    DVec3::new(VIEWPRT_WIDTH, 0., 0.);
const VIEWPORT_V: DVec3 =
    DVec3::new(0., -VIEWPRT_HEIGHT, 0.);

const FOCAL_LEN: f64 = 1.0;
const CAMERA_CENTER: DVec3 = DVec3::ZERO;

fn main() -> io::Result<()> {
    // Calculate the horizontal and vertical delta vectors from pixel to pixel.
    let pixel_delta_u: DVec3 =
        VIEWPORT_U / IMG_WIDTH as f64;
    let pixel_delta_v: DVec3 =
        VIEWPORT_V / IMG_HEIGHT as f64;

    // Calculate the location of the upper left pixel.
    let viewport_upper_left: DVec3 = CAMERA_CENTER
        - DVec3::new(0., 0., FOCAL_LEN)
        - VIEWPORT_U / 2.
        - VIEWPORT_V / 2.;
    let pixel00_loc: DVec3 = viewport_upper_left
        + 0.5 * (pixel_delta_u + pixel_delta_v);

    let pixels = (0..IMG_HEIGHT)
        .cartesian_product(0..IMG_WIDTH)
        .map(|(y, x)| {
            let pixel_center = pixel00_loc
                + (x as f64 * pixel_delta_u)
                + (y as f64 * pixel_delta_v);
            let ray_direction =
                pixel_center - CAMERA_CENTER;
            let ray = Ray {
                origin: CAMERA_CENTER,
                direction: ray_direction,
            };

            let pixel_colour = ray.colour() * 255.0;

            format!(
                "{} {} {}",
                pixel_colour.x, pixel_colour.y, pixel_colour.z
            )
        })
        .join("\n");
    fs::write(
        "output.ppm",
        format!(
            "P3 {} {} {} {}",
            IMG_WIDTH,
            IMG_HEIGHT,
            MAX_VAL,
            pixels,
        )
    )
}

struct Ray {
    origin: DVec3,
    direction: DVec3,
}

impl Ray {
    fn at(&self, t: f64) -> DVec3 {
        self.origin + t * self.direction
    }
    fn colour(&self) -> DVec3 {
        if hit_sphere(&DVec3::new(0., 0., -1.), 0.5, self) {
            return DVec3::new(1., 0., 0.);
        };

        let unit_direction: DVec3 =
            self.direction.normalize();
        let a = 0.5 * (unit_direction.y + 1.0);
        return (1.0 - a) * DVec3::new(1.0, 1.0, 1.0)
            + a * DVec3::new(0.5, 0.7, 1.0);
    }
}

fn hit_sphere(
    center: &DVec3,
    radius: f64,
    ray: &Ray,
) -> bool {
    let oc: DVec3 = ray.origin - *center;
    let a = ray.direction.dot(ray.direction);
    let b = 2.0 * oc.dot(ray.direction);
    let c = oc.dot(oc) - radius * radius;
    let discriminant = b * b - 4. * a * c;
    discriminant >= 0.
}