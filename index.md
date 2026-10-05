# <center> <font color='navy'>  <b> MicroPython na STM32 </b> </font> </center> 
## <center> <font color='brown'>  <b> Peter Fabo </b> </font>  </center> 

```{figure} ./img/logo.png
:width: 400px
:name: mp_0001
```


### <center> <font color='brown'>  <b> LAB - 411 Production </b> </font>  </center>   
### <center> <font color='brown'>  <b> Verzia 0.22, Október 2026 </b> </font>  </center>  
 

----------------

## Obsah 

%```{contents} Table of Contents
%:depth: 2
%```


```{toctree}
:titlesonly: True
:caption: Úvod
0010_uvod.md
0012_zaciname.md
0014_pouzitie.md
```

```{toctree}
:titlesonly: True
:caption: Elektronika
0020_terminologia.md
0022_zaklady.md
0024_signaly.md
0030_analog.md
0050_digital.md
```

```{toctree}
:titlesonly: True
:caption: Mikrokontrolér
0400_architektura.md
0410_programovanie.md
0420_filesystem.md
0440_library.md
```


```{toctree}
:titlesonly: True
:caption: Paralelný vstup a výstup
0100_gpio.md
```

```{toctree}
:titlesonly: True
:caption: Sériové zbernice
0200_usart.md
0250_spi.md
0150_i2c.md
```

```{toctree}
:titlesonly: True
:caption: Časovače
0300_timer.md
```

```{toctree}
:titlesonly: True
:caption: Displeje
./app_displej/0500_led_matrix.md
0255_spi_display_7219.md
0257_spi_display_12864.md
0158_i2c_display.md
```

```{toctree}
:titlesonly: True
:caption: Senzory
0156_i2c_lm92.md
0160_i2c_mems.md
```

```{toctree}
:titlesonly: True
:caption: Moduly
0505_funduino_01.md
0510_funduino_02.md
0590_prototyp.md
```

```{toctree}
:titlesonly: True
:caption: Platformy
0862_nucleo32.md
0860_nucleo64.md
0864_nucleo144.md
```


```{toctree}
:titlesonly: True
:caption: Prílohy
0710_install.md
0714_firmware.md
0716_editor.md
0720_jednotky_si.md
0730_znacky.md
```


## <font color='teal'> Vydal / Published by </font> 

    Vydalo v roku 2026 
    
    LAB - 411 Production
    Trenčín
    Slovensko
    

### <font color='brown'> Citovanie / How to cite</font>


## Licencie 

### <font color='brown'> Publikácia </font>  

Publikácia **MicroPython na STM32** je vydaná pod licenciou MIT

    Copyright © 2026 LAB-411 Team

    Permission is hereby granted, free of charge, to any person obtaining a copy 
    of this software and associated documentation files (the “Software”), to deal 
    in the Software without restriction, including without limitation the rights 
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
    copies of the Software, and to permit persons to whom the Software is furnished 
    to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all 
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
    A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
    OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


### <font color='brown'> MicroPython license information </font>  

    The MIT License (MIT)

    Copyright (c) 2013-2017 Damien P. George, and others

    Permission is hereby granted, free of charge, to any person obtaining a copy of this 
    software and associated documentation files (the “Software”), to deal in the Software 
    without restriction, including without limitation the rights to use, copy, modify, 
    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
    permit persons to whom the Software is furnished to do so, subject to the following 
    conditions:

    The above copyright notice and this permission notice shall be included in all copies 
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
    OR OTHER DEALINGS IN THE SOFTWARE.

### <font color='brown'> Preklady / Translations </font>

Preklady do iných jazykov sú možné v zmysle licencie MIT uvedenej nižšie. V zmysle nariadenia Európskeho parlamentu a Rady (EÚ) 2024/1689 z 13. júna 2024 autori tohoto diela **nepovolujú** využitie tohoto diela a ani jeho častí pre použitie v oblasti umelej inteligenice žiadnym aktuálnym ako aj budúcim spôsobom. 

Translations into other languages ​​are possible under the terms of the MIT license listed below. In accordance with Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024, the authors of this work **do not** authorize the use of this work or any part of it for use in the field of artificial intelligence in any current or future manner.


### <font color='brown'> Použité programové vybavenie / Software </font> 

Publikované na platforme *Sphinx* s využitím jazyka *MyST Markdown*, prostredia *CircuitMacros* a programovacieho jazyka *Python* v znení licencií uvedených nižšie.

Published on the *Sphinx* platform using the *MyST Markdown* language, the *CircuitMacros* environment, and the *Python* programming language under the terms of the licenses listed below.

Licencia k distribúcii programu **CircuitMacros**


    * Circuit_macros Version 10.9, copyright (c) 2025 J. D. Aplevich under     *
    * the LaTeX Project Public Licence in file Licence.txt. The files of       *
    * this distribution may be redistributed or modified provided that this    *
    * copyright notice is included and provided that modifications are clearly *
    * marked to distinguish them from this distribution.  There is no warranty *
    * whatsoever for these files.
    

Licencia k distribúcii programu **Sphinx**

    Copyright (c) 2007-2025 by the Sphinx team (see AUTHORS file). All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, 
    are permitted provided that the following conditions are met:

        Redistributions of source code must retain the above copyright notice, this list 
        of conditions and the following disclaimer.
        Redistributions in binary form must reproduce the above copyright notice, this list 
        of conditions and the following disclaimer in the documentation and/or other 
        materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
    SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF 
    THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Citácia **MyST Markdown**

    Rowan Cockett, Franklin Koch, Steve Purves, Angus Hollands, Yuxi Wang, Chris Holdgraf, 
    Dylan Grandmont, Stefan van der Walt, Andrea, Jan-Hendrik Müller, Spencer Lyon, 
    Cristian Le, Jim Madge, Thierry Parmentelat, wwx, Sugan Reden, Yuanhao Geng, Ryan Lovett, 
    Mikkel Roald-Arbøl,Nicolas M. Thiéry. 
    (2025). jupyter-book/mystmd: mystmd@1.6.0. Zenodo. 10.5281/ZENODO.14805610
    
    
## <font color='teal'> Titulný obrázok </font> 

    https://openclipart.org
    

