from setuptools import setup, find_packages

setup(
    name='bluestocking',
    version='0.1.2',
    author_email='bluestocking-dev@googlegroups.com',
    packages=find_packages(), #['bluestocking'],
    license='GPL',
    description="An information extraction toolkit built on top of NLTK.",
    long_description=open('README.md').read(),
    install_requires=['nltk','numpy']
)
