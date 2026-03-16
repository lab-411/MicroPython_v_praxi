import os

CIRCUIT_MACROS_PATH = './cm'

def cm_compile(file_name, cm_data='', dpi=300):

    fp = open( file_name + '.ckt', 'w'); 
    fp.write(cm_data);
    fp.close()
        
    os.system( 'm4 -I %s pgf.m4  %s > data.dpc'%(CIRCUIT_MACROS_PATH, file_name+'.ckt') )
    os.system( 'dpic -g data.dpc > data.tex') 
    
    temp = r'''
    \documentclass{article}
    \usepackage{amsmath}
    \usepackage{pst-plot, pst-eps, tikz}
    \pagestyle{empty}

    \begin{document}
      \begin{TeXtoEPS}
        \input{data.tex}
      \end{TeXtoEPS}
    \end{document}
    '''

    f = open('template.tex', 'w' ) 
    f.write(temp)
    f.flush()
    f.close()
    
    os.system( 'latex template.tex > latex.log')   
    os.system( 'dvips -q* -E template.dvi -G0 -o %s > dvips.log '%(file_name+'.eps') )        
    os.system('gs -dSAFER -dEPSCrop -r600 -sDEVICE=pngalpha -dALLOWPSTRANSPARENCY -o %s %s > gs.log'%(file_name+'.png', file_name+'.eps'))
    
    os.system( 'rm *.dvi' )
    os.system( 'rm *.aux' )
    os.system( 'rm *.log' )
    os.system( 'rm *.tex' )
    os.system( 'rm *.eps' )
    os.system( 'rm *.dpc' )
    return file_name + '.ckt'
