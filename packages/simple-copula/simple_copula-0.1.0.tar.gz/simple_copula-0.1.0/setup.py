from setuptools import setup, find_packages

setup(
    name='simple_copula',              # Your package name
    version='0.1.0',                # Version of your package
    description='A simple Python package for working with Gaussian Copulas',  # Short description
    long_description=open('README.md').read(),      # Full description from README
    long_description_content_type='text/markdown',  # Content type of README
    author='Ben Melcher',              # Your name
    author_email='blmelcher@outlook.com',  # Your email
    url='https://github.com/yourusername/my_package',  # URL to the package repository
    license='MIT',                   # License of your package
    packages=find_packages(),        # Automatically find packages in your directory
    install_requires=[],             # List of dependencies
    classifiers=[                    # Optional: Metadata for PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',         # Minimum Python version required
)
