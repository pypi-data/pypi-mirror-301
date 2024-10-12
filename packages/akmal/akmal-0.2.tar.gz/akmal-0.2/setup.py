from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name='akmal',  # Nama package kamu di PyPI
    version='0.2',  # Versi package
    packages=find_packages(),  # Cari semua modul secara otomatis
    description='orang tamvan',
    long_description=description,
    long_description_content_type='text/markdown',
    author='akmal',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 