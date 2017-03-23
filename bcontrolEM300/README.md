# plugins

# Das Plugin liest die Zähler EM300 aus. 

welche folgende Daten liefert.
* Wirkleistung
* Blindleistung
* Scheinleistung
* Summe und Einzelphasen
* Leiterspannungen
* Leiterströme
* Leistungsfaktor

Auf der Website 
https://www.b-control.com/produkte/em-300.html
findet man mehr Details darüber.

Programmiert wurde das ganze gegen diese API beschreibung
https://www.b-control.com/fileadmin/Webdata/b-control/Uploads/Downloads/Energy_Management/Deutsch/B-control_Energy_Manager_-_JSON-API.0101.pdf

Wenn ich mich nicht verzählt habe gibt es 59 Messerte die ausgelesen werden können.

Getestet wurde es mit den Zählern EM300 LR die Versionen EM300 L und EM300 LRW sollten aber auch gehen.

Zum einrichten muss man nur die IP angeben unter welcher der Zähler erreichbar ist und die Abfragefrequenz.
