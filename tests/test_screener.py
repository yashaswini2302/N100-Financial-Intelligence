import os

def test_engine_exists():
    assert os.path.exists("src/screener/engine.py")

def test_cli_exists():
    assert os.path.exists("src/screener/cli.py")

def test_export_exists():
    assert os.path.exists("src/screener/export_results.py")

def test_config_exists():
    assert os.path.exists("config/screener_config.yaml")

def test_output_folder():
    assert os.path.exists("output/exports")