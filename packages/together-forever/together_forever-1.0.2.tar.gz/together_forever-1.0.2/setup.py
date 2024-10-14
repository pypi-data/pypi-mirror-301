from setuptools import setup
from pathlib import Path

if __name__ == "__main__":
  long_description = ("./README.md")
  this_directory = Path(__file__).parent
  setup(
    packages = ['together_forever'],
    long_description=long_description,
    long_description_content_type='text/markdown'
  )
