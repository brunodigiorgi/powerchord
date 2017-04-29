from setuptools import find_packages
from setuptools import setup

install_requires = [
  'numpy',
]

tests_require = [
  'pytest',
]

setup(name='powerchord',
      version='0.1',
      description='chord label parsing library for music information retrieval',
      author='Bruno Di Giorgi',
      author_email='bruno@brunodigiorgi.it',
      url='https://github.com/brunodigiorgi/powerchord',
      license="GPLv2",
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
        'testing': tests_require,
      },
      )
