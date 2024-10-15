from setuptools import setup, find_packages

setup(
    name='normalizer_usps',
    version='0.1.0',         
    description='A library for normalizing US addresses.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    url='https://github.com/larissabeatrizlima/normalizer_usps', 
    author='Larissa Lima',
    author_email='larissabeatrizlima@outlook    .com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={'normalizer_usps': ['data/*.json']},
    install_requires=[
        'pandas',
        'importlib_resources; python_version < "3.9"',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
