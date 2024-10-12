import setuptools
#from setuptools import setup, Extension,find_packages

from distutils.core import setup, Extension

from Cython.Build import cythonize
from readme_renderer import markdown
#ext_modules = cythonize([Extension("distancia.distance", ["distancia/distance.py"])])

with open("README.md", "r") as fh:
    long_description = fh.read()
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()    
 

setuptools.setup(
#setup(
    
    #ext_modules=ext_modules,
    #ext_modules = cythonize(ext_modules),


    name="distancia", # Replace with your username

    version="0.0.62",

    author="Yves Mercadier",

    author_email="",

    description="distance metrics,data-science deep-learning machine-learning neural-network",

    long_description=markdown.render(long_description),
    #long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://pypi.org/project/distancia/",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=3.0',

)
