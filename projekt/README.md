# Projekt:
*Z37 - Aleksandra Szymańska, Angelika Ostrowska, Jakub Bąba*

W tym folderze znajduje się rozwiązanie zadania 2 w języku Python oraz dokumentacja.

W folderze klienta/serwera znajdują się:
- właściwy plik z kodem realizującym komunikację
- Dockerfile opisujący konfigurację kontenera
- skrypt run.sh uruchamiający klienta/serwer

## Uruchomienie
Aby przygotować z serwerami/klientami, należy wpisać komendę:
```
docker compose up --build -d
```

Następnie, należy uruchomić serwer:
```
docker compose exec server python3 server.py [PORT=8000] [MAX_POŁĄCZEŃ=5]
```
W tym oknie uruchamia się interaktywna sesja serwera, na której można wpisać komendy:
```
close <thread_no>   <--- zamyka połączenie z klientem o podanym numerze
```

W innych oknach można uruchomić klientów wpisując komendę:
```
docker compose exec client python3 client.py [HOST='z37_projekt_server'] [PORT=8000]
```

Pojawi się interaktywna aplikacja, w której można wysłać wiadomość, a także zamknąć połączenie.