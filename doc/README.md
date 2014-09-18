
What's here?
============


|File           | Explanation                                                          |
|:--------------|----------------------------------------------------------------------|
|Makefile 		|Makefile for the markdown document                                    |
|contact-databases-for-abuse-handling.mkd| An overview of all datasets which contain abuse contat lookup data |
|abuse-lookups.mkd| A proposed mechanism for generic abuse contact lookups|
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
or
* TexLive (Linux)
or a similar Tex distribution under Windows
