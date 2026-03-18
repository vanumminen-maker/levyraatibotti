import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------------------------------------------------------------------------
# Botin tila (muistissa, nollautuu restartin yhteydessä)
# ---------------------------------------------------------------------------
state = {
    "active": False,
    "current_song": None,   # {"artist": str, "title": str, "scores": {user_id: int}}
    "results": [],          # [{"artist": str, "title": str, "average": float, "votes": int}]
}


def is_admin():
    """Tarkistaa, että käyttäjällä on Manage Messages -oikeus."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.guild_permissions.manage_messages:
            return True
        await interaction.response.send_message(
            "❌ Sinulla ei ole oikeuksia tähän komentoon (tarvitset **Manage Messages** -oikeuden).",
            ephemeral=True,
        )
        return False
    return app_commands.check(predicate)


def save_current_song():
    """Tallentaa nykyisen kappaleen results-listaan, jos siitä on ääniä."""
    song = state["current_song"]
    if song is None:
        return None
    scores = list(song["scores"].values())
    if not scores:
        return None
    avg = round(sum(scores) / len(scores), 2)
    result = {
        "artist": song["artist"],
        "title": song["title"],
        "average": avg,
        "votes": len(scores),
    }
    state["results"].append(result)
    return result


# ---------------------------------------------------------------------------
# Discord-asetus
# ---------------------------------------------------------------------------
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# ---------------------------------------------------------------------------
# Komennot
# ---------------------------------------------------------------------------

@tree.command(name="aloitalevyraati", description="Aloita uusi levyraati (nollaa edellisen).")
@is_admin()
async def aloita(interaction: discord.Interaction):
    state["active"] = True
    state["current_song"] = None
    state["results"] = []
    await interaction.response.send_message(
        "🎶 **Levyraati on aloitettu!**\n"
        "Käytä `/vaihda <artisti> <kappale>` asettaaksesi ensimmäisen kappaleen."
    )


@tree.command(name="vaihda", description="Aseta uusi arvosteltava kappale.")
@app_commands.describe(artisti="Artistin nimi", kappale="Kappaleen nimi")
@is_admin()
async def vaihda(interaction: discord.Interaction, artisti: str, kappale: str):
    if not state["active"]:
        await interaction.response.send_message(
            "❌ Levyraati ei ole käynnissä. Aloita ensin komennolla `/aloitalevyraati`.",
            ephemeral=True,
        )
        return

    lines = []

    # Tallenna edellinen kappale jos sellainen oli
    saved = save_current_song()
    if saved:
        lines.append(
            f"📊 **{saved['artist']} — {saved['title']}** sai keskiarvon "
            f"**{saved['average']}/10** ({saved['votes']} ääntä)\n"
        )

    # Vaihda uuteen kappaleeseen
    state["current_song"] = {"artist": artisti, "title": kappale, "scores": {}}
    lines.append(
        f"🎵 Nyt arvosteltavana: **{artisti} — {kappale}**\n"
        "Antakaa arvosanat komennolla `/arvosana <1-10>`"
    )

    await interaction.response.send_message("\n".join(lines))


@tree.command(name="arvosana", description="Anna arvosana nykyiselle kappaleelle (1–10).")
@app_commands.describe(pisteet="Arvosana väliltä 1–10")
async def arvosana(interaction: discord.Interaction, pisteet: int):
    if not state["active"]:
        await interaction.response.send_message(
            "❌ Levyraati ei ole käynnissä.", ephemeral=True
        )
        return

    if state["current_song"] is None:
        await interaction.response.send_message(
            "❌ Yhtään kappaletta ei ole asetettu vielä. Ylläpitäjä voi asettaa kappaleen komennolla `/vaihda`.",
            ephemeral=True,
        )
        return

    if not (1 <= pisteet <= 10):
        await interaction.response.send_message(
            "❌ Arvosanan täytyy olla luku väliltä **1–10**.", ephemeral=True
        )
        return

    user_id = interaction.user.id
    if user_id in state["current_song"]["scores"]:
        old = state["current_song"]["scores"][user_id]
        await interaction.response.send_message(
            f"⚠️ Olet jo antanut arvosanan **{old}/10** tälle kappaleelle. "
            "Voit äänestää vain kerran per kappale.",
            ephemeral=True,
        )
        return

    state["current_song"]["scores"][user_id] = pisteet
    song = state["current_song"]
    await interaction.response.send_message(
        f"✅ Arvosanasi **{pisteet}/10** kappaleelle *{song['artist']} — {song['title']}* on kirjattu! "
        f"(Vain sinä näet tämän viestin)",
        ephemeral=True,
    )


@tree.command(name="lopetalevyraati", description="Lopeta levyraati ja lähetä tulosyhteenveto.")
@is_admin()
async def lopeta(interaction: discord.Interaction):
    if not state["active"]:
        await interaction.response.send_message(
            "❌ Levyraati ei ole käynnissä.", ephemeral=True
        )
        return

    # Tallenna viimeinen kappale
    save_current_song()

    state["active"] = False
    state["current_song"] = None

    if not state["results"]:
        await interaction.response.send_message(
            "🏁 Levyraati lopetettu. Yhtään kappaletta ei arvosteltu."
        )
        return

    ranked = sorted(state["results"], key=lambda r: r["average"], reverse=True)
    state["results"] = []

    lines = ["# 🏁 Levyraati päättyy! Tulokset:\n"]
    for i, r in enumerate(ranked, start=1):
        lines.append(
            f"**{i}. {r['artist']} — {r['title']}:** {r['average']}/10 "
            f"({r['votes']} {'ääni' if r['votes'] == 1 else 'ääntä'})"
        )

    await interaction.response.send_message("\n".join(lines))


@tree.command(name="ohje", description="Näytä ohjeet levyraadin käyttöön.")
async def ohje(interaction: discord.Interaction):
    teksti = (
        "## 🎵 Levyraati-botin ohjeet\n\n"
        "### 👑 Ylläpitäjille *(Manage Messages -oikeus)*\n"
        "`/aloitalevyraati` — Aloittaa uuden raadin (nollaa edellisen)\n"
        "`/vaihda <artisti> <kappale>` — Vaihtaa arvosteltavan kappaleen. "
        "Botti näyttää edellisen kappaleen keskiarvon automaattisesti.\n"
        "`/lopetalevyraati` — Lopettaa raadin ja lähettää tuloslistan kanavalle "
        "järjestyksessä korkeimmasta matalimpaan.\n\n"
        "### 🎧 Osallistujille\n"
        "`/arvosana <1-10>` — Anna arvosana nykyiselle kappaleelle. "
        "Voit äänestää kerran per kappale. Arvosanasi ei näy muille."
    )
    await interaction.response.send_message(teksti, ephemeral=True)


# ---------------------------------------------------------------------------
# Käynnistys
# ---------------------------------------------------------------------------

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Botti käynnissä: {client.user} (ID: {client.user.id})")
    print("Slash-komennot synkronoitu.")


client.run(TOKEN)
