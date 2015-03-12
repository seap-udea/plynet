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

# The Python Planetary Package

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

This is the developer copy.  You may also 

Instructions for the contirbutor
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

Licensing
---------

This project must be used and distributed under the [GPL License
Version 2] (http://www.gnu.org/licenses/gpl-2.0.html).

The symbol `[)]` means that it has been developed under the principles
of the [copyleft philosophy](http://en.wikipedia.org/wiki/Copyleft).

All wrongs reserved to [Jorge
I. Zuluaga](mailto:jorge.zuluaga@udea.edu.co).
