#pdf1:
#	./update-metadata-for-gitinfo
#	#pandoc -f markdown_github -o notes.pdf notes.md	

all: contact-databases-for-abuse-handling.pdf

latex:	contact-databases-for-abuse-handling.tex

contact-databases-for-abuse-handling.tex: contact-databases-for-abuse-handling.mkd
	pandoc  -N --listings -T "Contact database for IT security incident handling" -s -f markdown_github+pandoc_title_block+pipe_tables --toc -t latex -o contact-databases-for-abuse-handling.tex contact-databases-for-abuse-handling.mkd
	#pandoc  -N --listings -T "Contact database for IT security incident handling" -s -f markdown_github+pandoc_title_block+pipe_tables --toc -o contact-databases-for-abuse-handling.pdf contact-databases-for-abuse-handling.mkd

contact-databases-for-abuse-handling.pdf: contact-databases-for-abuse-handling.tex
	# add the proper stylesheets
	cat styleheader.tex > r
	tail -n +2 contact-databases-for-abuse-handling.tex  >> r
	mv r contact-databases-for-abuse-handling.tex
	# compute version info
	./update-metadata-for-gitinfo
	# update the toc
	pdflatex contact-databases-for-abuse-handling.tex
	pdflatex contact-databases-for-abuse-handling.tex

clean: 
	rm -f contact-databases-for-abuse-handling.pdf contact-databases-for-abuse-handling.tex contact-databases-for-abuse-handling.log contact-databases-for-abuse-handling.out contact-databases-for-abuse-handling.aux contact-databases-for-abuse-handling.toc
