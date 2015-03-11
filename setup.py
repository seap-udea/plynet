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
from os import path,system
import sys

class install_scripts_custom(install_scripts):
    def run(self):
        install_scripts.run(self)
        print "Creating plynet_data...",
        system("mkdir -p /opt/plynet_data")
        print "Done."

class install_data_custom(install_data):
    def run(self):
        install_data.run(self)
        print "Unpacking data...",
        system("bash /opt/plynet_data/unpack.sh")
        print "Done."

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
    data_files  = [('/opt/plynet_data',['data/data.tgz','data/unpack.sh'])],
    scripts     = ['plynet_check'],
    cmdclass    = {'install_scripts':install_scripts_custom,
                   'install_data':install_data_custom}
)
