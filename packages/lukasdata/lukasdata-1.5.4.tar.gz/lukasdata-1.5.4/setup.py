from setuptools import setup, find_packages

setup(
    name='lukasdata',
    packages=find_packages(),
    version='1.5.4',
    install_requires=["numpy","pandas","matplotlib","regex","seaborn"
    ]
)