from setuptools import setup, find_packages

setup(
    name='CustomThread',
    version='0.1.1',
    description='A custom threading class in Python that extends the standard threading.Thread.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Leo Gotardo',
    author_email='leonardo.gotardo2@gmail.com',
    url='https://github.com/LeoGotardo/CustomThread',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
