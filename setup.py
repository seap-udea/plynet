############################################################
#           $$\                                $$\         #
#           $$ |                               $$ |        #
#  $$$$$$\  $$ |$$\   $$\ $$$$$$$\   $$$$$$\ $$$$$$\       #
# $$  __$$\ $$ |$$ |  $$ |$$  __$$\ $$  __$$\\_$$  _|      #
# $$ /  $$ |$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ | $$ |        #
# $$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$   ____| $$ |$$\     #
# $$$$$$$  |$$ |\$$$$$$$ |$$ |  $$ |\$$$$$$$\  \$$$$  |    #
# $$  ____/ \__| \____$$ |\__|  \__| \_______|  \____/     #
# $$ |          $$\   $$ |                                 #
# $$ |          \$$$$$$  |                                 #
# \__|           \______/                                  #
#                                                          #
# Jorge I. Zuluaga [)] 2015                                #
############################################################
# Package Setup
############################################################
from setuptools import setup, find_packages
from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data

############################################################
#GLOBAL VARIABLES
############################################################
DATA_INSTALL=False
DATA_DIR="/opt/plynet_data"

############################################################
#INSTALLATION PROCEDURES
############################################################
class install_scripts_custom(install_scripts):
    def run(self):
        install_scripts.run(self)
        if DATA_INSTALL:
            print "Creating plynet_data...",
            system("mkdir -p %s"%DATA_DIR)
            print "Done."

class install_data_custom(install_data):
    def run(self):
        install_data.run(self)
        if DATA_INSTALL:
            print "Unpacking data...",
            system("bash -x %s/unpack.sh &> /tmp/pack.log"%DATA_DIR)
            print "Done."

############################################################
#SETUP
############################################################
if DATA_INSTALL:
    data_files=[('%s'%DATA_DIR,
                 ['data/pack.tar','data/unpack.sh','data/packdata.sh'])]
else:
    data_files=[]

setup(
    name        = "plynet",
    version     = "0.1.0a1",
    description = "Python Planetary Physics Package",
    url         = "http://github.com/seap-udea/plynet",
    author      = "Jorge I. Zuluaga",
    author_email= "jorge.zuluaga@udea.edu.co",
    license     = "GPL2.0",
    classifiers = [
        "Development status :: 1 - Planning",
        "Intended audience :: Scientist",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 2.6"
        ],
    keywords    = "plynet planets",
    packages    = find_packages(exclude=['contrib','docs','tests*']),
    package_data= {'plynet':['*.cfg']},
    scripts     = ['plynet_check'],
    data_files  = data_files,
    test_suite  = "tests",
    cmdclass    = {'install_scripts':install_scripts_custom,
                   'install_data':install_data_custom}
)
