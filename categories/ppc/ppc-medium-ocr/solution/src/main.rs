use clap::Parser;
use image::{ImageReader, Rgb};
use serde::Serialize;
use reqwest::cookie::Jar;
use reqwest::{Client, Url};
use std::sync::Arc;
use std::time::Duration;

const SIZE: usize = 25;
const CELL: u32 = 50;
const RED: [u8; 3] = [255, 0, 0];
const BLUE: [u8; 3] = [0x1F, 0x78, 0xB4];
const BLACK: [u8; 3] = [0, 0, 0];

#[derive(Serialize)]
struct Solution { moves: Vec<String> }
#[derive(Parser)]
struct Cli { url: String }

#[inline(always)]
unsafe fn diff(a: *const u8, b: &[u8; 3]) -> u32 {
    ((*a.offset(0) as i32 - b[0] as i32).abs()
        + (*a.offset(1) as i32 - b[1] as i32).abs()
        + (*a.offset(2) as i32 - b[2] as i32).abs()) as u32
}

#[inline(always)]
unsafe fn is_red(a: *const u8) -> bool {
    diff(a, &RED) < 50
}
#[inline(always)]
unsafe fn is_blue(a: *const u8) -> bool {
    diff(a, &BLUE) < 100
}
#[inline(always)]
unsafe fn is_black(a: *const u8) -> bool {
    diff(a, &BLACK) < 70
}

#[inline(always)]
unsafe fn check_horizontal(buf: *const u8, width: u32, x0: u32, y: u32) -> bool {
    let mut red_count = 0;
    for dx in 0..CELL {
        let idx = ((y * width + (x0 + dx)) * 3) as isize;
        if is_red(buf.offset(idx)) { red_count += 1; }
    }
    red_count > 25
}
#[inline(always)]
unsafe fn check_vertical(buf: *const u8, width: u32, x: u32, y0: u32) -> bool {
    let mut red_count = 0;
    for dy in 0..CELL {
        let idx = (((y0 + dy) * width + x) * 3) as isize;
        if is_red(buf.offset(idx)) { red_count += 1; }
    }
    red_count > 25
}
#[inline(always)]
unsafe fn is_nearly_black(a: *const u8) -> bool {
    diff(a, &BLACK) < 80
}
#[inline(always)]
unsafe fn is_start_face_cell(buf: *const u8, width: u32, x: usize, y: usize) -> bool {
    let cx = x as u32 * CELL;
    let cy = y as u32 * CELL;
    let mut black_corners = 0;
    for &(ox, oy) in &[(0, 0), (CELL-5, 0), (0, CELL-5), (CELL-5, CELL-5)] {
        for dx in 0..5 {
            for dy in 0..5 {
                let idx = (((cy+oy+dy) * width + (cx+ox+dx)) * 3) as isize;
                if is_nearly_black(buf.offset(idx)) { black_corners += 1; }
            }
        }
    }
    black_corners >= 50
}
#[inline(always)]
unsafe fn find_start(buf: *const u8, width: u32) -> Option<(usize, usize)> {
    for y in 0..SIZE {
        for x in 0..SIZE {
            if is_start_face_cell(buf, width, x, y) { return Some((x, y)); }
        }
    }
    None
}
#[inline(always)]
unsafe fn is_nearly_blue(a: *const u8) -> bool {
    diff(a, &BLUE) < 100
}
#[inline(always)]
unsafe fn is_end_blue_cell(buf: *const u8, width: u32, x: usize, y: usize) -> bool {
    let cx = x as u32 * CELL;
    let cy = y as u32 * CELL;
    let mut blue_count = 0;
    for dx in 0..CELL {
        for dy in 0..CELL {
            let idx = (((cy + dy) * width + (cx + dx)) * 3) as isize;
            if is_nearly_blue(buf.offset(idx)) { blue_count += 1; }
        }
    }
    blue_count >= 20
}
#[inline(always)]
unsafe fn find_end(buf: *const u8, width: u32) -> Option<(usize, usize)> {
    for y in 0..SIZE {
        for x in 0..SIZE {
            if is_end_blue_cell(buf, width, x, y) { return Some((x, y)); }
        }
    }
    None
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Cli::parse();
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    for round in 1..=150 {
        let url = format!("{}/maze", args.url);
        let res = client.get(&url).send().await?;
        let bytes = res.bytes().await?;
        let img = image::load_from_memory(&bytes)?.to_rgb8();
        let (width, _height) = img.dimensions();
        let buf = img.as_raw().as_ptr();
        let mut grid = [[[false; 4]; SIZE]; SIZE];

        unsafe {
            for y in 0..SIZE {
                for x in 0..SIZE {
                    let cx = x as u32 * CELL;
                    let cy = y as u32 * CELL;
                    grid[y][x][0] = check_horizontal(buf, width, cx, cy); // up
                    grid[y][x][1] = if y + 1 < SIZE { check_horizontal(buf, width, cx, cy + CELL) } else { true }; // down
                    grid[y][x][2] = check_vertical(buf, width, cx, cy); // left
                    grid[y][x][3] = if x + 1 < SIZE { check_vertical(buf, width, cx + CELL, cy) } else { true }; // right
                }
            }
        }

        let (start, end) = unsafe {
            (find_start(buf, width).expect("Start not found!"), find_end(buf, width).expect("End not found!"))
        };

        let mut q = [(0usize, 0usize); SIZE*SIZE];
        let mut front = 0;
        let mut back = 0;
        let mut visited = [[false; SIZE]; SIZE];
        let mut prev = [[None; SIZE]; SIZE];
        q[back] = start; back += 1;
        visited[start.1][start.0] = true;
        let moves = [((0isize, -1isize), "w"), ((1, 0), "d"), ((0, 1), "s"), ((-1, 0), "a")];
        while front < back {
            let (x, y) = q[front]; front += 1;
            if (x, y) == end { break; }
            for (dir, dir_ch) in &moves {
                let nx = x as isize + dir.0;
                let ny = y as isize + dir.1;
                if nx < 0 || nx >= SIZE as isize || ny < 0 || ny >= SIZE as isize { continue; }
                let nx = nx as usize; let ny = ny as usize;
                let allowed = match *dir_ch {
                    "w" => !grid[y][x][0] && !grid[ny][nx][1],
                    "s" => !grid[y][x][1] && !grid[ny][nx][0],
                    "a" => !grid[y][x][2] && !grid[ny][nx][3],
                    "d" => !grid[y][x][3] && !grid[ny][nx][2],
                    _ => false,
                };
                if allowed && !visited[ny][nx] {
                    visited[ny][nx] = true;
                    prev[ny][nx] = Some((x, y, *dir_ch));
                    q[back] = (nx, ny); back += 1;
                }
            }
        }

        let mut path = Vec::with_capacity(SIZE*SIZE);
        let mut curr = end;
        while curr != start {
            if let Some((px, py, dir)) = prev[curr.1][curr.0] {
                path.push(dir);
                curr = (px, py);
            } else { panic!("No path found!"); }
        }
        path.reverse();
        let moves_vec: Vec<String> = path.into_iter().map(|d| d.to_string()).collect();

        let solve_url = format!("{}/solve", args.url);
        let resp = client.post(&solve_url)
            .json(&Solution { moves: moves_vec })
            .send().await?;
        let resp_text = resp.text().await?;
        println!("[{}] {}", round, resp_text);
    }
    Ok(())
}