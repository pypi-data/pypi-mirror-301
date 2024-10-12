from setuptools import setup, find_packages

setup(
    name='HealthFitness',
    version='0.1.4',
    description='Menyediakan fitur pengecekan kesehatan dan fitness',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Kelompok 4 AP B',
    author_email='rifqialan46475@gmail.com',
    url='https://github.com/RfqiAlan/HealthFitnessCheck',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)