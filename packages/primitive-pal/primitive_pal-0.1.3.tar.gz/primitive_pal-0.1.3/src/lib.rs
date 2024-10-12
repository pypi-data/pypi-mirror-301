use log::{info, warn};
use pyo3::prelude::*;
use std::{path::Path, time::Instant};

mod vcd;
use vcd::{process_data, process_header};

/// Reads VCD file
#[pyfunction]
fn process_vcd(path: String) -> PyResult<String> {
    info!("Reading VCD file at: {}", path);

    // Create path object
    let path = Path::new(&path);

    match process_header(path)? {
        Some(ptr) => {
            info!("Found the start of the data section at: {}", ptr);
            let now = Instant::now();
            {
                let _ = process_data(path, ptr);
            }
            let elapsed = now.elapsed();
            println!("Processed VCD in {:.2?}", elapsed);
        }
        None => warn!("VCD file did not dump any variables"),
    }

    Ok("success".to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn primitive_pal(m: &Bound<'_, PyModule>) -> PyResult<()> {
    pyo3_log::init();

    m.add_function(wrap_pyfunction!(process_vcd, m)?)?;
    Ok(())
}
