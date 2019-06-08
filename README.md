# Linux Server Configuration - Udacity fullstack nano degree project




Host Name: http://ec2-35-181-60-203.eu-west-3.compute.amazonaws.com/
alternative : http://35.181.60.203.xip.io

IP Address: 35.181.60.203

## Amazon Lightsail Server Set Up

1. [Visit Amazon Lightsail](https://lightsail.aws.amazon.com/) First, log in to Lightsail. If you don't already have an Amazon Web Services account, you'll be prompted to create one(n.b account activation may take 24 hours).

2. Create an instance. Once you're logged in, Lightsail will give you a friendly message with a robot on it, prompting you to create an instance. A Lightsail instance is a Linux server running on a virtual machine inside an Amazon datacenter..

3. Choose an instance image: Ubuntu  Lightsail supports a lot of different instance types. An instance image is a particular software setup, including an operating system and optionally built-in applications.

we choose a plain Ubuntu Linux image. There are two settings to make here. First, choose "OS Only" (rather than "Apps + OS"). Second, choose Ubuntu as the operating system.

4. Scroll down to name your instance and click 'Create'

5. The instance needs a few minutes to set up. After it is set up, you will see 'running' in the left corner of the status card with the representations brighter. Take note of the public IP.

6. Click the status card and navigate to account

7. at the bottom you will find a link to the account page to Download your private key which is a .pem file.

8. Click the 'Networking' tab and find the 'Add another' at the bottom. Add port 123 (udp) and 2200(tcp).

## Server Configuration

1. Save the downloaded `.pem` public key file into .ssh folder which is based in the home directory

2. Secure public key while also making it accessible `$ chmod 600 ~/.ssh/YourAWSKey.pem`

N.B. From here take note of the use of first and second instances of terminals. The first terminal will be the server which will be same as a direct operation on the AWS terminal while the second terminal will be used to create the grader's account

3. Open the first terminal and use this key to log into our Amazon Lightsail Server: `$ ssh -i ~/.ssh/YourAWSKey.pem ubuntu@35.181.60.203`

4. Then type  `$ sudo adduser grader` to create another user 'grader'

5. Create a new file in the sudoers directory: `$ sudo nano /etc/sudoers.d/grader`. And give grader the super permisssion `grader ALL=(ALL:ALL) ALL`. In nano save with (control X, then type `yes`, then hit the return key on your keyboard)

6.  Run the following commands to update all packages and install finger package:
- `$ sudo apt-get update`
- `$ sudo apt-get upgrade`
- `$ sudo apt-get install finger`

7. now we will generate a key pair for grader

8. Open a new(now the second) Terminal window (Command+N) and input `$ ssh-keygen -f ~/.ssh/grader-key`

9. Stay on the same(i.e the second) Terminal window, input `$ cat ~/.ssh/grader-key.pub` to read the public key. Copy the public key.

10. Return to the first terminal window where you are logged into Amazon Lightsail as the root user, move to grader's folder by `$ cd /home/grader`

11. Create a .ssh directory (in same first terminal): `$ mkdir .ssh`

12. Create a file to store the public key(still in first terminal that work on the remote server): `$ touch .ssh/authorized_keys`

13. Edit the authorized_keys file `$ sudo nano .ssh/authorized_keys`

14. Change the permission: `$ sudo chmod 700 /home/grader/.ssh` and `$ sudo chmod 644 /home/grader/.ssh/authorized_keys`

15. Change the owner from root to grader: `$ sudo chown -R grader:grader /home/grader/.ssh`

16. Restart the ssh service: `$ sudo service ssh restart`

17. Type `exit` to disconnect from Amazon Lightsail server

18. Log into the server as grader(that is log in via the second terminal window): `$ ssh -i ~/.ssh/udacity_key.rsa grader@35.181.60.203`

19. Enforce the key-based authentication: `$ sudo nano /etc/ssh/sshd_config`. Find the *PasswordAuthentication* line and change 'yes' to `no`. and save changes 

20. to Change the ssh port from 22 to 2200:  Find the *Port* line and change `22` to `2200`. and save changes.

21.  to Disable ssh login for *root* user to secure the server:  Find the *PermitRootLogin* line and edit to `no`. and save changes. 

22.  Restart ssh `$ sudo service ssh restart`

23. Disconnect the server by `^c` and then log back through port 2200: `$ ssh -i ~/.ssh/grader-key -p 2200 grader@35.181.60.203` now loggin in via port 2200

24. Configure Uncomplicated Firewall:
- `$ sudo ufw allow 2200/tcp`
- `$ sudo ufw allow 80/tcp`
- `$ sudo ufw allow 123/udp`
- `$ sudo ufw enable`


## Deploy Catalog Application

Ensure you are logged in as grader. Should at anypoint a ubuntu password is requested simply ^d and use `sudo` to re-execute that command.

1. Install required packages
- `$ sudo apt-get install apache2`
- `$ sudo apt-get install libapache2-mod-wsgi python-dev`
- `$ sudo apt-get install git`

2. Enable mod_wsgi (mod_wsgi package implements an Apache module which can host any Python web application which supports the Python WSGI specification.)`$ sudo a2enmod wsgi` and start the web server by `$ sudo service apache2 start` or `$ sudo service apache2 restart`
3. Enter your public IP address in your browser now and the apache2 default page should be loaded.

4. Create catalog folder to keep app and make grader owner and group of the folder
- `$ cd /var/www`
- `$ sudo mkdir catalog`
- `$ sudo chown -R grader:grader catalog`
- `$ cd catalog`

5. Clone the project from Github: `$ git clone [https://github.com/drmtm/catalog] catalog` (so folder path to app will become `var/www/catalog/catalog`)

(The Web Server Gateway Interface (WSGI) is a specification for simple and universal interface between web servers and web applications or frameworks for the Python programming language.)

6. Create a .wsgi file in `/var/www/catalog/`: `$sudo nano catalog.wsgi` and add the following into this file
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/")

from catalog import app as application
application.secret_key = 'your_secret_key'
```

7. In /var/www/catalog/catalog Rename the `app.py` to `__init__.py` as follows `mv app.py __init__.py`

(The venv module provides support for creating lightweight “virtual environments” with each virtual environment having its own Python binary. It allows the app have its own independent set of installed Python packages in its site directories.)

8. Install virtual environment
- `$ sudo apt-get install python-pip`
- `$ sudo pip install virtualenv`
- `$ sudo virtualenv venv`
- `$ source venv/bin/activate`
- `$ sudo chmod -R 777 venv`

You should see a `(venv)` appears before your username in the command line.

9. Install the Flask and other packages needed for this application
- `$ sudo pip install Flask`
- `$ sudo pip install httplib2 oauth2client sqlalchemy psycopg2 sqlaclemy_utils requests`
N.B. You may need to re-install outside the venv if some modules are missing such as `ImportError: No module named sqlalchemy`...sometimes there are some minimal compatibility issues between venv and some module installation


10. Use the `nano __init__.py` command to change the `client_secrets.json` line to `/var/www/catalog/catalog/client_secrets.json` as follows `CLIENT_ID = json.loads(
    open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']`
    Ensure to look through `__ini__.py` for every instance of this change and replace as stated.
    Also replace
    `if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(0.0.0.0, port=5000)`

    with

    `if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()`

11. Configure and enable the virtual host
N.B `sites-available/: This is an apache2 directory that contains all of the virtual host files that define different web sites. These will establish which content gets served for which requests.`

- `$ sudo nano /etc/apache2/sites-available/catalog.conf`
- Paste the following code and save
```
<VirtualHost *:80>
    ServerName  35.181.60.203
    ServerAlias ec2-18-217-235-171.us-east-2.compute.amazonaws.com 35.181.60.203.xip.io
    ServerAdmin admin@35.181.60.203
    WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
    WSGIProcessGroup catalog
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalog/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalog/static
    <Directory /var/www/catalog/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
You can find your host name in this link: http://www.hcidata.info/host2ip.cgi
you can also use service like xip.io to get DNS name

12. Now we need to set up the database
- `$ sudo apt-get install libpq-dev python-dev`
- `$ sudo apt-get install postgresql postgresql-contrib`
- `$ sudo -u postgres -i`

You should see the username changed again in command line, and type `$ psql` to get into postgres command line

13. Create a user to create and set up the database. My database for example is named `catalog` and the user I am creating is also called `catalog`
- `$ CREATE USER catalog WITH PASSWORD [your password] login ;`
- `$ ALTER USER catalog CREATEDB;`
- `$ CREATE DATABASE catalog WITH OWNER catalog;`
- Connect to database `$ \c catalog`
- `$ REVOKE ALL ON SCHEMA public FROM public;`
- `$ GRANT ALL ON SCHEMA public TO catalog;`
- Quit postgres as follows: `$ \c` and then `$ exit`

List the existing roles: `\du`. The output should be like this:
  ```
                                     List of roles
   Role name |                         Attributes                         | Member of
  -----------+------------------------------------------------------------+-----------
   catalog   | Create DB                                                  | {}
   postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
  ```

14. use `sudo nano` command to change all engine to `engine = create_engine('postgresql://catalog:[your password]@localhost/catalog)` e.g engine = create_engine('postgresql://catalog:grader@localhost/catalog')
Base.metadata.bind = engine.
Ensure to do this in the database_setup.py and the lotsofmenus.py(i.e. in 3 places)

15. Initiate the database if you have a script to do so: `python database_setup.py and populate it`

16. enable your site by executing `sudo a2ensite [name of app]`  for example mine is `sudo a2ensite catalog`

17. Restart Apache server `$ sudo  apache2ctl restart` and enter your public IP address or host name into the browser. Hooray! Your application should be online now!



## Appendix:
N.B.


I. Project Folder(s) structure
```
/var/www/catalog
    |-- catalog.wsgi
    |__ /catalog
         |-- __init__.py
         |-- lotsofmenus.py
         |-- client_secrets.json
         |-- fb_client_secret.json
         |-- database_setup.py
         |-- /static
         |-- /templates
         |-- /venv

```



## Reference
Profound gratitude to:
- https://github.com/juvers/Linux-Configuration
- https://github.com/callforsky/udacity-linux-configuration
- https://github.com/twhetzel/ud299-nd-linux-server-configuration
- https://github.com/boisalai/udacity-linux-server-configuration

Other Resources:
- https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
- Official Ubuntu Documentation, [Automatic Updates](https://help.ubuntu.com/lts/serverguide/automatic-updates.html).
- Ubuntu Wiki, [AutomaticSecurityUpdates](https://help.ubuntu.com/community/AutomaticSecurityUpdates).
- [Askubuntu.com](https://askubuntu.com/)
- [Stackoverflow.com](https://stackoverflow.com/)



