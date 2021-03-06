## Request Object
The request object, `request`, allows you access to all the information the user has sent you. It is, like all [COM](start.md) objects, automatically available for you in the global scope.

Anything in `header` can also be accessed by subscripting the request object, so `request.header['ip']` and `request['ip']` are the same.

#### `agent`
The user agent, the string version stored in `.header['user agent']`, is parsed to get all the information, from browser to operating system and device type, so you can make best guesses on who your user is.

*[Find more about `UserAgent` and user agent parsing](agent.md)*

#### `args`
These are all the key-value pairs in the GET request. This is basically all the get variables which have values assigned to them. They are in a 
OrderedDict, in the order they were sent.  This is the same as `q_args`.

For the request "index.py?name=hello&settings&page=4&advanced", the args would be `OrderedDict({'name': 'hello', 'page': '4'})`.

*Also available with the [`plus_`](#plus_) and [`raw_`](#raw_) prefixes

#### `cookies`
Cookies is a `http.cookies.SimpleCookies` object. These are the cookies the client has sent to you, which should only be those for your site. See the [Python documentation](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie) for more information on SimpleCookies objects.

#### `directory`
This is the directory your script is running in, so `/hello/world/index.py`'s directory is `/hello/world/`.

#### `fields`
These are all the POST variables that the client has sent you, if they have sent any, as key-value pairs. It is advisable to use [`post`](#post) 
instead for clarity. This is the same as plus_fields.

*Also available with the [`q_`](#q_) and [`raw_`](#raw_) prefixes

#### `get`
These are any get variables you have been sent, either in [`keywords`](#keywords) or in [`args`](#args). They are in a OrderedDict, args first, and 
keywords have the value `None`.  This is the same as `q_get`.

*Also available with the [`plus_`](#plus_) and [`raw_`](#raw_) prefixes

For the request "index.py?name=hello&settings&page=4&advanced", get would be `OrderedDict({'name': 'hello', 'page': '4', 'settings':None, 'advanced': None})`.
#### `header`
These are all the headers the user has sent you in a dictionary. They can also be accessed straight by subscripting the `request` object.
- 'user agent', the user-agent string of the client
- 'ip', the IP address of the client
- 'protocol', the protocol being used, such as which HTTP version, e.g. 'HTTP/1.1'
- 'connection', the type of HTTP connection used. e.g. 'Keep-Alive', will default to '' if no connection type given in the environment variables
- 'method', whether the request was made with 'POST' or 'GET'
- 'accepted language', the language the user has specified *(normally ignored)*
- 'language', the first language the user has specified
- 'location', the location of the file the user requested, not neccessarily the file you're at now *(such as with paths or 404 error messages)*.

#### `keywords`
All the GET variables that weren't assigned to anything, stored in a list in the order they were sent. 
For the request "index.py?name=hello&settings&page=4&advanced", the keywords would be `['settings', 'advanced']`. This is the same as `q_keywords`.

*Also available with the [`plus_`](#plus_) and [`raw_`](#raw_) prefixes

#### `location`
The location of the script being run on the server.

#### `plus_...`
[`get`](#get), [`args`](#args), [`keywords`](#keywords) and [`post`](#post) are also availible with the `plus_` prefix. This uses Python's 
`unquote_plus` method, which also turns `+` into ` `. *This is the default fields and post attributes point to.*

#### `post`
These are all the POST variables that the client has sent you, if they have sent any, as key-value pairs, in the order they were sent in. This is 
the same as plus_post.

*Also available with the [`q_`](#q_) and [`raw_`](#raw_) prefixes

#### `q_...`
[`get`](#get), [`args`](#args), [`keywords`](#keywords) and [`post`](#post) are also availible with the `q_` prefix. This is normally the default and 
uses Python's `unquote` method. *This is the default get, args and keywords attributes point to.*

#### `raw_...`
[`get`](#get), [`args`](#args), [`keywords`](#keywords) and [`post`](#post) are also availible with the `raw_` prefix. This doesn't url decode the 
string.

#### `server`
These are the server variables accessible to the programme.
- 'name', the name the server has been given
- 'ip', the IP address of the server the code is running on
- 'port', the port being accessed.

_**Warning**: Although these values can generally be trusted, in rare cases, server set up will consistently give nonsensical values for them_