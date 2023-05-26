from setuptools import setup, find_packages
import versioneer

with open('README_en_US.md', mode='r', encoding='utf-8') as f:
    readme_en_us = f.read()

install_requires = [
    'pycvm>=0.3.2',
    'pybov>=0.1.1',
    'yfinance'
]

setup(name                          = 'pyibr',
      version                       = versioneer.get_version(),
      cmdclass                      = versioneer.get_cmdclass(),
      description                   = 'Calculates fundamental analysis indicators of Brazilian companies',
      long_description              = readme_en_us,
      long_description_content_type = 'text/markdown',
      author                        = 'Giovanni Lourenço',
      author_email                  = 'gvnl.developer@outlook.com',
      url                           = 'https://github.com/glourencoffee/pyibr/',
      license                       = 'MIT',
      packages                      = find_packages(),
      keywords                      = ['investment', 'finances'],
      install_requires              = install_requires,
      python_requires               = '>=3.7'
)