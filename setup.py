from setuptools import setup, find_packages

setup(
    name='healthcare',
    version='0.1.0',
    packages=find_packages(include=['healthcare']),
    test_suite = 'test',
    install_requires=[
        "colorama >= 0.4.0"
    ],
    python_requires='>=3.6'
)
