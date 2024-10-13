# setup.py
from setuptools import setup, find_packages

setup(
    name='goallteam_library_entity',
    version='0.0.2',
    packages=find_packages(),
    install_requires=['sqlalchemy'],  # Lista de dependencias
    author='goallteam',
    author_email='kenan249@gmail.com',
    description='Libreria de entidades para goallteam',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Go-All-Team/library-entity.git',  # Repositorio de GitHub u otro
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
