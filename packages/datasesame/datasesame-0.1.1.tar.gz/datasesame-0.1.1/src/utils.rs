use std::fs;

pub fn find_files_with_extensions(extensions: &[&str]) -> Vec<String> {
    let mut result_files = Vec::new();
    for entry in fs::read_dir(".").unwrap() {
        let entry = entry.unwrap();
        let path = entry.path();
        if path.is_file() {
            if let Some(ext) = path.extension() {
                if let Some(ext_str) = ext.to_str() {
                    if extensions.contains(&ext_str) {
                        if let Some(file_name) = path.file_name() {
                            if let Some(file_name_str) = file_name.to_str() {
                                result_files.push(file_name_str.to_string());
                            }
                        }
                    }
                }
            }
        }
    }

    result_files
}
