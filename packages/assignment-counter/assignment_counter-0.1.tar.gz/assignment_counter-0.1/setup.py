from setuptools import setup, find_packages

setup(
    name='assignment_counter',  # The name of your package
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
