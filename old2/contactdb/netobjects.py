import models

def addCountry(cc, cc3, cname):
	"""
		@TODO ADD CHECK ON VALUES GIVEN
		len(cc) == 2
		len(cc3) == 3
		...
		TO BE MOVED TO ANOTHER CLASS!! - HERE NET OBJECTS ONLY - USE FOR DEBUG ;)
	"""
	cobj = models.Countrycode(cc=cc, cc3=cc3, country_name=cname)
	cobj.save()
	return



def addASN(asn, asname):
	print("DEBUG - in addASN =%d= =%s=" % (int(asn), asname))
	asnobj = models.ASN(asn=3, asname="test")
	print("DEBUG - asnobj created")
	asnobj.save()
	print("DEBUG - saved to DB")
	return

	
def addIP(range, asn):
	return