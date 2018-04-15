from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pycheckers',
    version='0.1.0',
    description='Checkers game for AI algorithms demonstration',
    long_description=readme,
    author='Bartłomiej Bielecki, Jakub Fajkowski, Piotr Hachaj',
    url='https://github.com/jfajkowski/pycheckers',
    license=license,
    packages=find_packages(exclude=('docs', 'tests'))
)