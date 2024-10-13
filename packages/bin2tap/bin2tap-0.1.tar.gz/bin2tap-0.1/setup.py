from setuptools import setup, find_packages

setup(
    name='bin2tap',
    version='0.1',
    author='Raül Torralba',
    description='Convert a binary file into ZX Spectrum TAP file',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        bin2tap=bin2tap.cli:main
    ''',
)