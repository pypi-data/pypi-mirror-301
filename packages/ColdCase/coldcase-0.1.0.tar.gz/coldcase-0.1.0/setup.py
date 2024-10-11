from setuptools import setup, find_packages

setup(
    name='ColdCase', 
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ColdCase=ColdCase.__main__:main',
        ],
    },
    author='Andrew Marchese',
    author_email='aj.marchese@outlook.com',
    description='Various libraries',
    url='https://github.com/AndrewJesse/ColdCase',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
