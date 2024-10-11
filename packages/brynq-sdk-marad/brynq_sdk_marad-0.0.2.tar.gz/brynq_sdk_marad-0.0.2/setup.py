from setuptools import setup

setup(
    name='brynq_sdk_marad',
    version='0.0.2',
    description='Marad wrapper from BrynQ',
    long_description='Marad wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.marad"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
    ],
    zip_safe=False,
)