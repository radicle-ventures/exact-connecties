# Exact Online rapportagetools

Python-scripts die via de Exact Online REST API cijfers ophalen uit een of meer
administraties en daar rapportages van maken.

## Regels

**Lees alleen, schrijf nooit.** Alle bestaande API-aanroepen zijn GET. Voer geen
POST, PUT, PATCH of DELETE uit richting Exact Online, ook niet als dat sneller
lijkt. Dit draait tegen een live boekhouding.

**Vraag het na voordat je een boekjaar of administratie aanneemt.** Staat er in
de vraag geen jaartal of entiteit, vraag dat dan, in plaats van te gokken op het
huidige jaar of de eerste division in de lijst.

**Gebruik `venv`.** Draai scripts als `./venv/bin/python <script>`, niet als
`python <script>`, anders ontbreken de dependencies.

**Draai `python main.py` niet als er nog geen `tokens.json` is.** De eerste
autorisatie vraagt om een URL die de gebruiker uit zijn browser plakt, en die
input kan een script dat jij start niet leveren. Zeg dan tegen de gebruiker dat
hij die ene stap zelf in een eigen terminal moet doen.

**Bedragen zijn euro's.** Op de balans (`BalanceType == "B"`) staat een positief
bedrag voor een debetsaldo, een negatief bedrag voor credit. Op de W&V
(`BalanceType == "W"`) is omzet negatief en zijn kosten positief. Dit is al
verwerkt in `get_annual_report_data`, maar reken het na als je zelf sommeert.

## Opzet

| Bestand | Doel |
|---|---|
| `config.py` | leest `.env`, zet de API-URL's (NL: `start.exactonline.nl`) |
| `auth.py` | OAuth2, tokenopslag in `tokens.json`, automatisch verversen |
| `exact_api.py` | alle API-aanroepen, met paginering |
| `main.py` | PDF met bankstanden per administratie |

## Beschikbare API-functies

Alle functies in `exact_api.py` willen een `token` (uit
`auth.get_valid_token()`) en meestal een `division` (het administratienummer,
de `Code` uit `get_divisions`).

```
get_divisions(token)                                  administraties van deze gebruiker
get_bank_gl_accounts(token, division)                 grootboekrekeningen type 10 (kas) en 12 (bank)
get_all_gl_accounts(token, division)                  alle grootboekrekeningen
get_bank_balances(token, division)                    saldo en laatste mutatie per bankrekening
get_reporting_balance(token, division, gl_account_id) saldo van een grootboekrekening
get_last_transaction_date(token, division, gl_id)     datum van de laatste mutatie
get_year_balances(token, division, year)              alle periodesaldi van een boekjaar
get_annual_report_data(token, division, year)         balans en W&V, geaggregeerd
```

Zit de gevraagde data er niet bij, bouw dan een nieuwe aanroep volgens hetzelfde
patroon: `_get_json` voor een enkele respons, `_get_all_json` zodra er meer dan
een paar honderd regels kunnen terugkomen (die volgt de `__next`-links van
Exact, `_get_json` niet).

Datums komen binnen als `/Date(1735689600000)/`. Gebruik `_parse_exact_date`.

## Niet aanraken

`.env` en `tokens.json` bevatten inloggegevens. Lees ze niet uit, print ze niet,
en zet er nooit iets uit in een rapport, commit of bestandsnaam.
