# AElfi
A simple wrapper framework for Python 3 projects on Apache2

*[Documentation](AElfi/docs/main.md)*

Instead of messing around with complicated frameworks, AElfi does all the hard work for you, without making the project too heavy. Just put the AElfi files in your folder, customise the config file if you want to, and run `AElfi/build.py`, and you're set to go! Plus, with integrated [**mako** template](http://www.makotemplates.org/) support, you don't have to worry about messy view scripts.

![Python 3.4+](https://img.shields.io/badge/python-3.4%2B-blue.svg "Fully working, probably can work with lower versions")
![stars](https://img.shields.io/github/stars/mrRachar/AElfi.svg "Low, very low")

## Advantages

 1. Pure Python 3, no Python 2 problems or other extras
 2. Simple project building, run the `build.py` script, and it will build a special `.htaccess` file.
 3. Customise how it runs without having to mess with `.htaccess`. The config file `aelfi.conf` allows you to easily describe any path redirects, or anything else you want, in a clean, concise syntax
 4. Integrated support for [**mako** templates](http://www.makotemplates.org/). Save any mako file to `.template` with the same name as a `.py` file, and it will automatically run it for you.



## How to Setup
##### Requirements

- The Mako template engine: *`sudo`*`pip3 install mako` *- sudo may be neccessay, depending on your system*
- PyYAML for *aelfi.conf* files *`sudo`*`pip3 install pyyaml`
- `AllowOveride` to be on for the entire project folder
- That `mod_rewrite` is enabled:  
```bash
a2enmod rewrite
sudo service apache2 restart
```

#### Instructions
##### Install

Use [AElfi tools](https://github.com/mrRachar/AElfi-tools) for a quick and easy installation

   *or*
   
Download the latest release, and save it as the folder you want to build your web-app in.

   *or*
```bash
wget https://github.com/mrRachar/AElfi/archive/v0.4.0.zip
unzip v0.4.5.zip
mv AElfi-0.4.5 "Your Webapp Name"
```

##### Get Going
1. Edit `aelfi.conf` to your liking. You can change this later. 
2. Run `AElfi/build.py` from the project folder (on Windows, you need to run `python3 ...`). This will generate the appropriate .htaccess file
3. Start writing you Python files! They should work with no extra tinkering :smiley:!

Simple as 1, 2, 3!
