## Indices

To control where you want the server to go to when the directory is requested, not a file within, you use the `Index` directive. This contains a list of file names which should be checked to see if they exist. As with all other directives, it is optional, if you don't define the order you want files to be found in, it will default to the following:
```YAML
Index:
    - "index.py"
    - "index.php"
    - "index.html"
    - "index.htm"
    - "index.xml"
    - "index.txt"
    - "index.jpg"
    - "index.png"
    - "index.gif"
    - "index.jpeg"
    - "index.pl"
```
*If the default Index handling were a aelfi.conf directive*