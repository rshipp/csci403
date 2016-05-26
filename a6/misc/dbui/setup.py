import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pymongo',
    'shapely',
    'pyramid_chameleon',
    ]

setup(name='dbui',
      version='0.1',
      description='dbui',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="dbui",
      entry_points="""\
      [paste.app_factory]
      main = dbui:main
      """,
      )
