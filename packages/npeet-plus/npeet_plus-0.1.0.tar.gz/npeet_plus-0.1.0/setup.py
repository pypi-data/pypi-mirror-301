from setuptools import setup, find_packages

setup(
    name='npeet_plus',
    version='0.1.0',
    author='Greg Ver Steeg',
    author_email='albert.buchard@me.com',
    description='Non-parametric entropy estimation toolbox plus additional features',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/npeet_plus',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'scipy>=1.4.0',
        'scikit-learn>=0.22.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Copyright (c) 2022 Greg Ver Steeg
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
