from setuptools import find_packages, setup

setup(
    name='data_science_project_template',
    version='0.1.0',
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
)

