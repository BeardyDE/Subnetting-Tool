import ipaddress
import math
import os

def berechne_subnetze(ip, subnetze_benoetigt):
    try:
        netzwerk = ipaddress.ip_network(ip, strict=False)
        subnet_bits = math.ceil(math.log(subnetze_benoetigt, 2))
        neuer_prefix = netzwerk.prefixlen + subnet_bits
        
        if neuer_prefix > 32:
            raise ValueError("Zu viele Subnetze für diese IP-Adresse.")
        
        subnetze = list(netzwerk.subnets(new_prefix=neuer_prefix))
        return subnetze
    except ValueError as e:
        print(f"Fehler: {e}")
        return None
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        return None

def eingabe_von_konsole():
    ip_adresse = input("Geben Sie die IP-Adresse mit Präfix ein (z.B. 192.168.1.0/24): ")
    try:
        subnetze_benoetigt = int(input("Wie viele Subnetze werden benötigt?: "))
    except ValueError:
        print("Fehler: Die Anzahl der Subnetze muss eine ganze Zahl sein.")
        return None, None
    return ip_adresse, subnetze_benoetigt

def eingabe_von_datei(dateipfad):
    if not os.path.exists(dateipfad):
        print(f"Fehler: Datei '{dateipfad}' wurde nicht gefunden.")
        return None, None

    try:
        with open(dateipfad, 'r') as datei:
            zeilen = datei.readlines()
            ip_adresse = zeilen[0].strip()
            subnetze_benoetigt = int(zeilen[1].strip())
            return ip_adresse, subnetze_benoetigt
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None, None

def speichere_ergebnis_in_datei(zielfile, subnetze):
    try:
        with open(zielfile, 'w') as datei:
            for subnetz in subnetze:
                datei.write(f"{subnetz}\n")
        print(f"Subnetze erfolgreich in '{zielfile}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")

def hauptmenue():
    print("Subnetzberechnungstool")
    print("======================")
    print("1. Manuelle Eingabe")
    print("2. Eingabe aus einer Datei")

    wahl = input("Bitte wählen Sie eine Eingabemethode (1 oder 2): ")

    if wahl == '1':
        ip_adresse, subnetze_benoetigt = eingabe_von_konsole()
    elif wahl == '2':
        dateipfad = input("Geben Sie den Pfad zur Datei ein: ")
        ip_adresse, subnetze_benoetigt = eingabe_von_datei(dateipfad)
    else:
        print("Ungültige Auswahl.")
        return

    if not ip_adresse or not subnetze_benoetigt:
        print("Fehlerhafte Eingabe. Bitte erneut versuchen.")
        return

    subnetze = berechne_subnetze(ip_adresse, subnetze_benoetigt)

    if subnetze:
        print("\nBerechnete Subnetze:")
        for subnetz in subnetze:
            print(subnetz)
        
        speichern = input("Möchten Sie die Ergebnisse in einer Datei speichern? (j/n): ")
        if speichern.lower() == 'j':
            zielfile = input("Geben Sie den Dateinamen ein (z.B. subnetze.txt): ")
            speichere_ergebnis_in_datei(zielfile, subnetze)

if __name__ == "__main__":
    hauptmenue()
