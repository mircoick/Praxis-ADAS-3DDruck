Also dein Projekt sieht soweit echt gut aus, aber ein bisschen kann ich noch meckern 😙

*Schaltplan:*

- Im Schaltplan alle Anschlüsse mindestens mit einem Rastersprung dazwischen verbinden. (Also immer zwischen Anschluss des Steckers und z.B. GND oder einem Widerstand eine grüne Linie dazwischen)

- Hersteller und Herstellerbezeichnungen fehlen noch (Macht dir wirklich einiges leichter, auch für später wenn das sauber dokumentiert ist)

- Unbeschaltete Pins sind noch vorhanden (Wenn die immer unbeschaltet bleiben sollen, kannst du ein "Keine Verbindung" Zeichen einfügen, dann verschwinden auch die Fehler im ERC)

- Unbedingt ERC durchführen und erst, wenn alle Fehler behoben sind, bestellen.

- Namensgebung der Schaltpläne leicht inkonsistent (Groß- und Kleinschreibung) ("platines" kannst du "PCB" nennen, obwohl das vielleicht du universell ist)

- Bleib am besten bei den Schaltplanformaten auch einheitlich (z.B. alle Seiten DINA4), das sieht am Ende, wenn das als PDF raus kommt, besser aus.

- Kann es sein, dass du die Mounting-Holes nicht im Schaltplan hast? Die gehören eigentlich immer auf die erste Seite. (Generell muss auch alles im Schaltplan vorkommen, die kannst du im nachhinein auch aus der Stückliste ausschließen damit die da nicht als Einkaufteil auftauchen)

- Allgemein würde ich dir raten, um dein Problem mit den Steckerbezeichnungen auf dem alten Board zu dem neune Board zu lösen, einen weiteren Eintrag für die Artikeleigenschaften zu erstellen und den Haken auf Zeigen setzen. Den neune Eintrag kannst du dann z.B. Alte Bezeichnung nennen und diesen auch auf der Leiterplatte andrucken lassen. Dann kannst du einheitliche Referenz vergeben. Wenn du das machst, kann man KiCad sagen, dass er für jede Seite bei einem Präfix anfangen soll. Also auf Seite 1 bei 100 und Seite 2 bei 200. Dann nennen sich deine Stecker X100, X101, X200. Das macht das suchen später im Schaltplan viel einfacher und man weiß sofort zu welchem Schaltungsteil das gehört.

- Auf der ersten Seite kannst du die Kästen der einzelnen Seiten auch mit Farben füllen, sieht einfach besser aus [Rand: Blue2; Füllen: L.Yellow]

*PCB-Editor:*

- Für den DRC musst du unbedingt Regeln anlegen, ist schwer am Anfang aber das muss sein. Dazu kannst du von Git auch erstmal die Regeln importieren aus PCBWay und gff. abändern. [https://github.com/pcbway/PCBWay-Design-Rules] die aktuellen gibt es hier [https://www.pcbway.com/capabilities.html]

- Wenn du dann den DRC durchgefürt hast, alle Fehler beheben und verschieben. Wenn du das nicht behebst, bauen dir die Chinesen einfach das was die von dir bekommen, auch wenn das dann nicht funktioniert.

- Auf Lage 1 (F.Cu), 4 (In3.Cu), 5 (In4.Cu) und 6 (B.Cu) fehlen Polygone mit Net: z.B. GND. Damit der Lagenaufbau Symmetrisch ist. Das ist gerade bei späterem Lötprozess oder beim Fertigen wichtig, damit sich die Leiterplatte nicht verzieht. Außerdem verringert das die Störanfälligkeit.

- Den Bestückungsdruck noch verschieben, sodass man alles lesen kann und auch die Strichstärke nach den Designregeln passt. So, dass man auch erkennt, wo ein Wort anfängt und aufhört.

- Für die Leitungsbreiten gibt es einen Rechner in KiCad (auch den aus MWT damals) den kannst du nehmen und über den Strom die breiten ausrechnen. Wenn du das nicht schon gemacht hast.

- Generell kannst du im Bestückungsdruck auch erklärende Tabelle oder Richtungspfeile oder oder oder einbringen. Du kannst auch ganze Tabellen als Vektorgrafik einbinden, falls das hilft. Also auch viele Informationen wie blaues Kabel mit Stecker hier rauf.