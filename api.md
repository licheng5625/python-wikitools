api.py is a module used for communication with the wiki. It is always used, though not always necessary to import directly.

api.py contains three object definitions, [APIRequest](APIRequest.md), [APIResult](APIResult.md), and [APIListResult](APIListResult.md). Of these, APIRequest is the only one that will typically need to be used in a program.

api.py also contains 2 exception definitions, [APIError](APIError.md) and [APIDisabled](APIDisabled.md).

# Functions #

## resultCombine ##
`resultCombine(type, old, new)` - resultCombine is used to combine the results from multiple queries into one result by merging data structures and removing duplicate results. <var>type</var> is the query type (e.g. backlinks, revisions, etc.). <var>new</var> is the result to be merged and <var>old</var> is the result to merge into. This may be made into a method of APIResult in the future.

## urlencode ##
`urlencode(query, doseq=0)` - This is a slightly modified version of Python's urllib.urlencode function designed to work a little better with the way wikitools handles utf-8.

# Variables #
  * <var>canupload</var> - boolean, set to true if the "poster" package is available. Determines if file upload support should be enabled.
  * <var>gzip</var> - Either the Python gzip module or False if gzip and StringIO aren't available.

# Imports #
  * urllib2
  * re
  * time
  * sys
  * urllib.quote\_plus, urllib.is\_unicode
  * poster.encode.multipart\_encode
  * json or simplejson (still imported as json)
  * gzip
  * StringIO