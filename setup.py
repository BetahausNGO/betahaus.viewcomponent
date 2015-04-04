import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()
CREDITS = open(os.path.join(HERE, 'CREDITS.rst')).read()
CHANGES = open(os.path.join(HERE, 'CHANGES.rst')).read()

requires = ('pyramid>=1.2',
            'venusian',
            'zope.interface',)

setup(name='betahaus.viewcomponent',
      version='0.4.1',
      description='Plugin structure for menus, JSON responses or similar.',
      long_description=README + '\n\n' + CREDITS + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP",
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
      """,)
