# Tribe
**Tribe extracts a network from an email mbox and writes it to a graphml file for visualization and analysis.**

[![PyPI version][pypi_img]][pypi_href]
[![Build Status][travis_img]][travis_href]
[![Coverage Status][coveralls_img]][coveralls_href]
[![Code Health][health_img]][health_href]
[![Documentation Status][rtfd_img]][rtfd_href]
[![Stories in Ready][waffle_img]][waffle_href]

[![SNA Visualization](docs/images/sna_viz.png)](docs/images/sna_viz.png)

This repository contains code for the Social Network Analysis with Python
course that is being hosted by District Data Labs.

## Downloading your Data

This code will work with email data; and hopefull you have some to use for
the class. In particular, we will use a common format for email storage
called `mbox` - if you have Apple Mail, Thunderbird or Microsoft Outlook
you should be able to export your `mbox` with a bit of ease. If you have
[Gmail](https://gmail.com), follow these steps to export your mail:

1. Go to [https://www.google.com/settings/datatools](https://www.google.com/settings/datatools).
2. Click on "Create a new archive"
3. Select only Mail to be added to the archive
4. Select your compression format (zip for Windows, tgz for Mac)
5. Once the archive has been created, you will receive an email notifaction

Make sure you do this in advance of the class, it can take hours or even
days for the archive to be created!

For more information: [Download your Data: Per-service information](https://support.google.com/accounts/answer/3024195?hl=en)

## Getting Started

To work with this code, you'll need to do a few things to set up your environment, follow these steps to put together a _development ready environment_. Note that there are some variations of the methodology for various operating systems, the notes below are for Linux/Unix (including Mac OS X). Feel free to add Windows/Powershell instructions to help out as well.

1. Clone this repository

    Using the git command line tool, this is a pretty simple step:

        $ git clone https://github.com/DistrictDataLabs/tribe.git

    Optionally, you can fork this repository into your own user directory, and clone that instead.

2. Change directories (cd) into the project directory

        $ cd tribe

3. (Optional, Recommended) Create a virtual environment for the code and dependencies

    Using `virtualenv` by itself:

        $ virtualenv venv

    Using `virtualenvwrapper` (configured correctly):

        $ mkvirtualenv -a $(pwd) tribe

4. Install the required third party packages using `pip`:

        $ pip install -r requirements.txt

    Note, this may take a little while, but if you already have `matplotlib` and `pygraphviz` installed already, you should have little trouble.

5. Test everything is working:

        $ python tribe-admin.py --help

    You should see a help screen printed out.


<!-- References -->
[pypi_img]: https://badge.fury.io/py/tribe.svg
[pypi_href]: https://badge.fury.io/py/tribe
[travis_img]: https://travis-ci.org/DistrictDataLabs/tribe.svg?branch=master
[travis_href]: https://travis-ci.org/DistrictDataLabs/tribe/
[coveralls_img]: https://coveralls.io/repos/github/DistrictDataLabs/tribe/badge.svg?branch=master
[coveralls_href]: https://coveralls.io/github/DistrictDataLabs/tribe?branch=master
[health_img]: https://landscape.io/github/DistrictDataLabs/tribe/master/landscape.svg?style=flat
[health_href]: https://landscape.io/github/DistrictDataLabs/tribe/master
[waffle_img]: https://badge.waffle.io/DistrictDataLabs/tribe.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/DistrictDataLabs/tribe
[rtfd_img]: http://readthedocs.org/projects/ddl-tribe/badge/?version=latest
[rtfd_href]: http://ddl-tribe.readthedocs.org/en/latest/
