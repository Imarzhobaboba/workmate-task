import pytest
import csv
import tempfile
from io import StringIO
import argparse
from main import filter_data, aggregate_data, is_numeric  # Замените your_module на имя вашего модуля

@pytest.fixture
def sample_csv_data():
    data = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4"""
    return data

@pytest.fixture
def sample_csv_file(sample_csv_data):
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(sample_csv_data)
        f.seek(0)
        yield f.name

def test_is_numeric():
    assert is_numeric("123") is True
    assert is_numeric("123.45") is True
    assert is_numeric("abc") is False
    assert is_numeric("") is False
    assert is_numeric("123a") is False

def test_filter_data_equals(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    # Создаем mock для args
    args = argparse.Namespace()
    args.where = "brand=apple"
    args.aggregate = None
    
    filtered = filter_data(csv_dict, args)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'iphone 15 pro'

def test_filter_data_greater_than_numeric(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = "price>300"
    args.aggregate = None
    
    filtered = filter_data(csv_dict, args)
    assert len(filtered) == 2
    assert all(float(row['price']) > 300 for row in filtered)

def test_filter_data_less_than_numeric(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = "price<300"
    args.aggregate = None
    
    filtered = filter_data(csv_dict, args)
    assert len(filtered) == 2
    assert all(float(row['price']) < 300 for row in filtered)

def test_filter_data_greater_than_text(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = "name>p"
    args.aggregate = None
    
    filtered = filter_data(csv_dict, args)
    assert len(filtered) == 2  # 'redmi note 12' и 'samsung galaxy s23 ultra'

def test_aggregate_data_avg(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = None
    args.aggregate = "price=avg"
    
    result = aggregate_data(csv_dict, args)
    assert result['aggregation'] == 'avg'
    assert result['column'] == 'price'
    assert pytest.approx(result['value']) == (999 + 1199 + 199 + 299) / 4

def test_aggregate_data_min(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = None
    args.aggregate = "price=min"
    
    result = aggregate_data(csv_dict, args)
    assert result['aggregation'] == 'min'
    assert result['column'] == 'price'
    assert result['value'] == 199

def test_aggregate_data_max(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = None
    args.aggregate = "price=max"
    
    result = aggregate_data(csv_dict, args)
    assert result['aggregation'] == 'max'
    assert result['column'] == 'price'
    assert result['value'] == 1199

def test_aggregate_non_numeric_column(sample_csv_data):
    csv_dict = list(csv.DictReader(StringIO(sample_csv_data)))
    
    args = argparse.Namespace()
    args.where = None
    args.aggregate = "name=avg"
    
    result = aggregate_data(csv_dict, args)
    assert result is None
