## Protect

You can't trust everyone. This is especially important when building web apps where you are uploading files from users. Someone devious, let's call them [Alice](https://xkcd.com/177/), could upload a file to you site which might be a Python file. If you do nothing, Alice's file will be able to be executed, and thus run. To stop this, you need to create 'safe' zones, areas where nothing will execute. To do this, you just add a directory to the Protect directive, and all the files within will be protected.
```YAML
Protect:
    - resources/useruploads/  #It is best to end the directory with a slash
    - content/userfiles/
```
*A quick example of a protect directive*

***Note:*** *When paths are relative, they are relative to the root of the web app*

It is best to end the directory with a slash, otherwise AElfi might protect `/useruploads_safe/`, if you only specify `/useruploads`. Adding the slash means only this directory is protected.

The example would protect any file in the 'useruploads' and 'userfiles' directory, as well as any subdirectory. You can add as many, or as few as you want.

