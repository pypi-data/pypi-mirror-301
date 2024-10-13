from setuptools import setup, find_packages

setup(
    name="validantor",  # Cambia el nombre según tu preferencia
    version="0.1.0",
    author="Daniel Soto",  # Cambia esto por tu nombre
    author_email="dansoto804@gmail.com",  # Cambia esto por tu correo
    description="A simple data validation library in Python.",
    long_description=open("README.md").read(),  # Asegúrate de tener un archivo README.md
    long_description_content_type="text/markdown",
    url="https://github.com",  # Cambia esto por tu repositorio
    packages=find_packages(),  # Encuentra automáticamente los paquetes en tu proyecto
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Cambia si usas otra licencia
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Cambia según la versión mínima de Python que soportas
    install_requires=[],  # Aquí puedes agregar dependencias si las tienes
)
