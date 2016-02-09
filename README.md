# AElfi
A simple wrapper framework for Python 3 projects on Apache2

## How to Setup
1. Download the latest release, and save it as the folder you want to build your web-app in. You will also need `mod_rewrite`
2. Edit `aelfi.conf` to your liking. You can change this later. When your finished, run `AElfi/build.py` from the project folder. This will generate the appropriate .htaccess file
3. Start writing you Python files! They should work with no extra work :smiley:!

Simple as 1, 2, 3!

### Request
Request contains what the user has sent you, so `.header` is a dictionary of all the user headers, and `.cookies` are the cookies. Print anything out for more info about it. 

### Response
Response also has `.header` and `.cookies`, but these are what you are sending the user back. There is a `.sendheader` method, which will send all the headers, but this happens automatically when you print out something, so you don't have to deal with that
