import pytest, cssutils, os, bs4

def get_html():
    with open("index.html", encoding="utf-8") as f: #HTML fájl beolvasása
        return bs4.BeautifulSoup(f, 'html.parser') #Visszadobás egyben
    
def get_css():
    with open("style.css", encoding="utf-8") as f: #CSS fájl beolvasása
        css = cssutils.parseString(f.read())
        return [x for x in css.cssRules if x.type == x.STYLE_RULE]#Visszadobás egyben

def test_file_structure():
    expected = ["index.html",
                "style.css", 
                "szoveg.txt", 
                "hetfo_csirkecomb.jpg", 
                "kedd_makosteszta.jpg", 
                "szerda_halaszle.jpg", 
                "csutortok_rantotthus.jpg",
                "pentek_borsofozelek.jpg"] #Az elvárt fájlstruktúra
    
    files = os.listdir("./") #Helyi fájlok listája
    for f in expected:
        assert files.__contains__(f), f"A hiányzik a(z) {f} fájl!" #Az elvárt és jelenlegi struktúra összehasonlítása, ha hiányzik a jelenlegiből akkor AssertionError

#Fájlok beolvasása/átalakítása
html_soup = get_html() #bs4 html oldal
css_list = get_css() #cssutils lista

def GetPropertyValue(selector: str, propName: str):
    assert any(x for x in css_list if x.selectorText == selector), f"Nincs {selector} osztály!" #Osztály létezés ellenőrzés
    assert next(x for x in css_list if x.selectorText == selector).style.getPropertyValue(propName), f"Nincs {propName} tulajdonság!" 
    return next(x for x in css_list if x.selectorText == selector).style.getPropertyValue(propName)

#Feladatok
@pytest.mark.points(1)
def test_feladat_1():
    assert GetPropertyValue("body", "color") == "#006", "Helytelen az oldal betűszíne!"
    assert GetPropertyValue("body", "background-color") == "#EF6", "Helytelen a beállított háttérszín!"

@pytest.mark.points(1)
def test_feladat_2():
    assert GetPropertyValue("body", "font-style") == "italic", "Nincs dőlt beállítás az oldalon!"

@pytest.mark.points(1)
def test_feladat_3():
    assert GetPropertyValue("body", "width") == "50%", "Helytelen az oldal szélessége!"
    assert GetPropertyValue("body", "margin") == "auto", "Nincs középre igazítva az oldal!" 

@pytest.mark.points(2)
def test_feladat_4():
    assert html_soup.find("h1") != None, "Nem létezik egyes szintű fejezetcím!"
    assert html_soup.find("h1").text == "Heti étlap", "Helytelen a cím szövege!"
    #Meg kell nézni, hogy hol van pontosan a h1, ebben az esetben a body-nak 
    #konkrét leszármazottja, és az első. (Mindkettőt tudja a bs4)

@pytest.mark.points(2)
def test_feladat_5():
    assert html_soup.find(class_="hetek") != None, "Nem létezik hetek osztály az oldalon!"
    assert html_soup.find(class_="hetek").name == "div", "A hetek osztályú elem nem div!"

@pytest.mark.points(2)
def test_feladat_6():
    elems = [("a", "Előző hét"),
             ("span", "Aktuális hét"),
             ("a", "Következő hét")]
    
    for tag, text in elems:
        assert html_soup.find(class_="hetek").find(name=tag) != None, f"Nem létezik {tag} típusú elem a .hetek div-ben!"
        assert html_soup.find(class_="hetek").find(name="span") != None, f"Nem létezik olyan elem a .hetek div-ben, aminek a szövege '{text}' lenne!"