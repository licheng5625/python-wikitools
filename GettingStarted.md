This page details the options for downloading and installing wikitools. The instructions should work for any operating system, though they are designed mainly for Windows and Linux.
<div>
<br>
</div>
# Downloading #

There are several options for downloading wikitools, depending on your particular platform. The files can be downloaded from this site, from the [Downloads tab](http://code.google.com/p/python-wikitools/downloads/list) or from the [Python package index](http://pypi.python.org/pypi/wikitools) (aka, the Cheese shop). The files are the same on both sites, however the pypi are signed.

## Plain archives ##
There are 2 types of compressed archives available, a zip file and a gzipped tarball. The tarball can be opened with the command `tar -xzf wikitools-version.tar.gz` from a command line on Linux (or any system with the tar utility installed) or by using a program like 7zip on Windows. The zip file can be uncompressed with the built-in utility in all recent versions of Windows or with the zip command on other systems

## RPMs and Windows installer ##
The RPM files and Windows installer can be installed immediately after download, no preparation is required.

# Installing #

## Checking requirements ##
wikitools is untested on Python versions older than 2.5 or any 3.x version. It may work on older 2.x versions. If using 2.5 or older, the [simplejson](http://pypi.python.org/pypi/simplejson) package is required. The [poster](http://pypi.python.org/pypi/poster) package is required for file upload support in all Python versions. If not present, wikitools will still work, but upload support will be disabled.

## Standard installation ##
The "standard" installation installs wikitools using the standard Python installation location, into the site-packages directory, which will make wikitools available for all users on the machine:

### Source archives ###
After uncompressing the archive (see above), change to the recently uncompressed directory (which by default is titled "wikitools-version#") in a command line/terminal.

Simply run
```
python setup.py install
```
On Linux/Unix, you may have to run it as root depending on file permissions for Python's directories. On Windows Vista or 7 you may have to run the program as an administrator depending on your security setting and where Python is installed.

### Windows installer ###
Download and run the executable file, then click through the prompts. Note that on Windows Vista or 7 you may have to run the program as an administrator depending on your security setting and where Python is installed.

### RPM ###
The RPM files can be used on Linux systems that use an [RPM-based](http://en.wikipedia.org/wiki/RPM_Package_Manager) package manager. Download the file and run
```
rpm --install filename
```
You may need to run it as root.

## Alternate installation ##
In certain situations, you may not be able to install Python packages in the default location (such as a system that you do not have root access on). These instructions apply only to the source archives and cannot be done with the installer/RPM.

In Python 2.6 and newer versions, the following command can be substituted for the install command in the [section above](GettingStarted#Source_archives.md):
```
python setup.py install --user
```
This will install wikitools into a per-user directory. On Unix, `~/.local/lib/pythonX.Y/site-packages`. On Windows, `%APPDATA%/Python/PythonXY/site-packages` (where X and Y are the Python version numbers)

In older versions of Python, or where a different location is desired, the following command can be used:
```
python setup.py install --home=<dir>
```
wikitools will be installed under `<dir>/lib/python`. You may need to add this directory to the PYTHONPATH environment variable (see the documentation for your OS for how to do that).

# Using #
  * For new users getting started, see [QuickStart](QuickStart.md).
  * Experienced Python programmers should read the [Documentation](Documentation.md) for information about objects and functions provided by wikitools.

# See also #
  * For detailed information on installing 3rd party python packages, see [Installing Python Modules](http://docs.python.org/install/).
  * [PEP 370](http://www.python.org/dev/peps/pep-0370/), for more information on the per-user site packages directory described in the "Alternative installation" section.