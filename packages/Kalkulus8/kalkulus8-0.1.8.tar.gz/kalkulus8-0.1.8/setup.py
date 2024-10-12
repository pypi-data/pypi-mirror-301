from setuptools import setup, find_packages

setup(
    name='Kalkulus8',
    version='0.1.8',
    description='Paket ini terdiri dari beberapa modul yang berfungsi untuk menganalisis berbagai inputan dalam lingkup kalkulus',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Kelompok 8 AP B',
    author_email='indiraramayani9@gmail.com',
    url='https://github.com/indirarara/CalculusPython8.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.20',
        'matplotlib>=3.3',
        'sympy>=1.8',
    ],
)

