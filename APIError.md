APIError is an exception raised in the api module. It is the base class for all other API-related exceptions, which is currently only APIDisabled. APIError extends [Exception](http://docs.python.org/library/exceptions.html#exceptions.Exception).

APIError (not including subclasses) is currently raised in the following situations:
  * If a multipart request is made and the poster module is not available
  * When trying to change the result format using changeParam
  * When the MediaWiki API returns an error