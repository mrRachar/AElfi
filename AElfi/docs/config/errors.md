## Errors

Things go wrong, more often then we want. Sometime it's out of our hands, like when users try to go to places that don't exist, sometimes, well, let's not go there. To handle things when they go wrong, use the error directive. It contains a mapping of [error codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error) to files, which can be Python scripts.
```YAML
Errors:
    403: "text:Let's just pretend that file doesn't exist [403 Forbidden]"
    404: errorpages/404.py
```
*An example handling the errors 403 and 404*

***Note:*** *Paths must be relative to the apache DocumentRoot in the case of error handler files, due to limitations of .htaccess files. They can also contain the `text:` descriptor, which means the text is shown directly to the user*

If you want to access the original page the user was trying to get to, especially helpful when you're handling a 404 error, you can access it in the [`request.headers['location']`](../connection/request.md) variable, which always contains the original page the user was trying for.