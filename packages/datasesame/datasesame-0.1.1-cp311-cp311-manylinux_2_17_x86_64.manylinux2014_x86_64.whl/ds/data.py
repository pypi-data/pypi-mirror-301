from pathlib import Path
import rich
import polars as pl

def view(file: str):
    file = Path(file)
    file_suffix = file.suffix[1:].lower()
    
    readers = {
        "csv": lambda f: pl.read_csv(f),
        "parquet": lambda f: pl.read_parquet(f),
        "json": lambda f: pl.read_json(f),
        "ndjson": lambda f: pl.read_ndjson(f),
    }

    if file_suffix in readers:
        try:
            df = readers[file_suffix](file)
        except:
            if file_suffix == "json":
                df = readers["ndjson"](file)
    elif file_suffix in ["xlsx", "xls"]:
        if rich.confirm("Do you want to view a particular worksheet?"):
            sheet = rich.prompt("Enter the name of the worksheet you want to view")
            # TODO: Add support for sheet indexing
            df = pl.read_excel(file, sheet=sheet)
        else:
            df = pl.read_excel(file)
    else:
        raise ValueError("Unsupported file format")
    
    print(df)