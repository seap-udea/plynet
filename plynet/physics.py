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
# Physics module
############################################################
from plynet import *
from plynet.numeric import *

############################################################
#BASIC REQUIRED PACKAGES
############################################################

############################################################
#LOAD CONFIGURATION
############################################################
loadConfiguration(BASEDIR+"/physics.cfg",locals())

############################################################
#ROUTINES
############################################################
def densitySphere(M,R):
    """
    Mean Density of an Spherical Object
    """
    return M/(4./3*np.pi*R**3)

def aKepler(P,M1,M2,UL=AU,UT=DAY,UM=MSUN):
    """
    P: in UT
    M1,M2: In UM
    
    Returns a in UL
    """
    a=(((P*UT)**2*GCONST*((M1+M2)*UM))/(4*PI**2))**(1./3.)/UL
    return a

def PKepler(a,M1,M2,UL=AU,UT=DAY,UM=MSUN):
    """
    P: in UT
    M1,M2: In UM
    
    Returns a in UL
    """
    P=np.sqrt((a*UL)**3/(GCONST*((M1+M2)*UM)/(4*PI**2)))/UT;
    return P

# ========================================
# BHZ ACCORDING TO MZCC
# ========================================
def seffHZ(Teff,crits=['recent venus','early mars'],Tsun=TSUN,Mp='1.0'):
    """
    Kopparapu et al., 2014
    """
    if Teff<2600:Teff=2600.0
    if Teff>7200:Teff=7200.0
    Tst=Teff-Tsun

    Seffs=[]
    for crit in crits:
        if crit=="runaway greenhouse":
            if Mp=='1.0':
                S=1.107
                a=1.332E-4;b=1.58E-8;c=-8.308E-12;d=-1.931E-15
            if Mp=='5.0':
                S=1.188
                a=1.433E-4;b=1.707E-8;c=-8.968E-12;d=-2.048E-15
            if Mp=='0.1':
                S=0.99
                a=1.209E-4;b=1.404E-8;c=-7.418E-12;d=-1.713E-15
        elif crit=="moist greenhouse":
            S=1.0146
            #SAME AS 2013
            a=8.1884E-5;b=1.9394E-9;c=-4.3618E-12;d=-6.8260E-16
        elif crit=="recent venus":
            #ALL MASSES ARE EQUARL
            S=1.776
            a=2.136E-4;b=2.533E-8;c=-1.332E-11;d=-3.097E-15
        elif crit=="maximum greenhouse":
            S=0.356
            a=6.171E-5;b=1.698E-9;c=-3.198E-12;d=-5.575E-16
        elif crit=="early mars":
            S=0.32
            a=5.547E-5;b=1.526E-9;c=-2.874E-12;d=-5.011E-16
        else:
            S=a=b=c=d=Tst=-1
        Seffs+=[S+a*Tst+b*Tst**2+c*Tst**3+d*Tst**4]
        
    if len(Seffs)==1:return Seffs[0]
    else:return Seffs

def alphaHZ(Teff,crit='recent venus',Tsun=TSUN,Mp='1.0'):
    """
    Weighting factors
    Kopparapu et al., 2014
    """
    if Teff<2600:Teff=2600.0
    if Teff>7200:Teff=7200.0
    Tst=Teff-Tsun

    if crit=="runaway greenhouse":
        if Mp=='1.0':
            S=1.107
            a=1.332E-4;b=1.58E-8;c=-8.308E-12;d=-1.931E-15
        if Mp=='5.0':
            S=1.188
            a=1.433E-4;b=1.707E-8;c=-8.968E-12;d=-2.048E-15
        if Mp=='0.1':
            S=0.99
            a=1.209E-4;b=1.404E-8;c=-7.418E-12;d=-1.713E-15
    elif crit=="moist greenhouse":
        S=1.0146
        #SAME AS 2013
        a=8.1884E-5;b=1.9394E-9;c=-4.3618E-12;d=-6.8260E-16
    elif crit=="recent venus":
        #ALL MASSES ARE EQUARL
        S=1.776
        a=2.136E-4;b=2.533E-8;c=-1.332E-11;d=-3.097E-15
    elif crit=="maximum greenhouse":
        S=0.356
        a=6.171E-5;b=1.698E-9;c=-3.198E-12;d=-5.575E-16
    elif crit=="early mars":
        S=0.32
        a=5.547E-5;b=1.526E-9;c=-2.874E-12;d=-5.011E-16
    else:
        S=a=b=c=d=Tst=-1

    l=np.sqrt(1.0/S)
    alpha=a*Tst+b*Tst**2+c*Tst**3+d*Tst**4
    return l,alpha

def cHZ(Ls,Teff,lin='recent venus',lout='early mars',Seff=seffHZ):
    """
    Circumstellar Habitable Zone limits by Kopparapu et al. (2014)

    L: In solar Units
    Teff: In K
    """
    if Ls<0 or Teff<0:
        raise Exception("Negative value in stellar properties")
    Seffin,Seffout=Seff(Teff,crits=[lin,lout])
    Seffsun=1.0
    lin=(Ls/Seffin)**0.5
    lout=(Ls/Seffout)**0.5
    aHZ=(Ls/Seffsun)**0.5
    return lin,aHZ,lout

def binaryFlux(q,Ls1=1.0,Ls2=1.0,rc1=0.1,rc2=0.1,D=1.0,qsgn=1):
    R1=np.sqrt(D**2+rc1**2+2*D*rc1*np.sin(q))
    R2=np.sqrt(D**2+rc2**2-2*D*rc2*np.sin(q))
    F=qsgn*(Ls1/R1**2+Ls2/R2**2)
    return F

def averageFlux(d,**args):
    args['D']=d
    intFlux=lambda x:binaryFlux(x,**args)
    F=integrate(intFlux,0.0,2*PI)[0]/(2*PI)
    return F

def pBHZ(q,Ls1,Ls2,Teffbin,abin,
         Seff=seffHZ,
         crits=['recent venus','early mars'],
         eeq=False,
         verbose=False):
    """
    P-type Binary Habitable Zone (pBHZ) according to Mason, Zuluaga et
    al. (2013)
    """

    if verbose:print "Input:",q,Ls1,Ls2,Teffbin,abin
    
    rc2=abin/(q+1)
    rc1=q*rc2
    args=dict(Ls1=Ls1,Ls2=Ls2,rc1=rc1,rc2=rc2)

    #EFFECTIVE FLUXES
    Seffin,Seffout=Seff(Teffbin,crits=crits)
    if verbose:print "Seffs:",Seffin,Seffout

    #INNER LIMIT
    AF=lambda x:averageFlux(x,**args)-Seffin
    #lin=newtonSol(AF,1.0)
    lin=brentqSol(AF,1.0E-3,100.0)
    limits=lin,

    #OUTER LIMIT
    AF=lambda x:averageFlux(x,**args)-Seffout
    #lout=newtonSol(AF,1.0)
    lout=brentqSol(AF,1.0E-3,500.0)
    limits+=lout,

    if eeq:
        #EARTH EQUIVALENT
        AF=lambda x:averageFlux(x,**args)-1.0
        #aeeq=newtonSol(AF,1.0)
        aeeq=brentqSol(AF,1.0E-3,100.0)
        limits+=aeeq,

    return limits

def ecl2eq(lamb,beta,eps):
    """
    Coordinate transformation.  Ecliptic to Equatiorial
    """
    delta=np.arcsin(np.sin(beta)*np.cos(eps)+\
                        np.cos(beta)*np.sin(eps)*np.sin(lamb))
    p=np.cos(beta)*np.cos(eps)*np.sin(lamb)-np.sin(beta)*np.sin(eps)
    q=np.cos(lamb)*np.cos(beta)
    alphac=np.arctan(p/q)*RAD

    alpha=alphac
    if p*q<0:
        if q<0:alpha=alphac+180
        else:alpha=alphac+360
    else:
        if (p+q)<0:alpha=alphac+180

    return alpha*DEG,delta

def eq2hor(alpha,delta,LST,phi):
    """
    Coordinate transformation: Equatorial to Horizontal
    """
    H=np.mod(LST*15.0*DEG-alpha,360*DEG)
    h=np.arcsin(np.sin(delta)*np.sin(phi)+\
                    np.cos(delta)*np.cos(phi)*np.cos(H))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            Ac=np.arccos((np.sin(delta)-np.sin(phi)*np.sin(h))/\
                             (np.cos(phi)*np.cos(h)))
    except:
        if phi>0:Ac=180*DEG
        else:Ac=0.0*DEG

    A=Ac
    if H<180*DEG:A=360*DEG-Ac
    return H,h,A

def ecl2hor(lamb,beta,eps,LST,phi):
    """
    Coordinate transformation: Ecliptic to Horizontal
    """
    alpha,delta=ecl2eq(lamb,beta,eps)
    H,h,A=eq2hor(alpha,delta,LST,phi)
    return H,h,A

def eccentricAnomaly(e,M):
    """
    Mikkola, 1991
    Code at: http://smallsats.org/2013/04/20/keplers-equation-iterative-and-non-iterative-solver-comparison/
    """
    Ecorr=0;Esgn=1.0
    if M>180*DEG:
        M=360.0*DEG-M
        Ecorr=360*DEG
        Esgn=-1.0

    if e==0:return Ecorr+Esgn*M

    a=(1-e)*3/(4*e+0.5);
    b=-M/(4*e+0.5);
    y=(b*b/4 +a*a*a/27)**0.5;
    x=(-0.5*b+y)**(1./3)-(0.5*b+y)**(1./3);
    w=x-0.078*x**5/(1 + e);
    E=M+e*(3*w-4*w**3);

    #NEWTON CORRECTION 1
    sE=np.sin(E)
    cE=np.cos(E)

    f=(E-e*sE-M);
    fd=1-e*cE;
    f2d=e*sE;
    f3d=-e*cE;
    f4d=e*sE;
    E=E-f/fd*(1+\
                  f*f2d/(2*fd*fd)+\
                  f*f*(3*f2d*f2d-fd*f3d)/(6*fd**4)+\
                  (10*fd*f2d*f3d-15*f2d**3-fd*fd*f4d)*\
                  f**3/(24*fd**6))

    #NEWTON CORRECTION 2
    f=(E-e*sE-M);
    fd=1-e*cE;
    f2d=e*sE;
    f3d=-e*cE;
    f4d=e*sE;
    E=E-f/fd*(1+\
                  f*f2d/(2*fd*fd)+\
                  f*f*(3*f2d*f2d-fd*f3d)/(6*fd**4)+\
                  (10*fd*f2d*f3d-15*f2d**3-fd**2*f4d)*\
                  f**3/(24*fd**6))

    E=Ecorr+Esgn*E
    return E

def orbitalPosition(n,a,e,t,w=0):
    M=n*t
    E=eccentricAnomaly(e,M)
    x=a*np.cos(E)-a*e
    y=a*(1-e**2)**0.5*sin(E)
    cw=np.cos(w)
    sw=np.sin(w)
    return np.array([x*cw-y*sw,x*sw+y*cw])

###################################################
#TEST
###################################################
if __name__=="__main__":
    print "Physics Module."
