from setuptools import setup, find_packages

setup(
    name='sqlalchemy_pydantic_crud',
    version='0.1.3',
    author='Denisov Pavel',
    author_email='denisov.p.g@gmail.com',
    description='Base CRUD for SqlAlchemy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        # List your package dependencies here
    ],
)
