#!/usr/bin/make -f

.DELETE_ON_ERROR:

pbv.pdf: pbv.tex
	pdflatex pbv.tex

cover.pdf: cover.tex
	pdflatex cover.tex
