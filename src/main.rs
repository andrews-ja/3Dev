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
const VIEWPORT_X: DVec3 =
    DVec3::new(VIEWPRT_WIDTH, 0., 0.);
const VIEWPORT_Y: DVec3 =
    DVec3::new(0., -VIEWPRT_HEIGHT, 0.);

const FOCAL_LEN: f64 = 1.0;
const CAMERA_CENTER: DVec3 = DVec3::ZERO;

fn main() -> io::Result<()> {
    // Calculate the horizontal and vertical delta vectors from pixel to pixel.
    let pixel_delta_x: DVec3 =
        VIEWPORT_X / IMG_WIDTH as f64;
    let pixel_delta_y: DVec3 =
        VIEWPORT_Y / IMG_HEIGHT as f64;

    // Calculate the location of the upper left pixel.
    let viewport_top_left: DVec3 = CAMERA_CENTER
        - DVec3::new(0., 0., FOCAL_LEN)
        - VIEWPORT_X / 2.
        - VIEWPORT_Y / 2.;
    let viewoprt_origin: DVec3 = viewport_top_left
        + 0.5 * (pixel_delta_x + pixel_delta_y);

    let pixels = (0..IMG_HEIGHT)
        .cartesian_product(0..IMG_WIDTH)
        .map(|(y, x)| {
            let pixel_center = viewoprt_origin
                + (x as f64 * pixel_delta_x)
                + (y as f64 * pixel_delta_y);
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
    fn point_from_dist(&self, t: f64) -> DVec3 {
        self.origin + t * self.direction
    }
    fn colour(&self) -> DVec3 {
        let t =
            sphere_intersect(&DVec3::new(0., 0., -1.), 0.5, self);
        if t > 0.0 {
            let n_vec = (self.point_from_dist(t) - DVec3::new(0., 0., -1.))
                .normalize();
            return 0.5 * (n_vec + 1.0);
        };

        let unit_direction: DVec3 =
            self.direction.normalize();
        let a = 0.5 * (unit_direction.y + 1.0);
        return (1.0 - a) * DVec3::new(1.0, 1.0, 1.0)
            + a * DVec3::new(0.5, 0.7, 1.0);
    }
}

fn sphere_intersect(
    center: &DVec3,
    radius: f64,
    ray: &Ray,
) -> f64 {
    let oc: DVec3 = ray.origin - *center;
    let a = ray.direction.length_squared();
    let half_b = oc.dot(ray.direction);
    let c = oc.length_squared() - radius * radius;
    let discriminant = half_b * half_b - a * c;

    if discriminant < 0. {
        -1.0
    } else {
        (-half_b - discriminant.sqrt()) / a
    }
}