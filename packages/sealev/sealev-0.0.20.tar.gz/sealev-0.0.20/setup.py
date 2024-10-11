from setuptools import setup, find_packages

VERSION = '0.0.20' 
DESCRIPTION = 'Se Level DBs'
LONG_DESCRIPTION = 'Allows to access various Sea Level Databases via python'
from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text() 


# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="sealev", 
        version=VERSION,
        author="Alessandro Annunziato",
        author_email="alessandro.annunziato@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=['pycountry','pycurl','requests','reverse-geocoder',
                          'matplotlib','cartopy'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

# python setup.py sdist bdist_wheel
# twine upload dist/*