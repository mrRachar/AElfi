# AElfi
A simple wrapper framework for Python 3 projects on Apache2

## How to Setup
Download a release, unzip it, and make it the directory of your webapp/project. Then, write your app therein.

## How to use
Inside a project folder, you can write python files like normal, you don't even need '#usr/bin/env python3' at the start. Most importantly, you don't 
have to deal with the server backend, no more os.environ to find out request headers and the like. Just use the `request` and `response` objects, 
which are built into the environment. All output is automatically encoded in the encoding of your choice, `utf-8` by default, so you don't have to do 
this manually every time you type a non-ASCII symbol

### Request
Request contains what the user has sent you, so `.header` is a dictionary of all the user headers, and `.cookies` are the cookies. Print anything out for more info about it. 

### Response
Response also has `.header` and `.cookies`, but these are what you are sending the user back. There is a `.sendheader` method, which will send all the headers, but this happens automatically when you print out something, so you don't have to deal with that
