#!/bin/bash

echo '% LaTeX template file
\documentclass{article}
\usepackage{amsmath}
\usepackage{pst-plot, pst-eps, tikz}
\pagestyle{empty}

\begin{document}
  \begin{TeXtoEPS}
    \input{data.tex}
  \end{TeXtoEPS}

\end{document}' > template.tex

# cesta ku M4 knizniciam CircuitMacros (libcct.m4 ... )
CIRCUIT_MACROS='./cm/'

# expadovanie makier do formatu TIKZ
m4 -I $CIRCUIT_MACROS pgf.m4  $1 | dpic -g > data.tex

# kompilacia latex suboru
latex template.tex > latex.log
dvips -q* -E template.dvi -G0 -o $(basename $1 .ckt).eps > dvips.log

# konverzia *.eps -> *.png, parameter r-rozlisenie v dpi
gs -dSAFER -dEPSCrop -r600 -sDEVICE=pngalpha -dALLOWPSTRANSPARENCY -o $(basename $1 .ckt).png $(basename $1 .ckt).eps > gs.log

# zmazanie docasnych suborov
rm dvips.log
rm latex.log
rm $(basename $1 .ckt).eps
rm data.tex
rm template.tex
rm template.dvi
rm template.aux
rm template.log
