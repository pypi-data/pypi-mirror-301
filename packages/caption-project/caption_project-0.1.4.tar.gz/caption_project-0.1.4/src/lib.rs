use pyo3::{exceptions::PyValueError, prelude::*};
mod caption;
mod token_output_stream;
mod utils;

/// Prints a message.
#[pyfunction]
fn hello() -> PyResult<String> {
    Ok("Hello from caption-project!".into())
}


/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn caption_image(image_path: &str) -> PyResult<String> {
    let res = caption::read_file(image_path);//.map_err(Err(PyValueError::new_err("")))
    match res {
        Ok(contents) => Ok(contents),
        Err(e) => Err(PyValueError::new_err(e.to_string())),
        
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(caption_image, m)?)?;
    
    Ok(())
}


