#!/bin/bash
#
# compile.sh
#
# purpose:  Make slides, homework, and handout.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  09-Aug-2013
# modified: Sun 18 Aug 2013 12:44:17 PM BRT
#
# obs: the only argument is the directory with a lecture.tex file
# (without header and document class) and a homework.md file.
#


DIR=$1  # Lecture directory.

if [ $# -eq 1 ] ; then
    ALL=FALSE
elif [ $2 == "all" ] ; then
    ALL=TRUE
else
    echo "Unrecognized input parameters.  Enter directory and compile options (all or lecture)."
    exit 1
fi


fname=$(date +"%Y_%m_%d")_OM_$(basename ${DIR}) # Output file names.

# Temp latex files.
slides=$(mktemp --dry-run)
handouts=$(mktemp --dry-run)

# Options.
LATEXMK=/usr/bin/latexmk
OPTS="-pdf -latexoption=-interaction=batchmode"

PANDOC=/home/filipe/bin/pandoc
OPTION="--mathjax --smart --normalize --standalone --highlight-style=pygments"
FROM="--from markdown homework.md"
LATEX="--to latex --output ${fname}_Lista.pdf"

cat common/slides.tex common/header.tex ${DIR}/lecture.tex > $slides
cat common/handouts.tex common/header.tex ${DIR}/lecture.tex > $handouts

pushd ${DIR}
    $LATEXMK $OPTS --jobname=${fname}_Slides $slides  # Slides.
    if [ $ALL == "TRUE" ] ; then
        $LATEXMK $OPTS --jobname=${fname}_Notas $handouts  # Handouts.
        $PANDOC $OPTION $FROM $LATEX  # Homework.
    fi
        rm *.snm *.nav *.fdb_latexmk *.fls *.log *.out *.toc *.aux  # Clean-up.
popd
