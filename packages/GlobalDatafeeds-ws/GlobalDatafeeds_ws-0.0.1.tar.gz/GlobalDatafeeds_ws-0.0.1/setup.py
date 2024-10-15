from setuptools import setup, find_packages

VERSION = '0.0.1'

DESCRIPTION = 'Package to implement WebSocket API of Global Datafeeds'
LONG_DESCRIPTION = 'Package to implement WebSocket API of Global Datafeeds. This api will provide realtime data as ' \
                   'well as historical data. '

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="GlobalDatafeeds_ws",
    version=VERSION,
    author="Global Datafeeds",
    author_email="developer@globaldatafeeds.in",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    readme="README.md",
    packages=find_packages(),
    install_requires=['websockets'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
    ]
)
