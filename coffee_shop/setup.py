from setuptools import find_packages, setup

setup(
    name='coffee_shop_api',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'coffee_shop_api',
    ],
)