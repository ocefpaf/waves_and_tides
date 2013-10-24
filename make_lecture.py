# -*- coding: utf-8 -*-
#
# make_lecture.py
#
# purpose:  Make slides, homework, and handout.
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  20-Aug-2013
# modified: Wed 23 Oct 2013 09:53:41 PM BRST
#
# obs:
#

import os
import subprocess
from datetime import date
from tempfile import mktemp
from cStringIO import StringIO

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

header = r"""% Packages.
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

% Partial.
\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}} % partial derivatives

% Template.
\setbeamertemplate{blocks}[rounded][shadow=true]

% See http://goo.gl/p0Phn for other colors.
\usecolortheme[named=OliveGreen]{structure}

% See deic.uab.es/~iblanes/beamer_gallery/index_by_theme.html for other themes.
\usetheme{Madrid}

% Specify other colors and options as required.
\useoutertheme{infolines}  % Add info lines at the bottom.
\setbeamertemplate{items}[square]
\setbeamercolor{alerted text}{fg=Maroon}
\setbeamertemplate{navigation symbols}{}  % Remove lower navigation panel.

% Progress bar.
\usetikzlibrary{calc}
\definecolor{pbgray}{HTML}{575757}  % Background color for the progress bar.

\makeatletter
\def\progressbar@progressbar{}  % Progress bar.
\newcount\progressbar@tmpcounta  % Auxiliary counter.
\newcount\progressbar@tmpcountb  % Auxiliary counter.
\newdimen\progressbar@pbht  % Progressbar height.
\newdimen\progressbar@pbwd  % Progressbar width.
\newdimen\progressbar@tmpdim  % Auxiliary dimension.

\progressbar@pbwd=\linewidth
\progressbar@pbht=1pt

% Progress bar.
\def\progressbar@progressbar{%

    \progressbar@tmpcounta=\insertframenumber
    \progressbar@tmpcountb=\inserttotalframenumber
    \progressbar@tmpdim=\progressbar@pbwd
    \multiply\progressbar@tmpdim by \progressbar@tmpcounta
    \divide\progressbar@tmpdim by \progressbar@tmpcountb

  \begin{tikzpicture}[very thin]
    \draw[pbgray!30,line width=\progressbar@pbht]
      (0pt, 0pt) -- ++ (\progressbar@pbwd,0pt);
    \draw[draw=none]  (\progressbar@pbwd,0pt) -- ++ (2pt,0pt);

    \draw[fill=pbgray!30,draw=pbgray] %
       ( $ (\progressbar@tmpdim, \progressbar@pbht) + (0,1.5pt) $ ) -- ++(60:3pt) -- ++(180:3pt) ;

    \node[draw=pbgray!30,text width=3.5em,align=center,inner sep=1pt,
      text=pbgray!70,anchor=east] at (0,0) {\insertframenumber/\inserttotalframenumber};
  \end{tikzpicture}
}

\addtobeamertemplate{headline}{}
{
  \begin{beamercolorbox}[wd=\paperwidth,ht=5ex,center,dp=1ex]{white}%
    \progressbar@progressbar
  \end{beamercolorbox}
}
\makeatother"""

dclass = dict(slides=r"\documentclass[14pt,xcolor=dvipsnames]{beamer}",
              handout=r"""\documentclass[handout,14pt,xcolor=dvipsnames]{beamer}
\usepackage{handoutWithNotes}
\pgfpagesuselayout{4 on 1 with notes}[a4paper,border shrink=5mm]""")


def compile_tex(lecture, d_type):
    with open(lecture, 'r') as f:
        lecture = f.read()

    latex_file = mktemp()
    with open(latex_file, 'w') as tex:
        tex.writelines('%s\n%s\n%s\n' % (dclass.get(d_type), header, lecture))

    output = '%s_%s' % (fname, d_type)
    cmd = ('/usr/bin/latexmk', '-pdf',
            '-latexoption=-interaction=batchmode',
            '--jobname=%s' % output, latex_file)
    os.chdir(DIRECTORY)
    subprocess.check_call(cmd)

    # Clean-up.
    extensions = ('snm', 'nav', 'fls', 'log', 'out', 'toc', 'aux',
                  'fdb_latexmk')
    map(os.unlink, ['%s/%s.%s' % (DIRECTORY, output, ext) for
                    ext in extensions])
    return None


def compile_md(homework='homework.md'):
    OPTS = ['--mathjax', '--smart', '--normalize', '--standalone',
            '--highlight-style=pygments']
    FROM = ['--from', 'markdown', homework]
    TO = ['--to', 'latex', '--output', '%s_homework.pdf' % fname]
    cmd = ['/home/filipe/bin/pandoc'] +  OPTS + FROM + TO
    os.chdir(DIRECTORY)
    subprocess.check_call(cmd)
    return None


if __name__ == '__main__':
    args = docopt(__doc__, version='0.1.0')

    # Globals.
    TODAY = date.today().strftime("%Y_%m_%d")
    DIRECTORY = os.path.abspath(args.get('DIR'))
    DIR = os.path.split(DIRECTORY)[-1]
    COMP = args.get('--compile')

    fname = '%s_OM_%s' % (TODAY, DIR)  # Output file names.

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
