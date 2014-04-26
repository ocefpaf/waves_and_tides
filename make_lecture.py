# -*- coding: utf-8 -*-
#
# make_lecture.py
#
# purpose:  Make slides, homework, and handout.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  20-Aug-2013
# modified: Fri 25 Apr 2014 10:04:41 PM BRT
#
# obs: Uses latexmk, pdflatex adn pandoc.
#

import os
from datetime import date
from tempfile import mktemp
from subprocess import check_call, PIPE, Popen

from docopt import docopt


__doc__ = """
Make lecture slides, handout and homework.

Usage:
    make_lecture (DIR) [--compile=DOC]
    make_lecture (-h | --help | --version)

Examples:
    make_lecture Aula_01 --compile=slides
    make_lecture Aula_01 --compile=handout
    make_lecture Aula_01 --compile=homework
    make_lecture Aula_01 --compile=all

Arguments:
  DIR      Lecture directory.

Options:
  -c --compile=DOC   slides, handout, homework or all [default: slides]
  --version   Show version.
  ---help     Show this screen.
"""

header = r"""
\usepackage{tikz}
\usepackage{lmodern}
\usepackage{fancybox}  % Box [shadowbox, fbox, doublebox, ovalbox, Ovalbox].
\usepackage{cancel}
\usepackage{textcomp}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{multimedia}
\usepackage[utf8]{inputenc}
\usepackage{amssymb,amsmath}
\usepackage{longtable,booktabs}

\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}} % partial derivatives
\renewcommand\mathfamilydefault{\rmdefault}
\setbeamertemplate{blocks}[rounded][shadow=true]

\usecolortheme[named=OliveGreen]{structure}

\usetheme{Madrid}

\useoutertheme{infolines}
\setbeamertemplate{items}[square]
\setbeamercolor{alerted text}{fg=Maroon}
\setbeamertemplate{navigation symbols}{}  % Remove lower navigation panel.

\usetikzlibrary{calc}
\definecolor{pbgray}{HTML}{575757}

\makeatletter
\def\progressbar@progressbar{}
\newcount\progressbar@tmpcounta
\newcount\progressbar@tmpcountb
\newdimen\progressbar@pbht
\newdimen\progressbar@pbwd
\newdimen\progressbar@tmpdim

\progressbar@pbwd=\linewidth
\progressbar@pbht=1pt

\def\progressbar@progressbar{
    \progressbar@tmpcounta=\insertframenumber
    \progressbar@tmpcountb=\inserttotalframenumber
    \progressbar@tmpdim=\progressbar@pbwd
    \multiply\progressbar@tmpdim by \progressbar@tmpcounta
    \divide\progressbar@tmpdim by \progressbar@tmpcountb

  \begin{tikzpicture}[very thin]
    \draw[pbgray!30,line width=\progressbar@pbht]
      (0pt, 0pt) -- ++ (\progressbar@pbwd,0pt);
    \draw[draw=none]  (\progressbar@pbwd,0pt) -- ++ (2pt,0pt);

    \draw[fill=pbgray!30,draw=pbgray]
       ( $ (\progressbar@tmpdim, \progressbar@pbht) + (0,1.5pt) $ )
       -- ++(60:3pt) -- ++(180:3pt) ;

    \node[draw=pbgray!30,text width=3.5em,align=center,inner sep=1pt,
      text=pbgray!70,anchor=east] at (0,0)
      {\insertframenumber/\inserttotalframenumber};
  \end{tikzpicture}
}

\addtobeamertemplate{headline}{}
{
  \begin{beamercolorbox}[wd=\paperwidth,ht=5ex,center,dp=1ex]{white}%
    \progressbar@progressbar
  \end{beamercolorbox}
}
\makeatother"""

dcls = dict(slides=r"\documentclass[14pt,xcolor=dvipsnames]{beamer}",
            handout=r"""\documentclass[handout,14pt,xcolor=dvipsnames]{beamer}
\usepackage{handoutWithNotes}
\pgfpagesuselayout{4 on 1 with notes}[a4paper,border shrink=5mm]""")


def compile_tex(lecture, d_type):
    with open(lecture, 'r') as f:
        lecture = f.read()

    latex_file = mktemp()
    with open(latex_file, 'w') as tex:
        tex.writelines('%s\n%s\n%s\n' % (dcls.get(d_type), header, lecture))

    os.chdir(DIRECTORY)
    output = '%s_OD_%s' % (fname, d_type)
    cmd = ('/usr/bin/latexmk',
           '-pdf',
           '-latexoption=-interaction=batchmode',
           '--jobname=%s' % output, latex_file)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode > 0:
        print(stderr.decode('utf-8'))
        print("Check the '%s/%s.%s' for erros." % (DIRECTORY, output, 'log'))
    else:  # Clean-up!
        try:
            extensions = ('snm', 'nav', 'fls', 'log', 'out', 'toc', 'aux',
                          'fdb_latexmk')
            for ext in extensions:
                filename = '%s/%s.%s' % (DIRECTORY, output, ext)
                os.unlink(filename)
        except FileNotFoundError:
            pass
    os.chdir('..')
    return None


def compile_md(homework='homework.md'):
    OPTS = ['--mathjax', '--smart', '--normalize', '--standalone',
            '--highlight-style=pygments']
    FROM = ['--from', 'markdown', homework]
    TO = ['--to', 'latex', '--output', '%s_homework.pdf' % fname]
    cmd = ['/home/filipe/bin/pandoc'] + OPTS + FROM + TO
    os.chdir(DIRECTORY)
    check_call(cmd)
    return None


if __name__ == '__main__':
    args = docopt(__doc__, version='0.2.0')

    # Globals.
    TODAY = date.today().strftime("%Y_%m_%d")
    DIRECTORY = os.path.abspath(args.get('DIR'))
    DIR = os.path.split(DIRECTORY)[-1]
    COMP = args.get('--compile')

    fname = '%s_OM_%s' % (DIR, TODAY)  # Output file names.

    if COMP == 'slides':
        compile_tex('%s/lecture.tex' % DIRECTORY, d_type='slides')
    elif COMP == 'handout':
        compile_tex('%s/lecture.tex' % DIRECTORY, d_type='handout')
    elif COMP == 'homework':
        compile_md()
    elif COMP == 'all':
        compile_tex('%s/lecture.tex' % DIRECTORY, d_type='slides')
        compile_tex('%s/lecture.tex' % DIRECTORY, d_type='handout')
        compile_md()
    else:
        raise ValueError("Unrecognized option --compile=%s" % COMP)
