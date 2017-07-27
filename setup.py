import os
from setuptools import setup, find_packages, Command

# Thanks http://stackoverflow.com/questions/3779915/why-does-python-setup-py-sdist-create-unwanted-project-egg-info-in-project-r
class CleanCommand(Command):
  """Custom clean command to tidy up the project root."""
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
  name="doomfist",
  description="Orthofit backend",
  version=1.0,
  packages=find_packages(),
  install_requires=requirements,
  include_package_data=True,
  cmdclass={
        'clean': CleanCommand,
    }
)