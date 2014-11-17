# Tribe

**Social Network Analysis of Email**

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

5. Add the `tribe` module to the Python path for easy import

    There are a variety of ways to accomplish this, you could set the `$PYTHONPATH` environment variable, you could edit the `scripts/tribe-admin.py` file to modify the `sys.path` at runtime; choose your favorite approach. Mine is to use `.pth` files as below:
    
    First, find out the location of your Python cite packages with the following command:
    
        $ python -c 'from distutils.sysconfig import get_python_lib; print get_python_lib();'
    
    This is such a useful command, that I have it aliased in my .profile. Once you know this directory, create a .pth file with the current working directory in it as follows:
    
        $ echo $(pwd) > tribe.pth
        $ mv tribe.pth /path/to/site/packages/
    
    Then simply move the .pth file to the location that was specified in the first command. Open up a new terminal window, and cd into your home directory. Open up a python iterpreter and type in `import tribe` - this should work with no errors. 
    
5. (Optional) Add a symlink to the `scripts/tribe-admin.py` script to your `$PATH`. 

    The simplest way to deal with this is to create a directory, `$HOME/bin` then add that directory to your `$PATH` using your bash profile. Of course, there are a variety of ways to do this as well, you could add the `scripts` directory to your `$PATH`, symlink that directory to `/usr/local/bin` or a similar place on Windows. Whatever you're most comfortable with is fine. 
    
6. Test everything is working:

        $ scripts/tribe-admin.py --help
    
    You should see a help screen printed out (if you have import errors, see step 5, if you have a non executable error, make sure that you chmod tribe-admin.py to be executable). 
    
