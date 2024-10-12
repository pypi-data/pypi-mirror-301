#!/bin/bash

uv venv

source .venv/bin/activate

uv pip install -r pyproject.toml

uv pip install pytest

uv pip install maturin