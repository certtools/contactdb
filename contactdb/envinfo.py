'''
Created on Mar 27, 2013

@author: david
'''

import models
import sys
import traceback

def addSource(srcname, srcreliability):
    """
        @TODO: add error checking and stricter code
        -- USE TO TEST / PROTOTYPE
    """
    print("ADD SOURCE CALLED")
    try:
        print("in try")
        sobj = models.Source(name="azerty")
        print("object created")
        sobj.save()
        print("object saved")
    except:
        e = sys.exc_info()[0]
        tb = sys.exc_info()[2]
        print("DEBUG: IN ADD SOURCE EXCEPTION!! %s" % (e))
        traceback.print_tb(tb)
    return
