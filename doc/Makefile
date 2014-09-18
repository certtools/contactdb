#pdf1:
#	./update-metadata-for-gitinfo
#	#pandoc -f markdown_github -o notes.pdf notes.md	

all: datasets.pdf

latex:	datasets.tex

datasets.tex: datasets.mkd
	pandoc  -N --listings -T "Abuse Contact datasets for IT security incident handling" -s -f markdown_github+implicit_figures+pandoc_title_block+table_captions+multiline_tables --toc -t latex -o datasets.tex datasets.mkd
	#pandoc  -N --listings -T "Contact database for IT security incident handling" -s -f markdown_github+pandoc_title_block+pipe_tables --toc -o datasets.pdf datasets.mkd

datasets.pdf: datasets.tex
	# add the proper stylesheets
	cat styleheader.tex > r
	tail -n +2 datasets.tex  >> r
	mv r datasets.tex
	# compute version info
	./update-metadata-for-gitinfo
	# update the toc
	pdflatex datasets.tex
	pdflatex datasets.tex

clean: 
	rm -f datasets.pdf datasets.tex datasets.log datasets.out datasets.aux datasets.toc r
