# 🎵 Levyraati-botti

Discord-botti levyraatia varten. Ylläpitäjä vaihtaa kappaleet, osallistujat antavat arvosanat, ja botti lähettää yhteenvedon raadin lopussa.

---

## Komennot

| Komento | Oikeus | Kuvaus |
|---|---|---|
| `/aloitalevyraati` | Manage Messages | Aloittaa uuden raadin (nollaa edellisen) |
| `/vaihda <artisti> <kappale>` | Manage Messages | Vaihtaa arvosteltavan kappaleen |
| `/arvosana <1-10>` | Kaikki | Antaa arvosanan nykyiselle kappaleelle |
| `/lopetalevyraati` | Manage Messages | Lopettaa raadin ja lähettää tuloslistan |

---

## Asennus paikallisesti (testaamista varten)

1. Asenna Python 3.11+ jos ei ole asennettu: https://python.org

2. Asenna riippuvuudet:
   ```
   pip install -r requirements.txt
   ```

3. Luo tiedosto `.env` tähän kansioon ja kirjoita sinne:
   ```
   DISCORD_TOKEN=sinun_token_tähän
   ```

4. Käynnistä botti:
   ```
   python main.py
   ```

---

## Deployment Railwaylle

Katso erillinen deployment-opas tai kysele lisää.
