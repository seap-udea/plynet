```
           $$\                                $$\     
           $$ |                               $$ |    
  $$$$$$\  $$ |$$\   $$\ $$$$$$$\   $$$$$$\ $$$$$$\   
 $$  __$$\ $$ |$$ |  $$ |$$  __$$\ $$  __$$\\_$$  _|  
 $$ /  $$ |$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ | $$ |    
 $$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$   ____| $$ |$$\ 
 $$$$$$$  |$$ |\$$$$$$$ |$$ |  $$ |\$$$$$$$\  \$$$$  |
 $$  ____/ \__| \____$$ |\__|  \__| \_______|  \____/ 
 $$ |          $$\   $$ |                             
 $$ |          \$$$$$$  |                             
 \__|           \______/                            

```

# The Python Planetary Physics Package

Presentation
------------

**Plynet** is a package.


History of Development
----------------------

**Plynet** started as a course project in 2011.  In that time Camilo,
Sebastian Bustamante and Nataly.

Getting a copy
--------------

To get a copy of the newest version of this project just execute:

```
$ git clone --branch master http://github.com/seap-udea/plynet.git
```

If you want to get a different branch of the project just change
"master" by the name of the branch.

This is the developer copy.  You may also obtain the latest release of
the installable package, available in the `dist` folder.

Installing
----------

Once you have a developer copy or a user release please check the
options at the beginning of the `setup.py` file.  In particular check
the directory for installation of the data files.  

Once everything is checked run:

```
$ python setup.py install 
```

If you want to install the package in a different directory than the
system pyhton dir use:

```
$ python setup.py install --prefix=<path>
```

where `<path>` is the base directory where to install the package.

It should take into account that even although you modify the prefix
directory the data associated to the package will still be the same as
defined at the beginning of `setup.py`.

Managing Data
-------------

Plynet comes along with diverse data sources (planetary interior
structure models, stellar evolutionary models, planetary database,
etc.)

Contributors
............

Before distributing the package, developers should pack the data in a
proper container.  

This operation is only recommended when something in the data changes
or when new data is added.  For packing the data go to the
"plynet_data" or "data" directory and run:

   ```
   $ bash packdata.sh
   ```

Then, have a cup of coffee, this procedure could take a long time.

Final users
...........

Once the package has been obtained the data is saved in the directory
`/opt/plynet_data`.  To avoid unpack the data during install it is
recommended to run the unpack script:

   ```
   $ bash /opt/plynet_data/packdata.sh
   ```

Instructions for the contributor
--------------------------------

1. Generate a public key of your account at the client where you will
   develop contributions:
   
   ```
   $ ssh-keygen -t rsa -C "user@email"
   ```

2. Upload public key to the github Seap-Udea repository (only authorized
   for the Seap-Udea repository manager), https://github.com/seap-udea.

3. Configure git at the client:

   ```
   $ git config --global user.name "Your Name"
   $ git config --global user.email "your@email"
   ```

4. Get an authorized clone of the project:

   ```
   $ git clone git@github.com:seap-udea/plynet.git
   ```

5. [Optional] Checkout the branch you are interested in
   (e.g. <branch>):

   ```
   $ git checkout -b <branch> origin/<branch>
   ```

6. Checkout back into the master:

   ```
   $ git checkout master
   ```

Licensing
---------

This project must be used and distributed under the [GPL License
Version 2] (http://www.gnu.org/licenses/gpl-2.0.html).

The symbol `[)]` means that it has been developed under the principles
of the [copyleft philosophy](http://en.wikipedia.org/wiki/Copyleft).

All wrongs reserved to [Jorge
I. Zuluaga](mailto:jorge.zuluaga@udea.edu.co).
