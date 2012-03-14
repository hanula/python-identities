from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='identities',
      version=version,
      description="Simplifying identification of third-party and local resources.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='identity manager resources identification accounts social',
      author='Sebastian Hanula',
      author_email='sebastian.hanula@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
