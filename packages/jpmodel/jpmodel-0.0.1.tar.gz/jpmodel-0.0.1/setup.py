from setuptools import setup, find_packages

setup(
    name='jpmodel',
    version='0.0.1',
    description='',
    author='jongseo_park',
    author_email='jongsaeu@gmail.com',
    url='',
    install_requires=['tqdm', 'numpy', 'pandas', 'scikit-learn', 'rdkit', 'torch', 'torch_geometric'],
    packages=find_packages(exclude=[]),
    keywords=[],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
