---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

% #   <font color='#4B9DA9'> level 1 </font>
% ##  <font color='#547792'> level 2 </font>
% ### <font color='#E37434'> level 3 </font>
% {dropdown} <font color='#84B179'> Text </font>



# <font color='#4B9DA9'> Tranzistor </font>


* vlastnosti
* charakteristiky
* SE, SC-zdroj prúdu, zosilovač, výpočet
* základné zapojenia, prúdové zrkadlo, diferenciálny zosilovač
* typy, puzdra


%https://smhk.net/note/2023/11/plantuml-in-sphinx-using-myst-and-gitlab/
%https://docs.gitlab.com/administration/integration/plantuml/
%https://pypi.org/project/sphinxcontrib-plantuml/
%https://github.com/sphinx-contrib/plantuml/

You can specify height, width, scale and align: {numref}`acd`,



```{uml}
:caption: Caption with **bold** and *italic*
:name: acd
:align: center
:scale: 100%

clock   "Clock_0"   as C0 with period 50
clock   "Clock_1"   as C1 with period 50 pulse 25 offset 25
binary  "Binary"  as B
concise "Concise" as C
rectangle "Rectangle" as Re
robust  "Robust"  as R
analog  "Analog"  as A


@0
  C is Idle
  R is Idle
  Re is Idle
  A is 0

@100
B is high
C is Waiting
Re is Waiting
R is Processing
A is 3

@300
R is Waiting
A is 1
```

%```{eval-rst}
%.. uml::
%
%  @startuml
%  Bob -> Alice : hello
%  @enduml
%```



