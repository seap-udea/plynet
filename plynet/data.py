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
# Data module
############################################################
from plynet import *

############################################################
#BASIC REQUIRED PACKAGES
############################################################

############################################################
#LOAD CONFIGURATION
############################################################
loadConfiguration(BASEDIR+"/data.cfg",locals())

############################################################
#ROUTINES
############################################################
def plainID(ID):
    """
    Generate a PlainID from a planetary ID
    """
    chars=('_',' ','+','(',')','-')
    try:
        for char in chars:ID=ID.replace(char,"")
    except:
        rID=[]
        for id in ID:
            for char in chars:id=id.replace(char,"")
            rID+=[id]
        ID=rID
    return ID

def readObject(element,allprops):
    """
    Read an object from a cell element in a XML file.
    """

    results=dict()
    for props in allprops:
        prop=props[0]
        type=props[1]
        if type=="list":
            exec """
%s=element.findall('%s')
results['%s']=[]
results['%s_plain']=[]
for elem in %s:
    results['%s']+=[elem.text]
    results['%s_plain']+=[plainID(elem.text)]
"""%(prop,prop,prop,prop,prop,prop,prop) in locals(),globals()
        else:
            try:
                exec "%s=element.findall('%s')[0]"%(prop,prop)
                exec "%s_vl=%s(%s.text)"%(prop,type,prop)
                if type=='float':
                    try:
                        exec "%s_em=%s(%s.attrib['errorminus'])"%(prop,type,prop) in locals()
                        exec "%s_ep=%s(%s.attrib['errorplus'])"%(prop,type,prop) in locals()
                    except:
                        exec "%s_em=%s_ep=0"%(prop,prop)
                else:
                    exec "%s_em=%s_ep=''"%(prop,prop)
            except:
                if type=='float':
                    exec "%s_vl=-1;%s_em=%s_ep=0"%(prop,prop,prop) in locals()
                else:
                    exec "%s_vl=%s_em=%s_ep=''"%(prop,prop,prop) in locals()

            exec "results['%s']=[%s_vl,%s_em,%s_ep]"%(prop,prop,prop,prop) in locals()

    return results

def loadSystem(filexml,verbose=False):
    """
    Load a planetary system from a XML file.
    """

    from xml.etree import ElementTree as ET
    if verbose:print "Loading info from '%s'..."%filexml
    tree=ET.parse(filexml)
    system=tree.getroot()
    
    #==================================================
    #SYSTEM LEVEL
    #==================================================
    sysdict=readObject(system,SYSPROPS)

    #==================================================
    #BINARY LEVEL
    #==================================================
    sysdict['binaries']=[]
    binaries=system.getiterator("binary")
    sysdict['nbinaries']=len(binaries)
    if sysdict['nbinaries']>0:
        for binary in binaries:
            sysdict['binaries']+=[readObject(binary,BINARYPROPS)]

    #==================================================
    #STAR LEVEL
    #==================================================
    sysdict['stars']=[]
    stars=system.getiterator("star")
    sysdict['nstars']=len(stars)
    if sysdict['nstars']>0:
        for star in stars:
            sysdict['stars']+=[readObject(star,STARPROPS)]
    
    #==================================================
    #PLANETARY LEVEL
    #==================================================
    sysdict['planets']=[]
    planets=system.getiterator("planet")
    sysdict['nplanets']=len(planets)
    if sysdict['nplanets']>0:
        for planet in planets:
            sysdict['planets']+=[readObject(planet,PLANETPROPS)]

    return sysdict

def loadExoplanetCatalogue(systems=CONFIRMED_SYSTEMS,forceload=False,
                           verbose=False):
    """
    Load a catalogue made of multiple XML files.
    """
    catalogue=dict()
    catdir=DATADIR+OEC_DIR+systems
    fpickle='%s/catalogue.pkl'%catdir

    if verbose:
        print "Loading Open Exoplanet Catalogue: '%s'"%catdir
    
    #CHECK VERSION TIME OF THE CATALOGUE
    if not forceload and os.path.isfile(fpickle):
        sp=os.stat(fpickle)
        sc=os.stat(DATADIR+OEC_DIR+".git/FETCH_HEAD")
        if sp.st_mtime<sc.st_mtime:load=False
        else:load=True
    else:
        load=False

    #LOAD PICKLED VERSION OF THE CATALOGUE
    if load:
        import pickle
        fl=open(fpickle,'r')
        dictload=pickle.load(fl)
        fl.close()
        catalogue.update(dictload)
        if verbose:
            print "\tCatalogue unpickled from '%s'"%fpickle,
            print "Done."
    #GENERATE AND PICKLE PYTHON VERSION
    else:
        if verbose:print "\tReading full catalogue"
        out=shellExec("ls -m %s/*.xml"%catdir)
        catalogue['nsystems']=0
        catalogue['nbinaries']=0
        catalogue['nstars']=0
        catalogue['nplanets']=0
        for filexml in out.split(','):
            sysdict=loadSystem(filexml.strip(),verbose=False)
            id=plainID(sysdict['name'][0])
            catalogue[id]=sysdict
            catalogue['nsystems']+=1
            if sysdict['nbinaries']>0:catalogue['nbinaries']+=1
            catalogue['nstars']+=sysdict['nstars']
            catalogue['nplanets']+=sysdict['nplanets']

        import pickle
        fl=open(fpickle,'w')
        pickle.dump(catalogue,fl)
        fl.close()
        if verbose:print "\tCatalogue pickled at '%s'"%fpickle

    if verbose:
        print "\tNumber of systems: %d"%(catalogue['nsystems'])
        print "\tNumber of multiple systems: %d"%(catalogue['nbinaries'])
        print "\tNumber of stars: %d"%(catalogue['nstars'])
        print "\tNumber of planets: %d"%(catalogue['nplanets'])
        print "Done."

    return catalogue

def loadData(filename,typefrm="plynet"):
    """
    Read data file
    
    Parameters:
    ----------
    filename:
       String.  Absolute path of file.
       
    typefrm:
       Format of input file.  
       Accepted formats: 
          plynet: custom format
          apj_data: apj data tables
          apj_ascii: apj ascii tables
          csv: comma separated values

    Returns:
    -------
    data:
       Data in file
    
    """
    
    fl=open(filename)
    if typefrm=="plynet":
        for line in fl:
            #BLANK LINES
            if not re.search("\w",line):continue
            #COMENT LINES
            if "#" in line:
                #HEADER LINE
                if "#0:" in line:
                    line.strip()
                    print "HEAD:",line
            #REST OF LINES
            else:
                print "DAT:",line


    fl.close()

###################################################
#TEST
###################################################
if __name__=="__main__":
    print "Data Module."
