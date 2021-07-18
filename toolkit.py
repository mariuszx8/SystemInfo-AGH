import os
import platform
import subprocess
import csv
from tkinter import *

if __name__ == '__main__':
    comp_name, sys_name, sys_v, sys_p, bios, cpu = "", "", "", "", "", ""
    user = os.getlogin()  # Nazwa zalogowanego użytkownika
    if str(platform.system()) == "Windows":  # Dla systemu Windows korzysta z poleceń cmd
        try:
            cpu = subprocess.check_output("wmic cpu get name").decode('ISO-8859-1').strip().split("\n")[1]  # Pobranie modelu procesora, odczytanie danych z konsoli
            info = subprocess.check_output("systeminfo /fo csv").decode('ISO-8859-1')  # Pobranie informacji o systemie (zwrócone przez konsolę w formacie csv)
            reader = csv.reader(info.split('\n'), delimiter=",")  # Odczyt danych  o systemie w formacie csv
            line_count = 0
            for row in reader:
                if line_count == 1:  # Dostęp do odpowiedniej linii z właściwymi parametrami (linia 0 to nazwy kolumn, linia 1 to wartości parametrów)
                    comp_name = row[0]
                    sys_name = row[1]
                    sys_v = row[2]
                    sys_p = row[3]
                    bios = row[15]
                line_count += 1
        except EXCEPTION as e:
            print(e)
    if str(platform.system()) == "Linux":  # Wersja dla systemu Linux
        try:
            info = os.uname()  # Polecenie uname działa tylko pod Linuxem
            comp_name = info[1]
            sys_name = info[0] + " " + info[2]
            sys_v = info[3]
            cpu = (subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | cut -f 2 -d ':' | awk '{$1=$1}1' | uniq", shell=True).strip()).decode()  # Odczyt informacji o procesorze, poprzez odczyt pliku cpuinfo oraz przetworzenie zwróconej zawartości
            bios = (subprocess.check_output("cat /sys/class/dmi/id/bios_vendor", shell=True).strip()).decode() + " " + (subprocess.check_output("cat /sys/class/dmi/id/bios_version", shell=True).strip()).decode()  # Odczyt informacji na temat BIOSu, poprzez odczyt odpowiednich plików
        except EXCEPTION as e:
            print(e)
    welcome = "Witaj " + user
    window = Tk()  # GUI - utworzenie okna
    window.title("Szczegóły komputera")  # Tytuł okna programu
    lbl = Label(window, text=welcome, font=("Arial", 12))  # Dodanie nagłówka powitalnego z nazwą użytkownika (domyślnie wyśrodkowane)
    lbl.pack(padx=10, pady=10)  # Wstawienie nagłówka z odpowiednimi marginesami
    data = "Nazwa komputera: {0}\nNazwa systemu: {1}\nWersja systemu: {2}\nProducent systemu: {3}\nBIOS: {4}\nProcesor: {5}".format(
        comp_name, sys_name, sys_v, sys_p, bios, cpu)
    lbl = Label(window, text=data, font=("Arial", 11), anchor="e", justify=LEFT)  # Dodanie tekstu z parametrami (wyrównane do lewej strony)
    lbl.pack(padx=10, pady=10)  # Wstawienie tekstu z odpowiednimi marginesami
    window.mainloop()  # Wyświetlenie okna aplikacji
