import setuptools

setuptools.setup(
    name="browser_utils",
    version="0.1.0",
    url="https://github.com/birdsarah/tracking_checks",

    author="Sarah Bird",
    author_email="github@birdsbits.com",

    description="Util functions for inspecting your browser's data",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'pandas>=0.23',
        'requests',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
