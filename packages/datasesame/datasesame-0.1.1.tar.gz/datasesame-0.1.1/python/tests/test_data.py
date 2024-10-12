# TODO add excel tests

from ds.data import view
import pytest
import polars as pl
from sklearn import datasets

# Load the Iris dataset
iris = datasets.load_iris()
iris_df = pl.DataFrame({
    'sepal_length': iris['data'][:, 0],
    'sepal_width': iris['data'][:, 1],
    'petal_length': iris['data'][:, 2],
    'petal_width': iris['data'][:, 3],
    'target': iris['target']
})

# Fixture to create temporary files for different formats
@pytest.fixture(params=['csv', 'json', 'ndjson', 'parquet'])
def temp_file(tmp_path, request):
    file_extension = request.param
    temp_file_path = tmp_path / f'iris.{file_extension}'

    if file_extension == 'csv':
        iris_df.write_csv(temp_file_path)
    elif file_extension == 'json':
        iris_df.write_json(temp_file_path)
    elif file_extension == 'ndjson':
        iris_df.write_ndjson(temp_file_path)
    elif file_extension == 'parquet':
        iris_df.write_parquet(temp_file_path)

    return temp_file_path, file_extension

class TestView:
    def test_view(self, temp_file, capfd):
        temp_file_path, _ = temp_file
        view(temp_file_path)
        captured_view = capfd.readouterr().out 
        print(iris_df)
        captured_iris_df = capfd.readouterr().out 
        assert captured_view == captured_iris_df