# python setup.py sdist bdist_wheel
# twine upload dist/*

from setuptools import setup, find_packages

requirements = [
    'tqdm~=4.66.2',
    'requests~=2.31.0',
    'shapely~=2.0.1',
    'osmium~=3.7.0'
],

setup(
    name='vdownload',
    version='1.0.0',
    author = 'Thang Quach',
    author_email= 'quachdongthang@gmail.com',
    url='https://github.com/thangqd/vdownload',
    description=' A Powerful Geospatial Data Downloader',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    requires_python=">=3.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'osmdownload = vdownload.osm.osmdownload:main',
            'osmreplication = vdownload.osm.osmreplication:main',
            'osminfo = vdownload.osm.osminfo:main',
            'osm2geojson = vdownload.osm.osm2geojson:main',
            'osmpub = vdownload.osm.osmpub:main',         
            
            'openbuildings = vdownload.openbuildings.openbuildings:main',
           
        ],
    },    

    # scripts=["bin/utils.py"], # utils.py is just a demo,
    install_requires=requirements,    
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)