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
# Main Package File
############################################################

############################################################
#BASIC REQUIRED PACKAGES
############################################################
import os,commands,re

############################################################
#GLOBAL VARIABLES
############################################################
BASEDIR=os.path.dirname(__file__)

############################################################
#COMMON ROUTINES
############################################################
class dict2obj(object):
    """Object like dictionary
    
    Parameters:
    ----------
    dict:
       Dictionary with the attributes of object
    
    Examples:
    --------
    >>> c=dictobj({'a1':0,'a2':1})
    
    Addition:

    >>> c+=dictobj({'a3':2})

    """
    import commands
    def __init__(self,dic={}):self.__dict__.update(dic)
    def __add__(self,other):
        for attr in other.__dict__.keys():
            exec("self.%s=other.%s"%(attr,attr))
        return self

def shellExec(cmd,out=True):
    """
    Execute a command

    Parameters:
    ----------
    cmd: Linux command
    out: True if the output of the file goes to a variable.  Fale
    otherwise.

    Returns:
    -------
    output: If out = True, this is the command output.
    """
    if not out:
        system(cmd)
        output=""
    else:
        output=commands.getoutput(cmd)
    return output

def loadConf(filename):
    """Load configuration file

    Parameters:
    ----------
    filename: string
       Filename with configuration values.

    Returns:
    -------
    conf: dictobj
       Object with attributes as variables in configuration file

    Examples:
    --------
    >> conf=loadConf('input.conf')

    """
    d=dict()
    conf=dict2obj()
    if os.path.lexists(filename):
        execfile(filename,{},d)
        conf+=dict2obj(d)
        qfile=True
    else:
        PRINTERR("Configuration file '%s' does not found."%filename)
        errorCode("FILE_ERROR")
    return conf

"""
This lambda function allow to load a configuration file into the
"locals" dictionary of a module.  The objects define in fileconf will
be defined in the local scope of the module.
"""
loadConfiguration=lambda fileconf,scope:scope.\
    update(loadConf(fileconf).__dict__)

def readArgs(argv,fmts,defs,
             Usage="(No usage defined.)"):
    
    """Read the arguments from the command line.

    Parameters:
    ----------
    argv: Array with command line options
    fmts: Format of the 

    Returns:
    -------
    conf: dictobj
       Object with attributes as variables in configuration file

    Examples:
    --------
    $ dir,$conf,$qover=readArgs(argv,
                                ["str","float","int"],
                                ["gato","1.0","30"])
    """

    try:
        if '-h' in argv[1]:
            PRINTERR(Usage)
            exit(0)
    except IndexError:pass
    nvar=len(fmts)
    narg=len(argv)-1
    if narg==0:argv=['']+defs
    args=[]
    for i in range(1,nvar+1):
        try:argv[i]
        except IndexError:argv+=[defs[i-1]]
        if argv[i]=='--':argv[i]=defs[i-1]
        exec("args+=[%s(argv[i])]"%fmts[i-1])
    return args

def copyObject(obj):
    """
    Create a copy of an object
    
    Parameters:
    ----------
    obj: Object to be copies.

    Returns:
    -------
    Copy of the object.
    """
    import numpy as np
    new=dict()
    dic=obj.__dict__
    for key in dic.keys():
        var=dic[key]
        new[key]=var
        try:
            var.__dict__
            inew=copyObject(var)
            new[key]=inew
        except:
            pass
        if isinstance(var,np.ndarray):
            new[key]=copy(var)

    nobj=dict2obj(new)
    return nobj

###################################################
#DECORATION
###################################################
def titleShow(msg,char="*",size="auto"):
    """
    Generate a text title
    """
    if size=="auto":
        size=len(msg)
    title=char*size+"\n%s\n"%msg+char*size
    return title

###################################################
#LOAD CONFIGURATION
###################################################
loadConfiguration(BASEDIR+"/plynet.cfg",locals())
loadConfiguration(BASEDIR+"/datadir.cfg",locals())

###################################################
#TEST
###################################################
if __name__=="__main__":
    print "Main Module."
