from setuptools import setup, find_packages

setup(
    name='copulasim',
    version='0.1.0',
    description='A simple Python package for working with Gaussian Copulas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ben Melcher',
    author_email='blmelcher@outlook.com',
    url='https://github.com/yourusername/my_package',
    license='MIT',
    packages=find_packages(),  # Ensure it auto-discovers all modules
    python_requires='>=3.6',
)
