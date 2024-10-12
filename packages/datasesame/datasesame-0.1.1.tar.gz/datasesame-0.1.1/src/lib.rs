use pyo3::prelude::*;
use dialoguer::{theme::ColorfulTheme, FuzzySelect};
use std::collections::HashMap;

mod data;
mod utils;

enum MenuItem {
    Command(&'static str, &'static str, fn() -> (String, HashMap<String, String>)), 
    SubMenu(&'static str, &'static str, Menu),       
}


struct Menu {
    items: Vec<MenuItem>,
}

impl Menu {
    fn new(items: Vec<MenuItem>) -> Self {
        Self { items }
    }

    fn display(&self) -> (String, HashMap<String, String>) {
        let item_labels: Vec<String> = self
            .items
            .iter()
            .map(|item| match item {
                MenuItem::SubMenu(label, description, _) => format!("{}: {}", label, description), // Show description
                MenuItem::Command(label, description, _) => format!("{}: {}", label, description),
            })
            .collect();

        let selection = FuzzySelect::with_theme(&ColorfulTheme::default())
            .items(&item_labels)
            .default(0)
            .interact()
            .unwrap();

        match &self.items[selection] {
            MenuItem::Command(_, _, action) => action(),
            MenuItem::SubMenu(_, _, submenu) => submenu.display(),
        }
    }

    fn execute(&self, args: &[String]) -> (String, HashMap<String, String>) {

        if args.is_empty() {
            return self.display();
        }

        for item in &self.items {
            match item {
                MenuItem::Command(label, _description, action) if *label == args[0] => {
                    if args.len() == 1 {
                        return action();
                    }
                }
                MenuItem::SubMenu(label, _description, submenu) if *label == args[0] => {
                    return submenu.execute(&args[1..]);
                }
                _ => {}
            }
        }

        // If no match is found, display the current menu
        println!("Invalid command: '{}'", args[0]);
        self.display()
    }
}

#[pyfunction]
fn cli_entry(args: Vec<String>) -> PyResult<(String, HashMap<String, String>)>{
    let result = if args.len() > 1 {
        main_menu().execute(&args[1..])
    } else {
        main_menu().display()
    };
    Ok(result)
}

fn main_menu() -> Menu {
    Menu::new(vec![
        MenuItem::SubMenu("data", "wrangle data", data_menu()),
    ])
}

fn data_menu() -> Menu {
    Menu::new(vec![
        MenuItem::Command("view", "view a dataset", view),
    ])
}

fn view() -> (String, HashMap<String, String>) {
    data::view()
}

#[pymodule]
fn ds(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cli_entry, m)?)?;
    Ok(())
}

