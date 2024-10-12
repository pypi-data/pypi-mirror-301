from setuptools import setup, find_packages

setup(
    name='PyCZINV',
    version='0.1.4',
    author='Hang Chen',
    author_email='hchen8@lbl.gov',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'pygimli',
        # Add any additional dependencies your package requires
    ],
    description='Python package for geophysical inversion tailored to Critical Zone Science.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='geophysical inversion critical zone science',
)
