from setuptools import setup

setup(
    name='deploybot',
    author='G Adventures',
    author_email='software@gadventures.com',
    description='Slackbot Utils for deploying',
    packages=[
        'deploybot'
    ],
    install_requires=[
        'requests==2.18.4',
    ],
)
