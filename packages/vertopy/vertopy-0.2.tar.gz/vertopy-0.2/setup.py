from setuptools import setup, find_packages

setup(
    name="vertopy",
    version="0.2",
    author="Twinkel-Twinkel",
    author_email="bryawanyud@gmail.com",
    description="Library untuk konversi unit panjang, berat, suhu, dan waktu",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)