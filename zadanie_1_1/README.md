# Zadanie 1.1:
*Z37 - Aleksandra Szymańska, Angelika Ostrowska, Jakub Bąba*

W tym folderze znajdują się rozwiązania zadania 1.1 w językach C i Python oraz dokumentacja.

W folderze klienta/serwera w danym języku znajdują się:
- właściwy plik z kodem realizującym komunikację
- Dockerfile opisujący konfigurację kontenera
- skrypt run.sh uruchamiający klienta/serwer

## Uruchomienie
Aby uruchomić programy z serwerami/klientami, należy wpisać komendę `bash run` w odpowiednich folderach:
- Serwer w C: `zadanie1/c/server`
- Klient w C: `zadanie1/c/client`
- Serwer w Pythonie: `zadanie1/python/server`
- Klient w Pythonie: `zadanie1/python/client`

**Uwaga:** programy klienckie są skonfigurowane do łączenia się z serwerem w języku Python. Aby połączyć się z serwerem w języku C, należy zamienić linijkę z hostem.