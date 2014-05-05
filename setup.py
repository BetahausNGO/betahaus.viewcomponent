import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CREDITS = open(os.path.join(here, 'docs', 'CREDITS.rst')).read()
CHANGES = open(os.path.join(here, 'docs', 'CHANGES.rst')).read()

requires = ('pyramid>=1.2',)

setup(name='betahaus.viewcomponent',
      version='0.3.1b',
      description='betahaus.viewcomponent',
      long_description=README + '\n\n' + CREDITS + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        ],
      author='Robin Harms Oredsson',
      author_email='robin@betahaus.net',
      url='https://github.com/robinharms/betahaus.viewcomponent',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="betahaus.viewcomponent",
      use_2to3=True,
      entry_points = """\
      """,
      )

