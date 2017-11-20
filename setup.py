import sys
from setuptools import setup, find_packages

# require pypandoc conversion for upload
if 'upload' in sys.argv[1:]:
    import pypandoc
    README = pypandoc.convert('README.md', 'rst')
else:
    README = open('README.md').read()


setup(
    name='django-template-forms',
    description='Template based form rendering for Django',
    long_description=README,
    author='Ryan P Kilby',
    author_email='rpkilby@ncsu.edu',
    url='https://github.com/rpkilby/django-template-forms/',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    version='0.1.0',
    zip_safe=False,
    install_requires=[],
    license='BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
