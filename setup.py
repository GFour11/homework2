from setuptools import setup
from setuptools import find_namespace_packages
setup(name='clean_folder',
      version='1',
      description='cleaner for your trash folders',
      author='Egor Ulchenko',
      author_email='itxixitxit@gmail.com',
      license='GoIT',
      packages=find_namespace_packages(),
      entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:cleaner']}
      )