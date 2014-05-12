
What's here?
============


|File           | Explanation                                                          |
|:--------------|----------------------------------------------------------------------|
|Makefile 		|Makefile for the markdown document                                    |
|contact-databases-for-abuse-handling.mkd|the main markdown document describing how to do contact lookups for CERTs |
|common/ 		|supporting .tex templates for generating a nice PDF out of the markdown document |
|img/ 			|supporting images for generating a nice PDF out of the markdown document |
|contactDB-pgp support.pptx|slides describing the contact lookup for CERTs project. |


How to build the document
=========================

```
make clean; make
```

Pre-requisites
==============

* pandoc
* macTeX (tested with MacTex as well as TexLive)

