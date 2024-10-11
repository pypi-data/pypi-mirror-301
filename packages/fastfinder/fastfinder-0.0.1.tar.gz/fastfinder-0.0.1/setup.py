from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/fastfinder/__version__.py").read())

def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()


setup(
    name="fastfinder",
    description='Building lightcurve features for fast-evolving transients such as Kilonovae',
    long_description=readme(),
    long_description_content_type="text/markdown",
    version=__version__,
    author='genghisken',
    author_email='ken.w.smith@gmail.com',
    license='MIT',
    url='https://github.com/mFulton07/LasairFastfinder',
    packages=find_packages(),
    include_package_data=True,
    insall_requires=[
        'pandas',
        'matplotlib',
        'astropy',
        'dustmaps',
        'mocpy',
        'scikit-learn',
      ],
    classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
          'Topic :: Utilities',
    ],
    python_requires='>=3.8',
)
