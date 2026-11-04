@echo off
rem Oeffnet die Einkaufsliste (docs\einkaufsliste.html) im Standardbrowser. Kein Server noetig.
rem Neu erzeugen (nach Modell- oder Preisaenderung): python -X utf8 scripts\bom.py
start "" "%~dp0..\docs\einkaufsliste.html"
