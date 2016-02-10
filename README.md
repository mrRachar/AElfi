# AElfi
A simple wrapper framework for Python 3 projects on Apache2

Instead of messing around with complicated frameworks, AElfi does all the hard work for you, without making the project too heavy. Just put the AElfi files in your folder, customise the config file if you want to, and run `AElfi/build.py`, and you're set to go! Plus, with integrated `mako` template support, you don't have to worry about messy view scripts.

## Advantages

 1. Pure Python 3, no Python 2 problems or other extras
 2. Simple project building, run the `build.py` script, and it will build a special `.htaccess` file.
 3. Customise how it runs without having to mess with `.htaccess`. The config file `aelfi.conf` allows you to easily describe any path redirects, or anything else you want, in a clean, concise syntax
 4. Mako template support. Save any mako file to `.template` with the same name as a `.py` file, and it will automatically run it for you.

## How to Setup
##### Requirements

- The Mako template engine: `pip3 install mako`
- `AllowOveride` to be on for the entire project folder
- That `mod_rewrite` is enabled:  
```bash
a2enmod rewrite
sudo service apache2 restart
 ```
#### Instructions
1. Download the latest release, and save it as the folder you want to build your web-app in.
2. Edit `aelfi.conf` to your liking. You can change this later. When your finished, run `AElfi/build.py` from the project folder (on Windows, you need to run `python3 ...`). This will generate the appropriate .htaccess file
3. Start writing you Python files! They should work with no extra work :smiley:!

Simple as 1, 2, 3!

## How to Use
### Config file
The `aelfi.conf` file contains allows you to customise the way your app runs. The first part configures AElfi itself, whilst the second half controls the `.htaccess` file, without you having to deal with it directly. When you want to build the config file, run `AElfi/build.py`.

### Request
`request` contains what the user has sent you, so `.header` is a dictionary of all the user headers, and `.cookies` are the cookies. Print anything out for more info about it. 

### Response
`response` also has `.header` and `.cookies`, but these are what you are sending the user back. There is a `.sendheader` method, which will send all the headers, but this happens automatically when you print out something, so you don't have to deal with that

### Templates
The built-in `display` dictionary is empty to start with, and you can fill it throughout your programme. If a file with the same name, but a `.template` extension, is found within the folder, then this will be sent to the `mako` module, and the names within the dictionary will be used as variables within there. This allows you to control which variables you want to send to the view, and also allows you to easily separate the controller and view.
