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

# MicroPython  

S narastajúcim výkonom mikrokontrolérov sa v súčasnom období posúvajú možnosti ich využitia aj do oblastí, ktoré boli pred pár rokmi vyhradené výkonným počítačom alebo výpočtovým strediskám. Z relatívne jednoduchých čipov, často pozostávajúcich len z MCU a nevyhnutných periférií, primárne určených pre obsluhu a jednoduché spracovanie dát zo senzorov sa vyvinuli komplexné zariadenia obsahujúce priamo na čipe univerzálne komponenty potrebné pre tvorbu kompaktného a cenovo veľmi prijateľného systému riadenia, zberu, spracovania a transportu dát zo senzorov. S vývojom technických prostriedkov narastá aj komplexnosť programového vybavenie, na ktoré sú kladené vysoké požiadavky na jeho kvalitu a stabilitu, zariadenia často musia pracovať v ťažkých a komplikovaných podmienkach, bez možnosti údržby počas celej doby ich životnosti.


##  Vývoj aplikácií  

Vývoj typickej aplikácie pozostáva z dvoch častí

* Vývoj spojený s obsluhou technických prostriedkov - vstupných zariadení a senzorov, zobrazovacích a signalizačných prvkov a výstupných zariadení. Tento môže mať niekoľko úrovní - od jednoduchého pripojenia štandardného prvku ku normalizovanému rozhraniu (I2C, SPI, … ) a tvorbe príslušného API pre jeho obsluhu až po vývoj vlastného špecializovaného senzora alebo výstupného zariadenia s firmware, komunikačným rozhraním, implementáciou a spracovaním dát a unikátnym API.

* Vývoj spojený s vlastnou aplikáciou - od jednoduchej komunikačnej aplikácie až po rozsiahly systém komunikujúci cez Internet. Pretože individuálny vývoj od základu je náročný a zdĺhavý, pre implementácie IoT aplikácií bolo v poslednom období vytvorených množstvo operačných systémov, typickým predstaviteľom je projekt Zephyr, ktorý je portovaný na viacej ako 800 platforiem, pričom pre každú platformu má implementovanú obsluhu základných periférií. Súčasťou je mikrokernel alebo nanokoernel v závislosti od výkonu zariadení, podporuje multithreading a non-preemptive a preemptive plánovač (scheduling), programovacím jazykom je C a C++.

Vývoj programového vybavenia je zvyčajne realizovaný v programovacích jazykoch umožňujúcich jednoduchý prístup k perifériím mikrokontroléra, ako je C, C++, Assembler. Použitie týchto jazukov garantuje vysokú efektivitu programového vybavenia, na druhej strane vyžaduje špeciálne prostriedky podporované samotným mikrokontrolérom pre ladenie kódu a hladanie chýb.

Je zrejmé, že vývoj aplikácie vyžaduje tvorbu a používanie vývojových nástrojov, ktorých príprava a odladenie môže v závislosti od rozsahu trvať nezanedbateľnú dobu. Jednou z možností, ako túto etapu zjednodušiť, je použitie flexibilného univerzálneho nástroja, umožnujúceho interaktívnu prácu a testovanie jednotlivých častí zariadenia.

##  Oblasť použitia 

```Python``` je všeobecne pokladaný za univerzálny programovací jazyk vysokej úrovne ďaleko vzdialený od hardware. ```MicropPython``` je prepisom referenčnej implementácie CPython jazyka ```Python``` pôvodne pre platformu [pyboard](https://github.com/micropython/micropython) s podporou integrovaných periférií.

```{figure} ./img/pyboard.jpg
:width: 600px
:name: mp_0010a

Logo projektu MicropPython a platforma pyboard.
```


Implementácia je portovaná pre rôzne cielové platformy, je škálovateľná a open-source. O jeho popularite svedčí aj to, že na githube v súčasnej dobe existuje asi 2000 rôznych vetiev (fork) s rôznymi modifikáciami a úpravami pre rôzne vývojové a experimentálne dosky. Z aplikačného hľadiska je použitie MicroPython jednoduché, ako firmware sa nahrá štandardným programovacím software pre konkrétny typ mikrokontroléra do jeho flash pamäte a zvyčajne prostredníctvom emulácie sériového rozhrania komunikuje s terminálovou aplikáciu v počítači.

Oblasť použitia môžeme rozdeliť do niekokých kategórií

* Výuka a vzdelávanie, ```MicroPython``` poskytuje možnosť interaktívnej komunikácie s mikrokontrolérom v slučke REPL (Read–Eval–Print Loop). S priamym prístupom k perifériám mikrokotroléra cez akýkoľvek terminálový emulátor bez potreby písania a vysvetlovania množstva kódu potrebného na inicializáciu a elementárnu komunikáciu je možné na veľkom množstve podporovaných dosák vysvetliť študentom základné princípy zberu a spracovania dát, naviac v jednoduchom programovacom jazyku.

* Vývoj a testovanie periférií a senzorov. ```MicroPython``` poskytuje odladené a vyskúšané referenčné implementácie rozhraní mikrokontrolérov, čím vývojára zbavuje potreby implementácie celej vertikálnej štruktúry spojenej s komunikáciou a riadením periférneho zariadenia. Moderné integrované periférie komunikujúce cez sériové rozhrania (**I2C**, **SPI**, **CAN** …) sú riadené zápisom a čítaním hodnôt často z desiatok rôznych registrov, s individuálnym významom jednotlivých bitov a vzájomným previazaním hodnôt. Priamym interaktívnym prístupom v jednoduchom a populárnom jazyku k registrom zariadenia je možné jednoducho overiť funkciu periférií, vyvinúť a odladiť príslušný hardware a algoritmy pre riadenie a zber dát zo zariadenia. Vďaka abstrakcii hardware a univerzálnosti implementácie je možné pre vývoj využiť aj iné platformy, ako bude cieľová a to bez potreby detailnej znalosti jej programovania.

* Monitorovací a konfiguračný nástroj pre komplexné aplikácie. Rozsiahle aplikácie na výkonných mikrokontroléroch a **FPGA** obsahujú často implementáciu nezávislých pomocných prostriedkov pre monitorovanie a nastavovanie parametrov systému, pri **FPGA** to býva často SW implementácia niektorého z malých mikroprocesorov (8051, Z80 …), pomocou programu pre tieto mikroprocesory je možné sledovať a nastavovať parametre a konfiguráciu systému. Prvé pokusy s implementáciou MicroPython-u na FPGA ukazujú perspektívu daľšieho vývoja. V oblasti operačných systémov existuje experimentálny port MicroPython pre monitorovanie a nastavovanie parametrov kernelu Linuxu.


## Platforma STM32 

Rodina mikrokontrolérov triedy **STM32** zahŕňa triedu populárnych mikrokontrolérov obsahujúcich široké spektrum typov líšiacich sa výkonom, pamäťou perifériami a možnosťami optimalizácie spotreby. Vývoj aplikácií je podporovaný firmou STM pomocou dostupných kitov Nucleo, ktoré obsahujú okrem samotného mikrokontroléra aj pomocné obvody a programátor. V distribúcii MicroPython nájdeme podporu pre niektoré typy kitov Nucleo, od jednoduchých až po výkonné typy.
_images/nucleo64.png


```{figure} ./img/nucleo64.jpg
:width: 400px
:name: mp_0010b

Vývojový kit Nucleo-64
```


Konektory na doskách **Nucleo64** umožňujú použitie vývojových modulov z platformy Arduino. 

```{figure} ./img/arduino_uno.jpg
:width: 400px
:name: mp_0010c

Arduino Uno
```

Verzia Nucleo32 je pinovo kompatibilná s platformou Arduino Nano.


