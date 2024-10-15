from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    install_requires = fh.read().splitlines()

setup(
    name='py-pkg-tmpl',
    version='0.0.1-dev',
    license='AGPLv3',
    description='Template for creating and generic Python packages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sabar Dasgupta',
    author_email='s@bardasgupta.com',
    install_requires=install_requires,
    packages=['python_package_template'],
    python_requires='>=3.7'
)
