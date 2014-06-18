import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid_chameleon',
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'dnspython',
    ]

setup(name='bind9ui',
      version='0.0',
      description='bind9ui',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
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
      test_suite="bind9ui",
      entry_points="""\
      [paste.app_factory]
      main = bind9ui:main
      """,
      )
