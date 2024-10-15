# setup.py

from setuptools import setup

setup(
    name='food_waste_predictor',
    version='0.13',
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
    description='A command-line tool to predict food waste based on household size, food type, and amount purchased.',  # Short description
    long_description=open('README.md').read(),  # Read the README.md file for long description
    long_description_content_type='text/markdown',  # Specify that the long description is in Markdown format
    author='KARP',  # Replace with your name

    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
