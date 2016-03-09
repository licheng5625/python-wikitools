The APIRequest object is used to handle communication with the wiki. All functions that interact with the wiki use one or more APIRequests. Each object is designed to handle one API query. All HTTP requests are done via POST.



# Constructor #
APIRequest has 4 constructor parameters, 2 of which are required:
  * <var>wiki</var> - A [Wiki](Wiki.md) object corresponding to the site to communicate with **(required)**
  * <var>data</var> - A Python dictionary of key:value options for the API query **(required)**
  * <var>write</var> - Specifies whether the request is making a change on the wiki or not, HTTP error handling changes slightly for write queries. The default value is <var>False</var>.
  * <var>multipart</var> - Do the HTTP request as "multipart/form-data" rather than "application/x-www-form-urlencoded." This is needed only for file uploads and requires the [poster](http://pypi.python.org/pypi/poster) package to be installed. The default value is <var>False</var>.

# Methods #

## setMultipart ##
`setMultipart(multipart=True)`
Switch a request's encoding between "multipart/form-data" used for uploading and "application/x-www-form-urlencoded" used for everything else. This requires the poster package. Set <var>multipart</var> to True to use multipart encoding, set to False to use urlencoding.

## changeParam ##
`changeParam(param, value)`
Change the <var>value</var> of a parameter, <var>param</var> (or add a new parameter) in the request parameters. This **must** be used rather than changing the value of the <var>data</var> member variable as this function also updates the encoded parameters sent in the HTTP request.

## query ##
`query(querycontinue=True)`
Do the HTTP request and return a result. If querycontinue is set to True (the default), and a [query-continue](http://www.mediawiki.org/wiki/API:Query#Continuing_queries) value is found in the results, the query will be automatically continued with the value until a query is done that does not have a query-continue. The returned result will include the results from all queries combined. This behavior may or may not be useful for any particular application.

## Private methods ##
  * `__longQuery` - Implements the querycontinue option by searching for query-continue values and re-running queries with them
  * `__getRaw` - Gets the raw JSON text from the server, handles HTTP errors
  * `__parseJSON` - Transforms the JSON object into a Python object, handles maxlag errors.

# Member variables #
## Public ##
  * <var>sleep</var> - Controls how long to sleep before trying a request again after an HTTP error. Automatically incremented by getRaw. This should not be changed and it may be made private in a future release.
  * <var>data</var> - A shallow copy of (not a reference to) the <var>data</var> parameter passed during construction. This can be read, but should not be changed; use <var>changeParam</var> instead.
  * <var>iswrite</var> - The value of the <var>write</var> parameter passed during construction. Can be changed, though there isn't much reason to do so.
  * <var>multipart</var> - The value of the <var>multipart</var> parameter passed during construction.  This can be read, but should not be changed; use <var>setMultipart</var> instead.
  * <var>encodeddata</var> - The value of the <var>data</var> variable encoded for the HTTP request. This should not be changed and it may be made private in a future release.
  * <var>headers</var> - The HTTP headers for the HTTP request. This can be changed if you really know what you're doing.
  * <var>wiki</var> - The value of the <var>wiki</var> parameter passed during construction. This cannot be changed and it may be made private in a future release.
  * <var>response</var> - Contains an [httplib.HTTPMessage](http://epydoc.sourceforge.net/stdlib/httplib.HTTPMessage-class.html) with headers and other information after <var>query</var> is called. Set to False before the request is made.
  * <var>opener</var> - Contains a [urllib2.OpenerDirector](http://docs.python.org/library/urllib2.html#urllib2.OpenerDirector). This should not be modified and may be made private in a future release.
  * <var>request</var> - Contains a [urllib2 Request](http://docs.python.org/library/urllib2.html#request-objects) object. This should not be changed unless modifying an HTTP header, in which case the following code should be used:
> ```
apireq.request = urllib2.Request(apireq.wiki.apibase, apireq.encodeddata, apireq.headers)```
> where apireq is the APIRequest to be modified

## Private ##
  * `_continues` - Used in longQuery, otherwise unset.
  * `_generator` - Used in longQuery, otherwise unset.

# Examples #
See the [MediaWiki API](http://www.mediawiki.org/wiki/API) documentation for information about what information is available from the API and what parameters to use. "format=json" is automatically applied to each request and cannot be overridden.

Get some information about a wiki:
```
import pprint # Used for formatting the output for viewing, not necessary for most code
from wikitools import wiki, api
site = wiki.Wiki("http://www.mediawiki.org/w/api.php")
params = {'action':'query',
    'meta':'siteinfo',
    'siprop':'general'
}
req = api.APIRequest(site, params)
res = req.query(querycontinue=False)
pprint.pprint(res)
```
This will return something like:
```
{u'query': {u'general': {u'articlepath': u'/wiki/$1',
                         u'base': u'http://www.mediawiki.org/wiki/MediaWiki',
                         u'case': u'first-letter',
                         u'dbtype': u'mysql',
                         u'dbversion': u'4.0.40-wikimedia-log',
                         u'fallback8bitEncoding': u'windows-1252',
                         u'generator': u'MediaWiki 1.16wmf4',
                         u'lang': u'en',
                         u'mainpage': u'MediaWiki',
                         u'phpsapi': u'apache2handler',
                         u'phpversion': u'5.2.4-2ubuntu5.7wm1',
                         u'rev': 68239,
                         u'rights': u'Creative Commons Attribution-Share Alike 3.0 Unported',
                         u'script': u'/w/index.php',
                         u'scriptpath': u'/w',
                         u'server': u'http://www.mediawiki.org',
                         u'sitename': u'MediaWiki',
                         u'time': u'2010-06-26T19:08:50Z',
                         u'timeoffset': 0,
                         u'timezone': u'UTC',
                         u'variantarticlepath': False,
                         u'wikiid': u'mediawikiwiki',
                         u'writeapi': u''}}}
```