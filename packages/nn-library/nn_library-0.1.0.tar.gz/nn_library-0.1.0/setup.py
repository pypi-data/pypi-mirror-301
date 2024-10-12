from setuptools import setup, find_packages

setup(
    name='nn_library',  # Replace with your package’s name
    version='0.1.0',
    packages=find_packages(),
    setup_requires=['wheel'],
    author='Vitalii Cherednyk',
    author_email='vitalijcerednik@gmail.com',
    description='A library for building neural networks.',
    python_requires='>=3.6',
)
