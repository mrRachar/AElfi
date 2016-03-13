## Connection Object Model Objects
When your getting a page ready for the user, you are dealing with two parts: the user's request, and your response. Apache litters information about these in many different variables, from `os.environ` to `sys.stdin`, and doesn't give them in a very nice format. This can make your code hard to write, as you have to find everything, and scavenge the information from it once you have, and even harder to understand later.

AElfi, natrually, puts everything nice and neatly in two objects, one a `Request` instance, one a `Response`. These objects contain everything you 
need to work out exactly the what, how and who of the user, and to control exactly what you giving them back. They are both already in the 
global scope, so you've got them automatically.

### Request
Request contains all the information that the user has sent you. This includes any 'GET' or 'POST' variables, as well as cookies, protocol, ip, and requested URL, even the language their browser asked for. It also contains the user agent, which has been parsed for you.

*[Find out more about the `request` object](request.md)*

### Response
To control your response other then how the page looks like, you will need to use `response`. This contains the HTTP headers and any cookies you're sending back.

*[Find out more about the `response` object](response.md)*