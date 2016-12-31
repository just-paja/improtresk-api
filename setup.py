import os

from pip.req import parse_requirements

from setuptools import setup

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='improtresk-api',
    version='0.0.1',
    packages=['api'],
    include_package_data=True,
    description="Api for Improtresk registration system",
    long_description=README,
    url='https://github.com/PetrDlouhy/django-related-admin',
    install_requires=reqs,
    author='Petr Dlouhy, Paja Zak',
    author_email='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
