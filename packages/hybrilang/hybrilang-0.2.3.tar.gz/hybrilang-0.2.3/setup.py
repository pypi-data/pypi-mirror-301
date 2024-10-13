from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hybrilang',  # Nazwa pakietu na PyPI
    version='0.2.3',  # Zwiększ numer wersji!
    description='The Hybrilang programming language',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Artur Wyroslak', # Twoje imię
    author_email='artur.wyroslak@gmail.com', # Twój email
    license='MIT', # Licencja
    packages=find_packages(exclude=("tests",)), # Znajdź wszystkie pakiety
    install_requires=['llvmlite', 'js2py'], # Zależności 
    entry_points={
        'console_scripts': [
            'hybrilang=hybrilang.__main__:main' # Polecenie "hybrilang"
        ],
    },
    classifiers=[  # Opcjonalne metadane dla PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimalna wersja Pythona
)
