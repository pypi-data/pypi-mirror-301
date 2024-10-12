from setuptools import setup, find_packages

setup(
    name="hypermap",  
    version="0.1.2",  
    description="A package for generating wafermap plots with wafer edge, measurements with interpolated contour map, reticles, reticle-level results etc",
    author="yana",
    author_email="yana@hyperlightcorp.com",
    url="",  
    packages=["hypermap"],  
    install_requires=[          
        'matplotlib',           
        'numpy',
        'pandas',
        'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)