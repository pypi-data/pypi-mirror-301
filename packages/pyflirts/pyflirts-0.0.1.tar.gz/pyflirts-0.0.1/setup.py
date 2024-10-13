from setuptools import setup, find_packages

setup(
    name='pyflirts',
    version='0.0.1',
    author='Shiva Mishra',
    author_email='pyflirts@gmail.com',
    description='one line flirt lines for programmers ( flirt lines as a service )',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyflirts/pyflirts',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
