"""
setup
"""
from setuptools import setup, find_packages
# from gnupg import

setup(
    name='sperrylabelimg',
    version='1.0.0',
    description='A GUI for labelling images customized for usage at Sperry Rail',
    author='Brooklyn Germa',
    author_email='brooklyn.germa@sperryrail.com',
    url='https://gitlab.com/bGerma/customlabelimg',
    license='MIT',
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
        sperrylabelimg=sperryLabelImg.app:main
    ''',
)
