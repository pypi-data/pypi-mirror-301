from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hybrilang',
    version='0.2.0',  # Zmień wersję przy kolejnych publikacjach
    description='The Hybrilang programming language',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='adowu',
    author_email='artur.wyroslak@gmail.com',
    license='MIT', # lub inna licencja
    packages=find_packages(),
    install_requires=['llvmlite', 'js2py'],
    entry_points={
        'console_scripts': [
            'hybrilang=hybrilang:main'
        ],
    },
)
