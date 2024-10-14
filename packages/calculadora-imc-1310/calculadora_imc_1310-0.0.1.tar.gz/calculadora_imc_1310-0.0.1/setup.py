from setuptools import setup, find_packages

with open("README.md", 'r') as f: 
    page_description = f.read()

with open("requirements.txt") as f: 
    requirements = f.read().splitlines()

setup(
    name="calculadora_imc_1310",
    version="0.0.1",
    description="Calculadaor de IMC (Índice de Massa Corporal)", 
    long_description=page_description, 
    long_description_content_type="text/markdown", 
    author="SMC", 
    url="https://github.com/SergioMCavalcante/calculadora_imc_1310", 
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)