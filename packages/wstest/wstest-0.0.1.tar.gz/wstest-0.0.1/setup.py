from setuptools import setup, find_packages

setup(
    name='wstest',
    version='0.0.1',
    description='PYPI tutorial package creation written by wonseop',
    author='wonseop',
    author_email='wonseop.kim@samsung.com',
    url='https://github.com/wonseop/wstest',
    install_requires=['tqdm', 'pandas', 'scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=[],
    python_requires='>=3.7',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)