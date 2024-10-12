from setuptools import setup, find_packages

setup(
    name='BagVision',  # Replace with your package name
    version='0.1.0',  # Replace with your package version
    author='Preethi Manne',  # Replace with your name
    author_email='pmanne@ucsd.edu',  # Replace with your email
    description='Bag Identifier',  # Replace with your package description
    packages=find_packages(),
    install_requires=[
        'requests',       # For making HTTP requests
        'beautifulsoup4', # For web scraping
        'pandas',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
