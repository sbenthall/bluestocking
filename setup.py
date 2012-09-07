from setuptools import setup

setup(
    name='bluestocking',
    version='0.1.1',
    author_email='bluestocking-dev@googlegroups.com',
    packages=['bluestocking'],
    license='GPL',
    description="An information extraction toolkit built on top of NLTK.",
    long_description=open('README.md').read(),
    install_requires=['nltk']
)
