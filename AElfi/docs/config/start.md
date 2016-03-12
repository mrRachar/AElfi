## The Configuration File
Often you need to control how AElfi runs and manages access to your files. You need *aelfi.conf*, AElfi's universal config file.

*aelfi.conf* is a YAML *(YAML Ain't Markup Language)* file, which contains two streams: 

- The first controls AElfi
- The second part controls your web-app

### The First Half - Runtime Configuration
The first half control's AElfi's behaviour, handling how AElfi runs and processes files when sending them back to the user. This includes the default charset, and nothing else yet.

- How to control the [*default* charset](charset.md)

### The Second Half - Build Configuration
Think of this part as describing your web-apps' behaviour. It describes how files should be accessed, so your server can be protected from running bad files, or you can make nicer file names for scripts actually taking in GET variables.

- Making one file seem like another with [Path](path.md)s
- [Protect](protect.md)ing your server from malicious uploads
- When all goes wrong, saving face by controlling [Errors](errors.md)
- Where to start with [Indices *Index*](indices.md)

***Note:*** *The file is YAML, and thus values may or may not be quoted. The examples given do vary. As a general rule, only quote if you need to*

## A Nice Example
```YAML
# Runtime Configuration    # Here we control how AElfi runs
---                        # Start this part of the document

Charset: 'utf-8'           # Any Python recognised one should do the trick

...						   # We've finished controlling how AElfi runs

# Build Configuration	   # Let's turn to descriping our app's behaviour
---

Errors:					   # What to do in these cases
    # You'll notice that this starts with `text:`, so is not taken as a path
    403: "text:Let's just pretend that file doesn't exist [403 Forbidden]"
    # This one is a relative path
    404: "errors/404.py"
    # This one is an absolute path
    418: "/var/www/teapot/stopthinkingyouregettingcoffee.png"

Protect:					# Let's protect somewhere
    - myproject/resources   # This directory the user might upload to

Paths:                      # Now we need to reroute our user to a different file
    CGI-directory:          # Any name will do, it just clarifies it a bit
        when: '\.py$'       # Only if the file ends in `.py` (regex)
        from: '^(.*)$'      # Capture the entire file location
        to: 'cgi/$1'        # Send it to the same place, but from the cgi file
        options: 'QSA'      # Any extra options we need
```
