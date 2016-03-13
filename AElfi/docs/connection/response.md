## Response Object
The response object, `response`, allows you to modify what you're send the user back. It is, like all [COM](start.md) objects, automatically 
available for you in the global scope.

#### `cookies`
Cookies is a `http.cookies.SimpleCookies` object. These cookies will be sent back to the client, which should store them. See the [Python documentation](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie) for more information on SimpleCookies objects.

#### `header`
`response.header` is a dictionary containing all the HTTP headers that AElfi will be sending back. It contains 'Content-Type' by default, which is 
set to 'text/html;charset=*aelfi.conf charset value*'. You can add your own headers, but you are probably going to want to use the [offical headers](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields#Response_fields).

#### `headersent` 
This variable will be `False`, until the headers have been sent, either by [print](#print)ing or by calling [`sendheaders`](#sendheaders).

#### `print`
`response.print` is where AElfi's special print fuction is defined. It is the same as calling `print` in the global scope. It will automatically send 
headers the first time it is called, so you don't have to.

#### `sendheaders`
This will send all the headers to the client. As it is automatically called by the `print` function, or when a template runs, you don't need to call 
it, unless you've got an empty page with no template, or you need to send the headers early for some reason.