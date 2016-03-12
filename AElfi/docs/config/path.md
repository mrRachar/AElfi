## Path
Users tend not to like longer URLs, especially when there writing them down, or seeing them in an email. This is even more the case with GET variables. The problem is, when you need keep everything in one script, and to manage a dynamic site, this might seem impossible. Paths to the rescue! 

In this example, we are directing requests for "users/*userid*/", e.g. `users/13/`, to a GET variable sent to the users.py page: `users
.py?user=13`.
```YAML
Paths:
    My-Userpage-Path-Directive:
        when: ^users/[0-9]+
        from: ^users/([0-9]+)
        to: users.py?user=$1
        options: QSA
```
*A quick example of a path directive. This example is referenced throughout explanations; some regex knowledge required*

***Note:*** *Paths are all relative to the root of the web-app. This means if your web app is in `/var/www/apache2/myapp`, and the file is `/var/www/apache2/myapp/dashboard/index.py`, the path will be `dashboard/index.py`*

#### Title
Each redirect directive is introduced with a name. In the example, this is `My-Userpage-Path-Directive`, which may be a little long. This name should have no spaces, or colons, but apart from that can be *anything*. It doesn't actually affect how the programme runs in any way, except it makes the directive's purpose clearer, and is added as a comment preceding the rule in the `.htaccess` file.

#### When
The `when` condition is a regex expression must be matched before the rule will be run. This is a way of making sure that the rule is only run when you need it to be run. In the case of our example, only when the first characters of the path are "user/" followed by one or more number. For more information about what you can put here, head over to the [Apache .htaccess docs](http://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewritecond).

#### From
The `from` option is a way of collecting any information about the path. So in our case, we want to capture the user id, so we give a regex, where the user id is captured, so we can use it later as the get variable.

#### To
The `to` option says where we need to send this user locally. This of course could be a normal URL, but most likely you are going to want to put some of you regex captures in it. To do this, just put the group number (starting from 1) after a dollar sign, so if the capture group 1 is '562', then `users?user=$1` produces "users?user=562". This is how "directories" and "pages" can be converted into a GET variable form.

