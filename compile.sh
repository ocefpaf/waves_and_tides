#!/bin/bash
#
# compile.sh
#
# purpose:  Make slides, homework, and handout.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  09-Aug-2013
# modified: Sun 11 Aug 2013 07:24:32 PM BRT
#
# obs:
#

DIR=$1
slides=$(mktemp --dry-run)  # Slides.
handouts=$(mktemp --dry-run)  # Handouts.

cat slides.tex header.tex ${DIR}/lecture.tex > $slides
cat handouts.tex header.tex ${DIR}/lecture.tex > $handouts

OPTS="-pdf -latexoption=-interaction=batchmode"
pushd ${DIR}
    \latexmk $OPTS --jobname=slides $slides
    \latexmk $OPTS --jobname=handouts $handouts
    rm *.snm *.nav *.fdb_latexmk *.fls *.log *.out *.toc *.aux
popd

# Homework.
OPTION="--mathjax --smart --normalize --standalone --highlight-style=pygments --webtex"
FROM="--from markdown ${DIR}/homework.md"
DOCX="--to html --output ${DIR}/homework.html"
HTML="--to docx --output ${DIR}/homework.docx"
LATEX="--to latex --output ${DIR}/homework.pdf"

#pandoc $OPTION $FROM $HTML
#pandoc $OPTION $FROM $DOCX
pandoc $OPTION $FROM $LATEX
