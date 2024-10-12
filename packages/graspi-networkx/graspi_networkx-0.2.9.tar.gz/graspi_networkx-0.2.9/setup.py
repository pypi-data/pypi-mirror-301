from setuptools import setup, find_packages

setup(
    name='graspi_networkx',
    version='0.2.9',
    packages=find_packages(),
    install_requires=[
        'contourpy',
        'cycler',
        'fonttools',
        'kiwisolver',
        'matplotlib',
        'networkx',
        'numpy',
        'packaging',
        'pandas',
        'pillow',
        'pyparsing',
        'python-dateutil',
        'pytz',
        'six',
        'tzdata'
    ],
    python_requires='>=3.6',
    author="Qi Pan",
    author_email="mleung8@buffalo.edu",
    description="A package that utilizes NetworkX functionality for GraSPI",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/gobrin111/graspi_networkx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta"
    ],
)
