from setuptools import setup, find_packages

setup(
    name='Country_Converter_Toolkit',
    version='0.1.1',
    description='Package to find out various information about countries: Country Code, Country Language, City and Country Currency Information, Time Conversion, Currency Conversion, and search for Continents from Country Names',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Kelompok 5 AP B',
    author_email='aal3it@gmail.com',
    url='https://github.com/A-M-Haadi/Country_Converter_Toolkit.git',
    packages=find_packages(),
    classifiers=[

    ],
    python_requires='>=3.6'
)