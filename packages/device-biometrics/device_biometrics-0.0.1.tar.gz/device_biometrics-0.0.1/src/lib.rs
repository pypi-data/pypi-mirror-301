use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;

#[cfg(windows)]
mod bio_windows;
#[cfg(windows)]
use bio_windows as bio_provider;

#[pyfunction]
fn setup(name: &str) -> PyResult<bool> {
    match bio_provider::setup(name) {
        Ok(_) => Ok(true),  // Return `true` when setup succeeds
        Err(code) => {
            // Convert the error code into a Python runtime error
            Err(PyRuntimeError::new_err(format!("Setup failed with error code: {}", code)))
        }
    }
}

#[pyfunction]
fn authenticate(key_name: &str, data: &[u8]) -> PyResult<Vec<u8>> {
    match bio_provider::authenticate(key_name, data) {
        Ok(signed_data) => Ok(signed_data), // Return signed data
        Err(code) => {
            // Convert the error code into a Python runtime error
            Err(PyRuntimeError::new_err(format!("Authentication failed with error code: {}", code)))
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn biometric(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(setup, m)?)?;
    m.add_function(wrap_pyfunction!(authenticate, m)?)?;
    Ok(())
}
