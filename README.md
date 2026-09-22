# Exact Online koppelen aan een AI-assistent

Stel vragen over je eigen Exact Online administratie in gewone taal, zoals "wat
is het totale banksaldo over al mijn administraties?", en laat een AI-assistent
het antwoord uit Exact halen.

Je registreert daarvoor een eigen app in Exact Online en koppelt die aan je eigen
account. De gegevens gaan rechtstreeks van Exact naar jouw computer. Wij zien
niets en hebben geen toegang tot jouw administratie.

## Handleidingen

| Assistent | Handleiding |
|---|---|
| Claude Code op macOS | [docs/claude-macos.md](docs/claude-macos.md) |
| Claude Code op Windows | [docs/claude-windows.md](docs/claude-windows.md) |

Reken op ongeveer een half uur. Je hebt nodig:

* een Exact Online gebruiker die apps mag registreren (meestal de beheerder),
* een Claude-abonnement (Pro of Max) of tegoed op de Anthropic Console,
* Python 3.10 of nieuwer.

Handleidingen voor ChatGPT en andere assistenten volgen.

## Wat zit er in deze repo

| Bestand | Doel |
|---|---|
| `config.py` | leest `.env`, zet de API-URL's (standaard Nederland) |
| `auth.py` | OAuth2 met Exact, tokens in `tokens.json`, automatisch verversen |
| `exact_api.py` | de API-aanroepen die de assistent kan gebruiken |
| `main.py` | eerste koppeling, en een PDF met bankstanden per administratie |
| `CLAUDE.md` | instructies voor de assistent: welke functies er zijn en wat niet mag |

## Alleen lezen

Alle aanroepen naar Exact zijn lezend. `CLAUDE.md` verbiedt de assistent
boekingen, correcties of andere wijzigingen te doen. Controleer uitkomsten altijd
tegen Exact zelf: een verzorgd ogend rapport kan toch op de verkeerde periode of
administratie gebaseerd zijn.

`.env` en `tokens.json` bevatten je sleutels en staan in `.gitignore`. Deel ze
met niemand.

## Licentie

[CC BY 4.0](LICENSE). Je mag alles hergebruiken en aanpassen, ook commercieel,
zolang je naar deze repo verwijst.
