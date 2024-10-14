# setup.py

from setuptools import setup

setup(
    name='food_waste_predictor',
    version='0.1',
    py_modules=['food_waste_predictor'],  # Change from find_packages() to py_modules
    install_requires=[
        'pandas',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'food-waste-predictor=food_waste_predictor:cli',
        ],
    },
)
