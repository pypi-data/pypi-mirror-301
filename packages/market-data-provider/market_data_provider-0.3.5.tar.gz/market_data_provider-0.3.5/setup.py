from setuptools import setup, find_packages

setup(
    name='market-data-provider',
    version='0.3.5',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tenacity',
        'pytz',
    ],
    author='Maksym Usanin (usanin.max@gmail.com)',
    description='Market data provider',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
