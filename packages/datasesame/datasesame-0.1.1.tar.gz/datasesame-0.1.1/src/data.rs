use std::collections::HashMap;
use dialoguer::{theme::ColorfulTheme, FuzzySelect};
use super::utils;

const VALID_FILE_EXTENSIONS: [&str; 6] = ["csv", "xlsx", "xls", "json", "ndjson", "parquet"];

pub fn view() -> (String, HashMap<String, String>) {
    let files = utils::find_files_with_extensions(&VALID_FILE_EXTENSIONS);

    if files.is_empty() {
        println!("No suitable files found.");
        std::process::exit(1);
    }

    let selection = FuzzySelect::with_theme(&ColorfulTheme::default())
        .with_prompt("Select a file to view")
        .items(&files)
        .default(0)
        .interact()
        .unwrap();

    let mut py_args = HashMap::new();
    py_args.insert(String::from("file"), files[selection].to_string());
    (String::from("data_view"), py_args)
}