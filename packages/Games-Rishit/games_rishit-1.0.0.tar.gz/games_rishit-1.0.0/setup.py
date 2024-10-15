
### 2. `setup.py`
'''This file is essential for packaging your project and making it available via pip.

python'''
from setuptools import setup, find_packages
setup(
    name='Games_Rishit',
    version='1.0.0',
    description='A collection of mini-games: Tic-Tac-Toe, Air Hockey, and Dodgeball.',
    author='Rishit Dhiman',
    author_email='dhimanrishit21@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pygame','numpy'  # Assuming your games use pygame
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
