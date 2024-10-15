from distutils.core import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyside6-overlay-busy-indicator',
    packages=['qbusyindicator', 'qbusyindicator.examples'],
    version='1.6',
    license='MIT',
    description='A customizable overlay busy indicator with a smooth fade animation for PySide6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'qbusyindicator.examples': ['*.gif']},
    author='Poria Hemati',
    author_email='poria.hemati@gmail.com',
    url='https://github.com/pohemati/pyside6-overlay-busy-indicator',
    download_url='https://github.com/pohemati/pyside6-overlay-busy-indicator/archive/refs/tags/v1.6.tar.gz',
    keywords=['pyside6', 'overlay', 'busy', 'indicator', 'progressbar',
              'loading'],
    install_requires=[
        'PySide6',
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
