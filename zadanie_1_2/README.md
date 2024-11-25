# Zadanie 1.2:
*Z37 - Aleksandra Szymańska, Angelika Ostrowska, Jakub Bąba*

W tym folderze znajduje się rozwiązanie zadania 1.2 w języku Python, skrypty pomocnicze oraz dokumentacja.

W folderze klienta/serwera znajdują się:
- właściwy plik z kodem realizującym komunikację
- Dockerfile opisujący konfigurację kontenera

Ponadto w folderze zadania znajdują się pliki:
- `docker-compose.yaml` - skrypt pomagający w uruchomieniu kontenerów za pomocą jednej komendy
- `disrupt.sh` - skrypt wprowadzający zakłócenia w kontenerze klienta

## Uruchomienie
Uruchomienie kontenerów i rozpoczęcie komunikacji:
```
docker compose build
docker compose up
```
Dodanie zakłóceń
```
bash disrupt.sh
```
