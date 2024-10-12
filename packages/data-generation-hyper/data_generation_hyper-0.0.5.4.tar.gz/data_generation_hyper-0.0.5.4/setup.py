from setuptools import setup, find_packages

setup(
    name="data_generation_hyper",
    version="0.0.5.4",
    author="Cesare Bidini, Onuralp Guvercin, Emin Yuksel, Mevlut",
    author_email="cesare.bidini@gmail.com",
    description="Library for synthetic data generation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cesbid/data_generation",  # Your repository URL
    packages=find_packages(),
    package_data={
        'data_generation.code_generator.config': ['arguments.json']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)