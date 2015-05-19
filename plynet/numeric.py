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
# Numerical module
############################################################
from plynet import *

############################################################
#BASIC REQUIRED PACKAGES
############################################################
import numpy as np
from scipy.optimize import newton as newtonSol,brentq as brentqSol 
from scipy.integrate import quad as integrate,odeint
from scipy.linalg import norm
from fractions import gcd

############################################################
#LOAD CONFIGURATION
############################################################
loadConfiguration(BASEDIR+"/numeric.cfg",locals())

############################################################
#ROUTINES
############################################################
def errorNormal(value,variables):
    """
    Calculate error for an algebraic formula depending on a set of
    normal variables
    
    Parameters:
    ----------
    value:
      Value of the function
    
    variables:

      List of tuples.  Each tuple content the value of each variable in
      the formula, the error and the exponent of the variable.
      
      Examples: 
         f = x y, variables=[(x,dx,1),(y,dy,1)]
         f = G M m / r^2, variables=[(M,dM,1),(m,dm,1),(r,dr,-2)]

    Return:
    ------
    Error

    Example:
    -------
    def func(x,y):
        f=x*y
        return f

    x=3.0;dx=0.1
    y=4.0;dy=0.1
    f=func(x,y)

    df=errorNormal(f,[(x,dx,1.0),(y,dy,1.0)])
    print "Normal: f = %f +/- %f"%(f,df)
    """
    toterror=0
    for var in variables:
        central=var[0]
        error=var[1]
        exponent=var[2]
        toterror+=(exponent*error/central)**2
    return value*toterror**0.5

def errorFunction(function,variables,N=1000,CL=70.0,options=dict()):
    """
    Calculate error for a complex formula assuming variables that
    follow a given distribution.
    
    Parameters:
    ----------
    function:
      Function.
    
    variables:

      List of tuplas.  Each tupla content the value of each variable,
      its prior distribution and the arguments of the prior
      distribution.
      
      Examples: 
         f(x,y)=x y
         Let's assume that x and y are distributed normally (normal=np.random.normal)

         variables=[(normal,(x,dx)),(normal,(y,dy))]

    N:
      Size of random sample used to calculate the error
      
    CL: 
      Confidence level in %.

    Return:
    ------
    fM:
       Median
       
    dfm:
       Inferior error (+CL/2)

    dfp:
       Superior error (+CL/2)

    fm:
       Error "average", i.e. fm=fM + (dfp-dfm)/2

    df:
       Average error, df=(dfm+dfp)/2

    Example:
    -------
    normal=np.random.normal
    def func(x,y):
        f=x*y
        return f

    x=3.0;dx=0.1
    y=4.0;dy=0.1
    f=func(x,y)

    fM,dfm,dfp,fm,df=errorFunction(func,
                                [(normal,(x,dx)),
                                 (normal,(y,dy))])
    print "Montecarlo: f = %f (median = %f) + %f - %f, %f +/- %f"%(f,fM,dfp,dfm,fm,df)
    """
    #GENERATE THE VALUES
    fs=[]
    for i in xrange(N):
        args=()
        for var in variables:
            dist=var[0]
            fargs=var[1]
            if dist is None or fargs[1]==0:
                x=fargs[0]
            else:
                x=dist(*fargs)
            args+=(x,)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                f=function(*args,**options)
        except:
            continue
        fs+=[f]

    fs=np.array(fs)
    fmed=np.percentile(fs,50.0)

    #DIVIDE VALUES
    fup=fs-fmed
    fup=fup[fup>=0]
    dfmax=np.percentile(fup,CL)

    flow=fmed-fs
    flow=flow[flow>=0]
    dfmin=np.percentile(flow,CL)

    return fmed,dfmin,dfmax,fmed+(dfmax-dfmin)/2,abs(dfmin+dfmax)/2

def dec2Sex(dec,ndig=2,sgnstr=True):
    """
    Convert from decimal to sexagesimal.
    """
    sgn=np.sign(dec)
    if sgnstr:
        if sgn>=0:sign="+"
        else:sign="-"
    else:sign=""
    adec=abs(dec)
    degrees=int(adec)
    rem=adec-degrees
    octa=rem*60
    minutes=int(octa)
    rem=octa-minutes
    octa=rem*60
    seconds=octa
    fmt="%%s%%02d:%%02d:%%02.%df"%ndig
    return fmt%(sign,degrees,minutes,seconds)

def leastCM(x,y):
    """
    Least Common Multiple
    """
    z=x*y/gcd(x,y)
    return z

def angDistance(beta1,beta2,lamb1,lamb2):
    """
    Calculate angular distance using the Haversine formula

    beta: Polar coordinate
    lamb: Azimuthal coordinate
    """
    deltabeta=beta2-beta1
    deltalamb=lamb2-lamb1
    arg=np.sin(deltabeta/2)**2+\
        np.cos(beta1)*np.cos(beta2)*np.sin(deltalamb/2)**2
    angdist=2*np.arcsin(np.sqrt(arg))
    return angdist

###################################################
#TEST
###################################################
if __name__=="__main__":
    print "Numeric Module."
