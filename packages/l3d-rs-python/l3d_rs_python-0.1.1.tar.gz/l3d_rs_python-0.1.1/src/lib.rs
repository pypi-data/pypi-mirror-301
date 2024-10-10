use pyo3::prelude::*;
use l3d_rs::l3d::Luminaire;

#[pyfunction]
fn l3d_to_xml(path: &str) -> PyResult<String> {
    let loaded: Luminaire = Luminaire::load_l3d(path).unwrap();
    Ok(loaded.to_xml().unwrap())
}

#[pyfunction]
fn l3d_to_json(path: &str) -> PyResult<String> {
    let loaded: Luminaire = Luminaire::load_l3d(path).unwrap();
    Ok(loaded.to_json().unwrap())
}

#[pyfunction]
fn json_from_xml_str(xml_str: &str) -> PyResult<String> {
    let loaded: Luminaire = Luminaire::from_xml(&xml_str.to_string()).unwrap();
    Ok(loaded.to_json().unwrap())
}

#[pyfunction]
fn xml_from_json(json_str: &str) -> PyResult<String> {
    let loaded: Luminaire = Luminaire::from_json(json_str).unwrap();
    Ok(loaded.to_xml().unwrap())
}

#[pymodule]
fn l3d_rs_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(l3d_to_xml, m)?)?;
    m.add_function(wrap_pyfunction!(l3d_to_json, m)?)?;
    m.add_function(wrap_pyfunction!(xml_from_json, m)?)?;
    m.add_function(wrap_pyfunction!(json_from_xml_str, m)?)?;
    Ok(())
}