#!/bin/bash
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
# Packing plynet data
############################################################
DATADIR="pack"
EXCLUDE="--exclude unpack.sh --exclude packdata.sh --exclude pack --exclude pack.tar"

echo "Preparing tarball..."
tar zcf $DATADIR/data.tgz $EXCLUDE *

cd $DATADIR
echo "Splitting tarball..."
rm data_*
split -b 1000000 data.tgz data_
rm data.tgz

echo "Adding data files to git database..."
git add -f data_*
cd -

echo "Putting files in a distributable tarball..."
tar cf pack.tar $DATADIR

echo "Done."
