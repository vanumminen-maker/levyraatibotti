# 🚀 Levyraati-botti — Käyttöönotto-ohjeet

---

## VAIHE 1 — Discord Developer Portal: Botin luominen

> **Mikä tämä on?** Discord-botit täytyy "rekisteröidä" Discordin omalla sivustolla ennen kuin ne voivat toimia.

1. Mene osoitteeseen **[discord.com/developers/applications](https://discord.com/developers/applications)**
2. Kirjaudu sisään **omilla Discord-tunnuksillasi**
3. Klikkaa oikeasta yläkulmasta **"New Application"**
4. Anna nimeksi esim. `LevyraatiBotti` → klikkaa **"Create"**
5. Vasemmasta valikosta klikkaa **"Bot"**
6. Klikkaa **"Reset Token"** → vahvista → klikkaa **"Copy"**

   > ⚠️ **TÄRKEÄÄ:** Tämä on salainen avain (token). Älä jaa sitä kenellekään. **Kopioi se nyt** — tarvitset sitä Vaiheessa 3.

7. Sivulla alempana kohdassa **"Privileged Gateway Intents"**, jätä kaikki OFF (levyraatibotti ei tarvitse niitä)
8. Klikkaa sivun alhaalta **"Save Changes"**

✅ **Valmis kun:** Token on kopioitu talteen.

---

## VAIHE 2 — Botin lisääminen Discord-palvelimellesi

1. Vasemmasta valikosta klikkaa **"OAuth2"**
2. Klikkaa **"URL Generator"**
3. Kohdassa **"Scopes"**, laita rasti:
   - ✅ `bot`
   - ✅ `applications.commands`
4. Alle ilmestyy **"Bot Permissions"** -osio. Laita rasti:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Embed Links
   - ✅ View Channels
5. Sivun alhaalta kopioi **"Generated URL"** -kentässä oleva pitkä linkki
6. Avaa se **uuteen selainvälilehteen**
7. Valitse Discord-palvelimesi pudotusvalikosta → klikkaa **"Authorise"** → **"Jatka"**

✅ **Valmis kun:** Botti näkyy palvelimesi jäsenlistassa (aluksi offline).

---

## VAIHE 3 — GitHub: Koodin lataus pilveen

> **Mikä tämä on?** GitHub on paikka, jossa koodi säilytetään netissä. Railway hakee koodin sieltä.

1. Mene osoitteeseen **[github.com](https://github.com)** ja kirjaudu sisään
2. Klikkaa **"+"** → **"New repository"**
3. Täytä:
   - **Repository name:** `levyraati-bot`
   - Valitse **Private**
   - Klikkaa **"Create repository"**
4. Avaa **PowerShell** kansiossa `levyraati-bot` (kirjoita File Explorerin osoitepalkkiin `powershell` ja paina Enter)
5. Kirjoita nämä komennot **yksi kerrallaan**:
   ```
   git init
   git add .
   git commit -m "ensimmäinen versio"
   git branch -M main
   git remote add origin https://github.com/SINUN-KÄYTTÄJÄNIMESI/levyraati-bot.git
   git push -u origin main
   ```
   > Vaihda `SINUN-KÄYTTÄJÄNIMESI` omaan GitHub-käyttäjänimeesi.

✅ **Valmis kun:** GitHub-sivullasi näkyy tiedostot (`main.py`, `requirements.txt` jne.)

---

## VAIHE 4 — Railway: Botin käynnistäminen pysyvästi

> **Mikä tämä on?** Railway pitää botin käynnissä 24/7, vaikka oma tietokone olisi kiinni.

1. Mene osoitteeseen **[railway.app](https://railway.app)**
2. Kirjaudu **GitHub-tunnuksilla** ("Continue with GitHub")
3. Klikkaa **"New Project"**
4. Valitse **"Deploy from GitHub repo"**
5. Anna Railway:lle lupa GitHubiin: klikkaa **"Configure GitHub App"** → valitse `levyraati-bot` → **"Save"**
6. Valitse `levyraati-bot` listasta
7. Railway alkaa rakentaa projektia — **odota** hetki

8. Klikkaa projektia → ylhäältä **"Variables"**-välilehti
9. Klikkaa **"New Variable"** ja täytä:
   - **Name:** `DISCORD_TOKEN`
   - **Value:** (liitä Vaiheessa 1 kopioitu token tähän)
   - Klikkaa **"Add"**

10. Railway käynnistää botin automaattisesti uudelleen

✅ **Valmis kun:** Railway näyttää **"Active"** tai **"Running"** ja botti näkyy Discordissa **vihreänä** (online).

---

## Käyttö arjessa

1. **Ylläpitäjä:** `/aloitalevyraati`
2. **Ylläpitäjä:** `/vaihda Radiohead Creep`
3. **Osallistujat:** `/arvosana 8`, `/arvosana 7`, ...
4. **Ylläpitäjä:** `/vaihda Nirvana Smells Like Teen Spirit` *(botti näyttää edellisen kappaleen keskiarvon automaattisesti)*
5. **Ylläpitäjä:** `/lopetalevyraati` *(botti lähettää koko listan tuloksineen)*

> ⚠️ Muistutus: Botti tallentaa pisteet vain muistiin — jos botti käynnistyy uudelleen kesken raadin, pisteet nollautuvat. Normaalissa raadissa tämä ei ole ongelma.
