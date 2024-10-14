from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='data_science_project_template',
    version='1.0.0',
    description='Data Science Project Template',
    author='Shailaja Janjirala',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'mlflow',
        'sqlalchemy',  # For PostgreSQL connection
        'gcsfs',       # If you plan to use GCP storage
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)

