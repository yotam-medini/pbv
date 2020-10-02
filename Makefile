#!/usr/bin/make -f

pbv.pdf: pbv.tex
	pdflatex pbv.tex

cover.pdf: cover.tex
	pdflatex cover.tex
