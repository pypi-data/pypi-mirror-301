from setuptools import setup, find_packages

setup(
    name= 'statistic-method',
    version= '0.2',
    packages= find_packages(),
    install_requires= [
        'pandas',
        'openpyxl'
    ],
    author= 'kelompok 2 B',
    description= 'Package ini bertujuan untuk membantu dalam mengolah data/nilai',
)