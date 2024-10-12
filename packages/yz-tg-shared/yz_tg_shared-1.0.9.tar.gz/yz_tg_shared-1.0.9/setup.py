from setuptools import setup, find_packages

setup(
    name='yz_tg_shared',
    version='1.0.9',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "greenlet==3.0.3",
        "mysql-connector-python==9.0.0",
        "pyaes==1.6.1",
        "pyasn1==0.6.0",
        "pydantic==1.10.17",
        "pydantic-sqlalchemy==0.0.9",
        "SQLAlchemy==1.4.52",
        "typing_extensions==4.12.2"
    ],
    author='OP',
    author_email='parfenchuks@gmail.com',
    description='A package for shared code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
