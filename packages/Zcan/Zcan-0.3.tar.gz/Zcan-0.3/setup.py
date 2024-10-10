from setuptools import setup, find_packages
 
setup(
    name='Zcan',
    version='0.3',
    description='A small example package',
    packages=find_packages(),
    package_data={'': ['*.py']},
    python_requires='>=3.6',
)