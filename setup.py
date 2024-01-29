import os
from setuptools import setup, find_packages

# Obtiene el path absoluto del proyecto.
proj_directory = os.path.dirname(
    os.path.abspath(
        __file__,
    ),
)

# Obtiene los paquetes requeridos para el proyecto.
with open(os.path.join(proj_directory, "requirements.txt"), "r", encoding="utf-16") as f:
    required_packages = f.read().splitlines()
print(required_packages)

# Setup del proyecto
setup(name='trustmonitor', 
      version='0.1', 
      install_requires=required_packages,
      packages=find_packages())