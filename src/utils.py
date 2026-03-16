'''
Utility pre pouzitie skriptov CircuitMacro v jupyter-book

Historia
220422  - doplnenie konverziu rad dpic prikladov
        - upravy utilit pre konverziu pomocou pycirkuit
240616  - uprava cesty pre zdielane kniznice v owncloud 
240830  - doplnenia a upravy
251125  - upravy pre pouzitie s TIKZ
'''

#=======================================================================
# template - header
# template pre zahlavie suboru, predpoklada sa pouzitie z notebooku,
# ktory je v nadradenom adresari

cm_start = r'''
.PS
pi=3.14159265359
                        # parametre z PIC (resp. GNU PIC)
scale = 2.54            # cm - jednotka pre obrazok
maxpswid = 30           # rozmery obrazku
maxpsht = 30            # 30 x 30cm, default je 8.5x11 inch
cct_init                # inicializacia lokalnych premennych

arrowwid  = 0.127       # parametre sipok - sirka
arrowht = 0.254         # dlzka

'''


# template - footer
cm_end = r'''
.PE
'''

#======================================================================
import os

def cm_compile(file_name, cm_data='', dpi=300):
    '''
    Konverzia textoveho retazcu s CircuitMacros na obrazok PNG.
    '''
    
    # kontrola home directory
    # vsetky bunky v jednom *.md subore pouzivaju jednu instanciu pythonu
    # osetrenie na zmenu adresaru pri opakovanom volani funkcie
    wd =  os.getcwd()
    q = wd.split('/')
    if(q[-1] != 'src'):
        os.chdir('./src/')
        
    fp = open( file_name + '.ckt', 'w'); 
    fp.write(cm_start + cm_data + cm_end);
    fp.close()
        
    CIRCUIT_MACROS_PATH = './cm'
    
    # TIKZ 
    os.system( 'm4 -I %s pgf.m4  %s > data.dpc'%(CIRCUIT_MACROS_PATH, file_name+'.ckt') )
    # DPIC
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
    
    # LATEX
    os.system( 'latex template.tex > latex.log')   
    
    # DVIPS
    os.system( 'dvips -q* -E template.dvi -G0 -o %s > dvips.log '%(file_name+'.eps') )
    #print('DVIPS')
    #os.system( 'dvips -E  template.dvi -G0 -o %s  '%(file_name+'.eps') )
    
    os.system('gs -dSAFER -dEPSCrop -r600 -sDEVICE=pngalpha -dALLOWPSTRANSPARENCY -o %s %s > gs.log'%(file_name+'.png', file_name+'.eps'))
    
    os.system( 'rm *.dvi' )
    os.system( 'rm *.aux' )
    os.system( 'rm *.log' )
    os.system( 'rm *.tex' )
    os.system( 'rm *.eps' )
    os.system( 'rm *.dpc' )
    return file_name + '.ckt'
    
