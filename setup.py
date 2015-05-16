"""
aio.testing
"""

from setuptools import setup, find_packages

from aio.testing import __version__ as version


setup(
    name='aio.testing',
    version=version,
    description="Aio testing utils",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='',
    author='Ryan Northey',
    author_email='ryan@3ca.org.uk',
    url='http://github.com/phlax/aio.testing',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['aio'],
    include_package_data=True,
    zip_safe=False,
    test_suite="aio.testing.tests",    
    install_requires=[
        'setuptools',
        ],
    entry_points="""
    # -*- Entry points: -*-
    """)
