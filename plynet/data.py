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
class Stack(object):
    def __init__(self,ncols):
        self.ncols=ncols
        if ncols>1:
            self.array=np.zeros((0,ncols))
        else:
            self.array=np.array([])
    def __add__(self,array):
        if self.ncols>1:
            self.array=np.vstack((self.array,array))
        else:
            self.array=np.append(self.array,array)
        return self
    def __or__(self,other):
        new=np.vstack((np.transpose(self.array),
                       np.transpose(other.array)))
        return np.transpose(new)
    
def toStack(array1d):
    sarray=stack(1)
    sarray.array=array1d
    return sarray

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

def saveData(filename,fts,data):
    """
    Save data from matix 'data' (plain list) using field specifications provided in
    fts.

    Example:
      fts=[
        # IDs
        ("ID","-","s"),
        ("KOI","-","s"),
        ("TN","-","s"),
        ("KIC","-","d"),

        # Stellar information
        ("stag","-","s"),
        ("Ms","Msun","f"),
        ("dMsp","Msun","f"),
        ("dMsm","Msun","f"),
        ("Rs","Rsun","f"),
        ("dRsp","Rsun","f"),
        ("dRsm","Rsun","f")]
    
    """
    fl=open(filename,"w")

    # Create header
    nfields=len(fts)
    header1="#"
    header2="#u:"
    header3="#t:"
    for i in xrange(nfields):
        field=fts[i]
        header1+="%d:%s\t"%(i,field[0])
        header2+="%s\t"%(field[1])
        header3+="%s\t"%(field[2])
    
    fl.write(header1+"\n")
    fl.write(header2+"\n")
    fl.write(header3+"\n")

    for row in data:
        i=0
        for field in row:
            typed=fts[i][2]
            try:
                fl.write(DATA_FORMAT[typed][2]%field+'\t')
            except:
                print "I cannot write ",field,"as ",DATA_FORMAT[typed][2]
                fl.write("-99\t")
            i+=1
        fl.write("\n")

    fl.close()
        
def readData(filename,typefrm="plynet",verbose=False):
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
          cds: cds format
          ipac: ipac format
          csv: comma separated values

    All files should be formatted in a particular form.

    Example: plynet:

       #0:Col0   1:Col1   2:Col2
       #-        m        AU
       #:s       f        f

    The first column in the header is the name of each column.  The
    second line are the physical units.  The third line are the type
    of data.  This line must alwasy start with '#:'.

    Returns:
    -------

    data:

       Data in the file.  Data is a dictionary.  Keys are the name of
       the columns.  Elements of the dictionary are lists of values.

    fields:
       
       List of tuples.  Each tuple has the key of the data and types
       dictionaries and the units of each field.
       Example: [('field1','kg'),('field2','m'),('field3','-')]

    types: 

       Dictionary.  Keys are the name of columns.  Value is the type
       of the column (indicated as d - integer, f - float, s -
       string).
  
    Example:
    >> data,fields,types=readData("data/LowDensity.pdat")
    >> print fields
    [('ID', '#-'), ('Rp', 'Rjup'), ('dRpp', 'Rjup'), ('dRpm', 'Rjup')]
    >> print data['ID']

  
    """
    if verbose:
        print "Loading data file '%s'..."%filename

    if os.path.isfile(filename):
        fl=open(filename)
    else:
        errorMsg("Data file does not exist",extra=filename)

    data=dict()
    fields=[]
    types=dict()

    if typefrm=="plynet":
        if verbose:print "\t","Plynet datafile"
        for line in fl:

            #BLANK LINES
            line=line.strip("\n\r")

            #BLANK LINES
            if not re.search("\w",line):
                continue

            #COMENT LINES
            elif "#" in line:

                #HEADER LINE
                if "#0:" in line:
                    data=dict()
                    field_parts=line.split()
                    fields=[]
                    for field_str in field_parts:
                        m=re.search("(\d+):(\w+)",field_str)
                        try:
                            num=int(m.group(1))
                            nam=m.group(2)
                        except:
                            errorMsg("readData","Bad formed header",extra=field_str)
                        data[nam]=[]
                        fields+=[(nam,)]
                    
                #UNITS LINE
                if "#u:" in line:
                    line=line.replace("u:","")
                    units=line.split()
                    for i in xrange(len(units)):
                        fields[i]+=(units[i],)

                #CONVERSION LINE
                if "#t:" in line:
                    line=line.replace("t:","")
                    type_parts=line.split()
                    types=dict()
                    i=0
                    for type_str in type_parts:
                        nam=fields[i][0]
                        m=re.search("(\w)",type_str)
                        types[nam]=m.group(1)
                        i+=1

            #REST OF LINES: READ DATA
            else:
                content_parts=line.split()
                i=0
                for content in content_parts:
                    field=fields[i][0]
                    typed=types[field]
                    exec("val=%s(content)"%DATA_FORMAT[typed][0])
                    data[field]+=[val]
                    i+=1

    elif typefrm=="ipac":
        if verbose:print "\t","IPAC datafile"
        ftypes=dict(double='f',char='s',integer='d',int='d')
        ndesc=0
        data=dict()
        for line in fl:
            leading=line[0]
            if leading=="\\":continue

            #Description lines
            if line[0]=="|":
                line=line.strip("\n\r")
                
                # Field names
                if ndesc==0:
                    parts=line.split("|")
                    dfields=[]
                    for field in parts:
                        field=field.strip(" \n\r")
                        if field=="":continue
                        dfields+=[field]
                    ndesc+=1
                    for field in dfields:
                        data[field]=[]


                # Types
                elif ndesc==1:
                    parts=line.split("|")
                    types=dict()
                    i=0
                    for ftype in parts:
                        ftype=ftype.strip(" \n\r")
                        if ftype=="":continue
                        types[dfields[i]]=ftypes[ftype]
                        i+=1
                    ndesc+=1

                # Units
                elif ndesc==2:
                    parts=line.split("|")
                    fields=[]
                    i=0
                    for unit in parts:
                        unit=unit.strip("\n\r")
                        if unit=="":continue
                        unit=unit.strip(" ")
                        fields+=[(dfields[i],unit)]
                        i+=1
                    ndesc+=1

            # Data
            else:
                #values=line.split("\t")
                values=re.split("\s{2,}",line)
                i=0
                for field in fields:
                    ftype=types[field[0]]
                    if values[i]=="null":values[i]=DATA_FORMAT[ftype][1]
                    exec("value=%s(values[i])"%(DATA_FORMAT[ftype][0]))
                    data[field[0]]+=[value]
                    i+=1
        
    elif typefrm=="cds":
        if verbose:print "\t","CDS datafile"
        ftypes=dict(I='d',F='f',E='f',A='s')
        sepline=0
        qstart=True
        for line in fl:

            # STRIP LINES
            line=line.strip("\n\r")

            # BLANK LINES
            if not re.search("\w",line) and \
                    not re.search("[-=]",line):continue

            # SEPARATOR LINE
            if "----" in line:
                sepline+=1

            # DATA DESCRIPTION
            elif sepline==2:

                if qstart:
                    types=dict()
                    dfields=[]
                    fields=[]
                    qstart=False

                # SEPARATE INFORMATION FROM LINENUMBERS
                m=re.search("\s+\d+\s*-\s*\d+ (.+)",line)
                try:parts=m.group(1).split()
                except:continue
                
                # SEARCH FOR FIELD NAME
                fname=parts[2]
                fname=re.sub("[()\[\]\/-]","_",fname)
                fname=fname.strip("_")
                dfields+=[fname]

                # SEARCH FOR UNITS
                units=parts[1]
                fields+=[(fname,units)]
                
                # SEARCH FOR TYPE
                ftype=parts[0][0]
                ftype=ftypes[ftype]
                types[fname]=ftype

            elif sepline==3:
                for field in dfields:
                    data[field]=[]

            elif sepline==4:
                values=line.split()
                i=0
                for field in dfields:
                    exec("value=%s(values[i])"%(DATA_FORMAT[types[field]][0]))
                    data[field]+=[value]
                    i+=1

    fl.close()
    return data,fields,types

def data2Matrix(data,types,fields,index,verbose=False):
    
    """
    Convert (part of a) float or integer columns into a single float
    matrix.

    Columns of the matrix correspond to "fields".  Rows correspond to
    the object.

    Parameters:
    ----------

    data:

       Dictionary.  Keys are name of fields.  Value are list of values
       for this field.

    types: 

       Dictionary.  Keys are the name of columns.  Value is the type
       of the column (indicated as d - integer, f - float, s -
       string).
       
    fields:
       
       List of tuples.  Each tuple has the key of the data and types
       dictionaries and the units of each field.
       Example: [('field1','kg'),('field2','m'),('field3','-')]

    index:

       Name of one of the columns that can be used to search for a
       given row.  Example if fields are Col0, Col1, Col2 and the
       first column is an identifier you can use this identifier as
       index.

    Return:
    ------

    indexes:

       List of indexes to find the data in the data file.

    cols:

       Name of the columns included in the matrix in the same order as
       they are tabulated.

    matrix:
    
       Numpy matrix with non-textual data (float and integers).


    Example:
    -------

    data2Matrix is normally used together with readData in this way:

        >> data,fields,types=readData("KOI_KIC-Asteroseismology-Huber+2014.txt")
        >> rows,cols,matrix=data2Matrix(data,types,fields,"KIC")
        >> print rows
        ['11446443', '10666592', '8554498', '11853905', '6521045', '8866102', '7051180']
        >> print cols
        [('Teff','K'), ('dT','K'), ('FeH','dex'), ('dFeH','dex'), ('rho','kg/m3'), ('drho',,'kg/m3'), ('R','Rjup'), ('dR','Rjup'), ('M','Msun'), ('dM','Rsun')]
        >> print matrix[:,0]
        [ 5850.  6350.  5753.  5781.  5825.  6325.  5302.  5669.  5627.  5896.]
        
    You can recover the values corresponding to a given index using the index method:

        >> i = rows.index("8554498")
        >> print matrix[i,:]
        [  5.75300000e+03   7.50000000e+01   5.00000000e-02   1.00000000e-01
        2.96500000e-01   9.20000000e-03   1.74700000e+00   4.20000000e-02
        1.13000000e+00   6.50000000e-02]
    
    """
    
    ndata=len(data[index])
    if verbose:
        print "Converting data with %d rows using index %s"%(ndata,index)
    indexes=[]
    matrix=[]
    for i in xrange(ndata):
        indexes+=[data[index][i]]
        row=[]
        cols=[]
        for field in fields:
            fieldn=field[0]
            typed=types[fieldn]
            if typed!="s":
                cols+=[fieldn]
                val=data[fieldn][i]
                row+=[val]
        matrix+=[row]
    return indexes,cols,np.array(matrix)

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

def loadKOI(koi,verbose=False):
    """
    Load a KOI object
    """
    koistr="%04d"%int(koi)
    filexml=DATADIR+OEC_DIR+KEPLER_SYSTEMS+"KOI-%s.xml"%koistr
    try:
        koisys=loadSystem(filexml)
    except:
        errorMsg(loadKOI,"KOI number did not found.")
    return koisys

def loadConfirmed(name,verbose=False):
    """
    Load a Confirmed system
    """
    filexml=DATADIR+OEC_DIR+CONFIRMED_SYSTEMS+"%s.xml"%name
    try:
        sys=loadSystem(filexml)
    except:
        errorMsg(loadKOI,"Planet '%s' did not found."%name)
    return sys

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

def readSolarSystem(verbose=False):
    """
    Read solar system

    Return:
    ------
    ElementTree object

    Example:
    -------
    >> SOLSYS=readSolarSystem()
    >> for planet in objectsList(SOLSYS,"planet"):
           planet.index=indexObject(planet)
           name=getObjectProperty(planet,"name","str")
           print name
    """
    import xml.etree.ElementTree as ET,urllib,gzip,io
    
    #READ SOLAR SYSTEM
    if verbose:print "Reading Solar System..."
    filename=DATADIR+SOLSYS_DIR+"SolarSystem.xml.gz"
    fl = open(filename,"rb")
    solsys=ET.parse(gzip.GzipFile(fileobj=io.BytesIO(fl.read())))
    fl.close()

    return solsys

SOLSYS=readSolarSystem()
def getSolSys(objname,propiedad,tipo="float",solsys=SOLSYS):
    """
    Get property of a Solar System object.

    Parameter:
    ---------
    objeto:
       String.  Name of the object.

    propiedad:
       String.  Name of property.

    tipo (optional):
       Type of property (float, int, str).

    Example:
    -------
    >> Mjup=getSolSys("Jupiter","mass")
    >> print Mjup
    1.899e+27
    """
    objeto=solsys.find(".//*[@name='%s']"%objname)
    if objeto is None:
        errorMsg("getSolSys","No object found with this name",
                 extra=objname)
    text=objeto.findtext(propiedad)
    exec("value=%s(text)"%tipo)
    return value

def readPlanetCatalogues(verbose=False):
    """
    Read confirmed planets and kepler candidates catalogues.

    Return:
    ------
    Tuple: kepler ElementTree object, confirmed planet ElementTree object

    Example:
    -------
    >> DB_KEPLER,DB_CONFIRMED=readPlanetCatalogues()
    >> for planet in objectsList(planets,"planet"):
           planet.index=indexObject(planet)
           name=getObjectProperty(planet,"name","str")
           print name
    """

    import xml.etree.ElementTree as ET,urllib,gzip,io
    
    #READ KEPLERS
    if verbose:print "Reading Exoplanets Catalogue: Kepler..."
    filename=DATADIR+OEC_DIR_GZ+"systems-kepler.xml.gz"
    fl = open(filename,"rb")
    keplers=ET.parse(gzip.GzipFile(fileobj=io.BytesIO(fl.read())))
    fl.close()

    #READ CONFIRMED
    if verbose:print "Reading Exoplanets Catalogue: Confirmed..."
    filename=DATADIR+OEC_DIR_GZ+"systems.xml.gz"
    fl = open(filename,"rb")
    confirmed=ET.parse(gzip.GzipFile(fileobj=io.BytesIO(fl.read())))
    fl.close()
    return keplers,confirmed

def getObjectProperty(objeto,propiedad,tipo):
    """
    Get property of a XML object (ElementTree).

    Parameters:
    ----------

    objeto:
        Object (ElementTree)

    propiedad:
        String.  Name of property.

    tipo:
        Type of property.  It should be the name of a valid "cast"
        routine (conversion from string to another type).  Normally
        used: float, int, str.

    Return:
    ------
    Tuple with property value and its items.

    Example:
    >> planet.index=indexObject(planet)
    >> Rp=getObjectProperty(planet,"mass","float")
    >> print Rp
    (1.31228, {'errorminus': 0.14581, 'errorplus': 0.14581})
    >> V=4*pi/3*Rp[0]**3

    """
    try:
        i=objeto.index.index(propiedad)
    except ValueError:
        return None,None
    except AttributeError:
        errorMsg("getObjectProperty","The object should be indexed first.")

    #Get property node
    prop=objeto.getchildren()[i]
    text=prop.text

    #Get value
    try:
        if not text is None:
            exec("value=%s(text)"%tipo)
        else:
            value=None
    except:
        errorMsg("getObjectProperty","Error when getting value of object property",
                 extra="Property = %s, Type = %s, Text = %s"%(propiedad,tipo,prop.text))

    #Item dictionary
    items=dict()

    #Check for other items
    i=0
    for item in prop.items():
        key=item[0]
        try:
            exec("items[key]=%s(item[1])"%tipo)
        except:
            items[key]=item[1]

    return value,items

def indexObject(objeto):
    """
    Index an object (ElementTree).  This routine extract the
    children name of a given node in an XML tree.

    Parameters:
    ----------
    objeto:
        Object (ElementTree)

    Returns:
    -------
    List of children names.
    """
    index=[]
    for prop in objeto.getchildren():
        label=prop.tag
        index+=[label]
    return index

def objectsList(db,node):
    """
    Return a list of objects in a XML database
    
    Parameters:
    ----------

    db:
       XML database (ElementTree)

    node:
       Name of node to list

    Returns:
    -------
    List of objects in database starting in 'node' (list of ElementTree).

    Example:
    -------
    for planet in objectsList(systems):
        print planet.findtext("name")
    """
    iterator=db.findall(".//%s"%node)
    return iterator

###################################################
#PRELOAD
###################################################

###################################################
#TEST
###################################################
if __name__=="__main__":
    print "Data Module."
