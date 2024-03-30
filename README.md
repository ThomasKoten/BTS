# Semestrální práce k přemětu BTS

## Použité komponenty
* Raspberry Pi 4 s nainstalovaným Home Assistant
* Zigbee USB dongle
* Multifunční kostka Aqara
* Senzor otevření dvěří/oken ZC-M1
* Žárovka IKEA TRÅDFRI LED 600 lm
* Adaptér pro napájení žárovky ze zásuvky

## Implementované automatizace
* Nastavení jasu žárovky podle stavu okna
* Přepíná stavu žárovky dvojitým poklepáním kostkou
*  Korigování jasu žárovky pomocí otáčení kostkou
*  Změna barvy žárovky převracením kostky o 90°
  
## Bližší popis automatizací
### Nastavení jasu žárovky podle stavu okna
Pokud je okno otevřeno sníží se jas žárovky, aby světlo nepřilákalo okolní hmyz.
Pokud je okno znovu zavřeno hodnota jasu se vrátí na hodnotu před otevřením okna.
> [!IMPORTANT]
>Jas se změní jen pokud žárovka svítí.

### Přepíná stavu žárovky dvojitým poklepáním kostkou
Dvojitým poklepáním kostkou dojde k vypnutí/zapnutí žárovky. 
Zároveň dojde k nastavení barvy a jasu na počáteční hodnoty. 
> [!NOTE]
> V tomto případě je to bílá barva `rgb(255, 255, 255)` a jas ```127```.

###  Korigování jasu žárovky pomocí otáčení kostkou
Vodorovným otáčením kostky doprava se zvyšuje jas žárovky. 
Vodorovným otáčením kostky doleva se snižuje jas žárovky.
> [!IMPORTANT]
>Žárovka musí svítit aby došlo ke změně jasu.

###  Změna barvy žárovky převracením kostky o 90°
Převrácením kostky o 90° se změní barva žárovky.

Barva světla záleží na horní straně kostky po převrácení viz. diagram kostky.
