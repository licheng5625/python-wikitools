<font size='5pt'><b>Note that this project is now hosted at <a href='https://github.com/alexz-enwp/wikitools'>GitHub</a></b> </font>All changes to the code will be done there, any new bugs should be reported there, and future releases will be available there (and via pypi)



---




Python package to interact with the MediaWiki API. The package contains general tools for working with wikis, pages, and users on the wiki and retrieving data from the MediaWiki API. There is also the source for some en.wikipedia specific scripts using the framework, including the source for [Mr.Z-bot @ en.wikipedia](http://en.wikipedia.org/wiki/User:Mr.Z-bot).

  * The wikitools module requires Bob Ippolito's [simplejson](http://pypi.python.org/pypi/simplejson) module or the json module in Python 2.6+.
  * Chris AtLee's [poster](http://pypi.python.org/pypi/poster) package is needed for file upload support in all Python versions, but it is not required for use. If not present, file upload support will be disabled.
  * Version 1.1.1 was released on 14 April 2010. Source downloads with a setup.py script, a Windows installer, and an RPM are available in the Downloads tab or the right sidebar.
  * wikitools will be roughly following the MediaWiki release cycle for major releases, ensuring that each release is compatible with the version of MediaWiki released at the same time. If you are using the development alpha version of MediaWiki (as Wikipedia does), you should consider using the development version of wikitools, which can be downloaded via SVN here (from the "source" tab). Old versions can be downloaded from the [deprecated download list](http://code.google.com/p/python-wikitools/downloads/list?can=4).
  * Note that due to developer time constraints, only the most recent release and the SVN version are supported and receive bugfix releases. For major bugs affecting old versions, a patch may be released.
  * Documentation is available on the [wiki](wikitools.md)

  * Some bot scripts (not the framework itself) require the [MySQLdb module](http://sourceforge.net/projects/mysql-python) and a MySQL server.
  * Scripts in the "pywiki" branch directory require [Pywikipedia](http://meta.wikimedia.org/wiki/Pywiki). Note that these scripts are unmaintained and may no longer work.
  * If you'd like to help out with this, send me an email (mrzmanwiki {at} gmail {dot} com) or leave a message on my en.wikipedia user talk page.

  * [README](http://python-wikitools.googlecode.com/svn/trunk/README)
  * Also available on the Python package index: [pypi](http://pypi.python.org/pypi/wikitools)

  * Author: Alex Zaddach
  * Some assistance and code by [bjweeks](http://en.wikipedia.org/wiki/User:bjweeks)