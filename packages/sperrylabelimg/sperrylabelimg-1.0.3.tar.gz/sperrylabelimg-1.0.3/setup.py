"""
setup
"""
from setuptools import setup, find_packages

setup(
    name='sperrylabelimg',
    version='1.0.3',
    description='A GUI for labelling images customized for usage at Sperry Rail',
    author='Brooklyn Germa',
    author_email='brooklyn.germa@sperryrail.com',
    url='https://gitlab.com/bGerma/customlabelimg',
    license='MIT',
    # package_dir={'': 'sperryLabelImg'},
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'labelImg==1.8.6'
    ],
    entry_points='''
        [console_scripts]
        sperrylabelimg=app:main
    ''',
)
