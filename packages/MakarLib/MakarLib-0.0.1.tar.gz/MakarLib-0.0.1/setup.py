from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='MakarLib',
  version='0.0.1',
  author='Makar',
  author_email='',
  description='Hello World',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://ru.wikipedia.org/wiki/%D0%9D%D0%B5%D0%B3%D1%80',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='makar',
  project_urls={},
  python_requires='>=3.6'
)