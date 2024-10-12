from src.main import StatisticMethod
import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), 'example.xlsx')


def test_read_data():
    stat = StatisticMethod(file_path)
    assert "Matematika" in stat.datas


def test_mean():
    stat = StatisticMethod(file_path)
    stat2 = pd.read_excel(file_path)
    assert stat.mean('Matematika') == stat2['Matematika'].mean()


def test_modus():
    stat = StatisticMethod(file_path)
    stat2 = pd.read_excel(file_path)
    print(stat2['Matematika'].mode())
    stat.modus("Matematika")
