from setuptools import find_packages, setup

setup(
    name='vzool-config',
    version='0.0.1',
    description='A class for managing configuration settings in a SQLite database.',
    author='Abdelaziz Elrashed Elshaikh Mohamed',
    author_email='aeemh.sdn@gmail.com',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.9",
    packages=find_packages(
        include=[
            'config',
        ],
    ),
    requires=[],
)