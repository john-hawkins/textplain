# -*- coding: utf-8 -*-
 
"""setup.py: setuptools control."""
 
import re
from setuptools import setup
 
version = re.search(
        '^__version__\s*=\s*"(.*)"',
        open('textplainer/__init__.py').read(),
        re.M
    ).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
setup(
      name = "textplainer",
      packages = ["textplainer"],
      install_requires=[
        'pandas','numpy','spacy'
      ],
      include_package_data=True,
      entry_points = {
        "console_scripts": ['textplainer = textplainer.cli:main']
      },
      version = version,
      description = "Python command line application to analyse impact of a text feature to a machine learning model.",
      long_description = long_descr,
      long_description_content_type='text/markdown',
      author = "John Hawkins",
      author_email = "hawkins.john.c@gmail.com",
      license="MIT",
      url = "https://john-hawkins.github.io/posts/2020/10/textplainer-intuitive-explanations-for-text/",
      project_urls = {
          'Documentation': "https://john-hawkins.github.io/posts/2020/10/textplainer-intuitive-explanations-for-text/",
          'Source': 'https://github.com/john-hawkins/textplainer',
          'Tracker': 'https://github.com/john-hawkins/textplainer/issues',
      },
    )


