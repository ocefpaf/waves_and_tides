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

LATEXMK=/usr/bin/latexmk
PANDOC=/home/filipe/bin/pandoc

DIR=$1
slides=$(mktemp --dry-run)  # Slides.
handouts=$(mktemp --dry-run)  # Handouts.

datestring=$(date +"%d_%b_%Y")

cat common/slides.tex common/header.tex ${DIR}/lecture.tex > $slides
cat common/handouts.tex common/header.tex ${DIR}/lecture.tex > $handouts

OPTION="--mathjax --smart --normalize --standalone \
        --highlight-style=pygments --webtex"
FROM="--from markdown homework.md"
DOCX="--to html --output ${datestring}_OM_homework.html"
HTML="--to docx --output ${datestring}_OM_homework.docx"
LATEX="--to latex --output ${datestring}_OM_homework.pdf"

pushd ${DIR}
    OPTS="-pdf -latexoption=-interaction=batchmode"
    # Slides.
    $LATEXMK $OPTS --jobname=${datestring}_OM_slides $slides

    # Handouts.
    $LATEXMK $OPTS --jobname=${datestring}_OM_handouts $handouts

    # Homework.
    $PANDOC $OPTION $FROM $LATEX

    # Clean-up.
    rm *.snm *.nav *.fdb_latexmk *.fls *.log *.out *.toc *.aux
popd
