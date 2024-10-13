from setuptools import setup, find_packages

setup(
    name='custom_telegraph',
    version='0.1.0',
    description='A library adds dots annotation to telegraph library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='BeadierMitten49',
    packages=find_packages(),
    install_requires=[
        'telegraph'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
