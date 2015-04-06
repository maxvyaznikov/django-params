from setuptools import setup, find_packages


setup(
    name='django-params',
    version='0.1',
    url='https://github.com/maxvyaznikov/django-params',
    download_url='https://github.com/maxvyaznikov/django-params',
    author='Max Vyaznikov',
    author_email='maxvyaznikov@gmail.com',
    license='LICENSE',
    description="Django package makes possible to store in DB and manage "
                "through django-admin parameters with different types",
    long_description=open('README.txt').read(),
    platforms='Any',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    packages=find_packages(),
    include_package_data = True,
)
