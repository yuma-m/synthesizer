from setuptools import setup, find_packages
version = '0.1.0'

try:
    import pypandoc
    read_md = lambda f: pypandoc.convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='synthesizer',
    version=version,
    description="A simple virtual analog synthesizer.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        ],
    keywords='analog synthesizer',
    author='Yuma Mihira',
    author_email='info@yurax2.com',
    url='https://github.com/yuma-m/synthesizer',
    license='GPLv3',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    zip_safe=True,
    long_description=read_md('README.md'),
    test_suite='test',
)
