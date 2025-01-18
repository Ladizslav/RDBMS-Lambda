# README

## Informace o projektu
- Jméno projektu: Pokémoní databáze
- Autor: Ladislav Dobiáš
- Datum dokončení: 18.1.2025
- Kontaktní údaje: dobias@spsejecna.cz
- Instituce: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
- Typ projektu: Školní projekt

## Příprava aplikace

1. Stáhněte soubor z Moodlu nebo z GitHubu.
2. Spusťte Visual Studio Code.
3. Otevřete terminál a zadejte příkaz:

    pip install mysql-connector-python

**Poznámka:** Pokud nastane chyba, může to být způsobeno:
- Nenainstalovaným Pythonem na vašem počítači.
- Zapnutým proxy nastavením, které blokuje instalaci balíčků.
        
---
        
## Nastavení MySQL
        
1. Spusťte aplikaci **MySQL Workbench 8.0**.
2. Zkontrolujte, zda je vytvořeno základní připojení (Connection) se specifikací:

    User: root Host: localhost Port: 3306

3. Pokud připojení neexistuje:
- Klikněte na tlačítko `+` pro vytvoření nového připojení.
- Nastavte `Server Management` přes "Configure Server Management".
4. **Poznámka:** 
- Je nuté vyplnit data do config.json.
- Tady jsou moje použite:

{
    "host": "127.0.0.1",
    "user": "root",
    "password": "student",
    "database": "pokemon_db",
    "port": 3306
}
      
---
        
## Spuštění aplikace
        
Aplikaci lze spustit dvěma způsoby:
        
### Ve Visual Studio Code
1. Otevřete soubor `main.py`.
2. Spusťte skript stisknutím klávesy `F5` nebo příkazem `Run`.
        
### Přímo ze souboru
1. Otevřete terminál.
2. Navigujte do složky, kde se nachází soubor `main.py`.
3. Spusťte příkaz:
    python main.py

---

## Jak aplikace funguje
        
1. Po spuštění aplikace se uživateli zobrazí nabídka dostupných akcí v konzoli.
2. Postupujte podle pokynů zobrazených na obrazovce.
3. Databáze a tabulky se vytvoří automaticky při spuštění aplikace, není nutné je manuálně aktivovat.
        
## Použité technologie
- Staré pojekty
- ChatGPT
- W3Schools
- GeeksforGeeks

## Test cases
- Test case jsou uloženy v TestCases/..
- Postupujte podle jejich číslení tzv. 1.,2.,3.

## Model databáze
- Model je uložen v img/..