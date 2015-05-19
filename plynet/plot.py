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
from matplotlib import use
use('Agg')
from matplotlib import colors,ticker,patches,pylab as plt
from matplotlib.pyplot import cm
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy

############################################################
#LOAD CONFIGURATION
############################################################
loadConfiguration(BASEDIR+"/plot.cfg",locals())

############################################################
#ROUTINES
############################################################
def saveFig(filename,watermark="plynet",watermarkpos="outer",dxw=0.01,dyw=0.01,va='top'):
    """
    Save figure with a watermark.
    """
    ax=plt.gca()

    #SAVE WATERMARK
    if watermarkpos=='inner':
        xw=1-dxw
        yw=1-dyw
        ha='right'
    if watermarkpos=='outer':
        xw=1+dxw
        yw=1+dyw
        ha='left'

    font=FontProperties().copy()
    font.set_family("serif")
    ax.text(xw,yw,watermark,
            horizontalalignment=ha,
            verticalalignment=va,
            rotation=90,color='b',alpha=0.3,fontsize=12,
            fontproperties=font,
            transform=ax.transAxes)

    plt.savefig(filename)

def offSet(dx,dy):
    """
    Place a text offset from the nominal coordinates.  To be used with
    option transform.

    Example:
    =======
    ax.text(0.5,0.5,"Text",transform=offet(5,-5)
    """
    fig=plt.gcf()
    ax=fig.gca()
    toff=offset_copy(ax.transData,fig=fig,
                     x=dx,y=dy,units='dots')
    return toff

def plotError(ax,xmat,ymat,**args):

    # Options
    argplot=dict()
    argplot.update(args)
    argerr=dict()
    argerr.update(args)
    argerr.update(markersize=0,linestyle="none")

    xav=xmat[:,0]+(abs(xmat[:,1])-abs(xmat[:,2]))/2
    yav=ymat[:,0]+(abs(ymat[:,1])-abs(ymat[:,2]))/2
    dx=(abs(xmat[:,1])+abs(xmat[:,2]))/2
    dy=(abs(ymat[:,1])+abs(ymat[:,2]))/2

    # Plot points
    ax.plot(xmat[:,0],ymat[:,0],**argplot)

    # Plot x-error
    ax.errorbar(xav,ymat[:,0],xerr=dx,**argerr)

    # Plot y-error
    ax.errorbar(xmat[:,0],yav,yerr=dy,**argerr)

def plotLabels(ax,texts,xs,ys,**args):
    """
    Put labels to a set of data points

    Parameters:
    ----------
    ax: axis.
    texts: List of strings.
    xs: List of abcisa values.
    ys: List of ordinate values.
    """
    
    # Ranges
    xmin,xmax=ax.get_xlim()
    ymin,ymax=ax.get_ylim()

    for i in xrange(len(texts)):

        # Exclude labels for points out of the plot ranges
        if ((xs[i]-xmin)*(xs[i]-xmax)>0) or\
                ((ys[i]-ymin)*(ys[i]-ymax)>0):continue

        # Plot labels
        ax.text(xs[i],ys[i],str(texts[i]),**args)

def customColor(value,cmap=cm.gray,minval=0,maxval=1):
    """
    Calculate a custom color from a given value 
    """
    f=(value-minval)
    if f<0:f=0
    if f>(maxval-minval):f=0.99*(maxval-minval)
    fn=f/(maxval-minval)

    #print value,f,fn

    color=cmap(fn)
    return color

###################################################
#TEST
###################################################
if __name__=="__main__":
    print "Plot Module."
