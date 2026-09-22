# Exact Online koppelen aan Claude Code (macOS)

Deze handleiding beschrijft wat je moet doen om deze tool toegang te geven tot
jouw eigen Exact Online administratie(s). Je registreert daarvoor een eigen app
in Exact Online en koppelt die aan je eigen account. Er worden geen gegevens met
ons gedeeld en wij hebben geen toegang tot jouw administratie.

De commando's in deze handleiding gaan uit van een Mac met macOS 13 (Ventura) of
nieuwer. Werk je op Windows, gebruik dan
[de Windows-handleiding](claude-windows.md).

Reken op ongeveer een half uur.

---

## Deel 1. Eenmalig in Exact Online

Dit deel is hetzelfde als op Windows: het gebeurt helemaal in de browser.

### Stap 1. Zorg voor het juiste account

Je hebt een Exact Online gebruiker nodig die:

* toegang heeft tot de administratie(s) die je wilt uitlezen, en
* de rol heeft om apps te registreren (meestal de beheerder van de omgeving).

Twijfel je? Log in op Exact Online en kijk of je bij "Mijn apps" kunt komen. Kan
dat niet, dan moet je beheerder deze stappen doen of je de rol geven.

### Stap 2. Open het App Center

Ga naar https://apps.exactonline.com en log in met dat account. Zoek de sectie
waar je je eigen apps beheert (die heet "Manage my apps" of "Mijn apps beheren").

### Stap 3. Registreer een app

Kies voor het registreren van een nieuwe app. Exact maakt onderscheid tussen een
app voor testen/eigen gebruik en een app die je publiceert voor andere klanten.
Voor eigen gebruik binnen je eigen omgeving volstaat de eerste. Publiceren is
niet nodig en vraagt een certificeringstraject.

Vul in:

| Veld | Waarde |
|---|---|
| Naam | vrij te kiezen, bijvoorbeeld "Bankstanden rapportage" |
| Redirect URI | `https://www.exact.com/login` |
| Type | server-side app (de variant die een client secret oplevert) |

**De redirect URI moet letterlijk zo worden ingevuld, teken voor teken.** Dit is
verreweg de meest gemaakte fout. Wijkt hij ook maar één karakter af (een extra
slash, http in plaats van https), dan weigert Exact de autorisatie later met een
foutmelding die niet duidelijk maakt dat dit de oorzaak is.

### Stap 4. Noteer de twee sleutels

Na het opslaan toont Exact:

* **Client ID**, een lange code in de vorm `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
* **Client Secret**

Het secret wordt in veel gevallen maar één keer getoond. Sla beide direct op in
een wachtwoordmanager (bijvoorbeeld de app Wachtwoorden of 1Password). Ben je het
secret kwijt, dan genereer je in het App Center een nieuwe en vervang je hem
overal.

Deel deze twee waarden met niemand. Ze horen bij jouw omgeving.

### Stap 5. Controleer je regio

Deze tool is ingesteld op de Nederlandse omgeving, `start.exactonline.nl`. Log
je normaal in op een ander domein (`.be`, `.de`, `.co.uk`, `.fr`, `.es`, `.com`),
pas dan `BASE_URL` in `config.py` aan naar dat domein, bijvoorbeeld
`https://start.exactonline.be`. Anders krijg je een lege of foutieve respons.

---

## Deel 2. Claude Code installeren

Claude Code is een assistent die in je terminal draait, de projectmap kan lezen
en zelf commando's uitvoert. Je typt je vraag in gewoon Nederlands.

Doe dit als eerste op je computer. De stappen hierna gaan een stuk makkelijker
als je hem al hebt, want het meeste werk uit Deel 3 kun je aan hem overlaten.

Je opent de Terminal met Cmd + spatie (Spotlight), `terminal` typen en Enter
drukken. Je vindt hem ook in Finder onder Programma's > Hulpprogramma's.

Plakken in de Terminal gaat met Cmd + V, net als overal op de Mac.

### Stap 6. Installeer Claude Code

Je hebt een abonnement op Claude (Pro of Max) of een account met tegoed op de
Anthropic Console nodig. Dat staat los van je Exact-licentie.

Installeren doe je in de Terminal, met dit ene commando:

```
curl -fsSL https://claude.ai/install.sh | bash
```

Dit is de aanbevolen route, want die versie werkt zichzelf bij. Gebruik je
Homebrew, dan kan het ook met onderstaand commando, maar dan moet je zelf
updaten:

```
brew install --cask claude-code
```

Twee dingen die misgaan bij deze stap:

* **"command not found: claude" direct na het installeren.** De installer zet
  het programma in een map die je Terminal nog niet kent. Sluit het
  Terminal-venster en open een nieuw. Helpt dat niet, lees dan de laatste regels
  die de installer heeft getoond: daar staat het commando dat je moet uitvoeren
  om die map toe te voegen.
* **macOS vraagt of de Terminal bij je bestanden mag**, bijvoorbeeld in
  Documenten, Bureaublad of Downloads. Dat is normaal. Klik op Sta toe, anders
  kan Claude de projectmap niet lezen. Heb je per ongeluk geweigerd, zet het dan
  aan in Systeeminstellingen > Privacy en beveiliging > Bestanden en mappen >
  Terminal.

Je hebt hier geen Python, Node.js of Git voor nodig.

### Stap 7. Haal het project op en log eenmalig in

Ga naar https://github.com/radicle-ventures/exact-connecties, klik op de groene knop **Code** en kies
**Download ZIP**. Dubbelklik het zip-bestand in Downloads om het uit te pakken,
en verplaats de map `exact-connecties-main` naar een vaste plek buiten iCloud
Drive, bijvoorbeeld `~/Projects` (zie Deel 5). Dat is vanaf nu de projectmap.

Start Claude Code vanuit de projectmap. Twee commando's:

```
cd ~/pad/naar/het/project
```

```
claude
```

Handig: typ `cd ` (met een spatie erachter) en sleep de projectmap vanuit Finder
in het Terminal-venster. Het pad wordt dan voor je ingevuld, ook als er spaties
in staan. Druk daarna op Enter.

De eerste keer vraagt hij hoe je wilt inloggen. Kies je Claude-abonnement, dan
opent er een browservenster. Kies je de Console, dan plak je een API-sleutel.
Daarna onthoudt hij dat.

Voordat Claude een commando uitvoert, vraagt hij toestemming. Lees die regel
even en bevestig als hij klopt. Je kunt per soort commando aangeven dat hij het
voortaan zonder vragen mag doen.

---

## Deel 3. Het project klaarzetten en koppelen

De stappen 8 tot en met 10 kun je grotendeels aan Claude overlaten. Vraag hem in
de projectmap: *"zet dit project klaar: maak een venv en installeer de
dependencies"*. Hij voert de commando's uit en vraagt onderweg toestemming.

Hieronder staan ze ook met de hand, voor het geval je het liever zelf doet of
iets misgaat.

### Stap 8. Zorg voor Python

Je hebt Python 3.10 of nieuwer nodig. Op de Mac heet het commando `python3`, niet
`python`. Controleren:

```
python3 --version
```

Drie mogelijke uitkomsten:

* **Je ziet 3.10 of hoger.** Prima, ga door naar stap 9.
* **Je ziet 3.9.x.** Dat is de Python die Apple meelevert met de
  ontwikkelaarstools. Die is te oud voor dit project. Installeer een nieuwere
  versie zoals hieronder beschreven.
* **Er verschijnt een venster dat vraagt om de "command line developer tools"
  te installeren.** Klik dat weg met Annuleer: ook dat levert de te oude versie
  op. Installeer Python zoals hieronder beschreven.

Installeren: haal de macOS-installer van https://www.python.org/downloads/ en
doorloop hem met de standaardinstellingen. Gebruik je Homebrew, dan kan het ook
met `brew install python`. Sluit daarna de Terminal, open een nieuw venster en
controleer met `python3 --version` of je nu de nieuwe versie ziet.

### Stap 9. Installeer de onderdelen

Ga in de Terminal naar de map van het project. Drie commando's, een voor een:

```
cd ~/pad/naar/het/project
```

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Je ziet nu `(venv)` voor de regel staan. Dat betekent dat je in de juiste
omgeving zit. Binnen die omgeving werkt ook gewoon `python` en `pip`. Dan:

```
pip install -r requirements.txt
```

Elke keer dat je een nieuw Terminal-venster opent, moet je opnieuw eerst `cd`
naar de projectmap en `source venv/bin/activate` draaien.

### Stap 10. Zet je sleutels klaar

Er moet een bestand komen met de naam `.env`, in de projectmap. Finder verbergt
bestanden die met een punt beginnen en TextEdit maakt er graag een `.env.rtf` of
`.env.txt` van, dus doe het via de Terminal. Vervang de twee waarden door die uit
stap 4 en voer beide regels uit:

```
echo "EXACT_CLIENT_ID=jouw-client-id" > .env
```

```
echo "EXACT_CLIENT_SECRET=jouw-client-secret" >> .env
```

Let op het verschil: de eerste regel gebruikt één `>` (maakt het bestand aan of
overschrijft het), de tweede `>>` (voegt een regel toe). Draai je de tweede per
ongeluk met één `>`, dan is je client ID weg en moet je beide regels opnieuw
doen.

Controleer daarna of het klopt met `cat .env`. Je hoort precies twee regels te
zien, zonder aanhalingstekens eromheen.

Maak het bestand daarna alleen leesbaar voor jezelf:

```
chmod 600 .env
```

Wil je het bestand in Finder zien, druk dan in de projectmap op
Cmd + Shift + punt. Dezelfde toetsen verbergen het weer.

Dit bestand staat al in `.gitignore` en hoort nooit in versiebeheer, in iCloud
Drive-deelmappen of in een mailtje terecht te komen.


### Stap 11. Koppel je account, eenmalig

**Deze ene stap moet je zelf doen, in je eigen Terminal-venster.** Laat Claude
hem niet voor je starten. Je moet halverwege een URL uit je browser plakken, en
die invoer kan hij niet leveren. Het script blijft dan wachten op iets dat nooit
komt.

Start de tool (met `(venv)` voor de regel, zie stap 9):

```
python main.py
```

Er gebeurt nu het volgende:

1. Er opent een browservenster met een Exact Online inlogscherm. Log in met het
   account uit stap 1. Opent er niets, kopieer dan de lange URL die in de
   Terminal is verschenen en plak die zelf in Safari of Chrome.
2. Exact vraagt of je de app toegang wilt geven. Bevestig dat.
3. Je komt terecht op een pagina van exact.com. Die pagina zelf doet niets, dat
   is normaal en geen fout.
4. Kopieer de **volledige URL uit de adresbalk** van die pagina, inclusief alles
   achter het vraagteken, en plak die terug in de Terminal waar erom gevraagd
   wordt. Druk op Enter.

Let bij Safari op: die toont in de adresbalk standaard alleen de domeinnaam.
Klik eerst in de adresbalk zodat de hele URL zichtbaar wordt, en kopieer dan
pas met Cmd + A en Cmd + C.

De tool haalt daar de autorisatiecode uit en wisselt die in voor tokens. Die
worden opgeslagen in `tokens.json`. Vanaf nu ververst alles zichzelf en hoef je
dit niet opnieuw te doen, ook niet als je verder via Claude werkt.

Behandel `tokens.json` als een wachtwoord. Wie dat bestand heeft, kan bij je
administratie. Zet ook dit bestand op alleen-voor-jezelf:

```
chmod 600 tokens.json
```

### Stap 12. Controleer het resultaat

De tool haalt vervolgens alle administraties op waar je account bij mag en zet de
bankstanden in een PDF in dezelfde map. Zie je de namen van je administraties
voorbijkomen, dan staat de koppeling. De PDF open je met `open` gevolgd door de
bestandsnaam, of gewoon door erop te dubbelklikken in Finder.

---

## Deel 4. Vragen stellen aan je administratie

### Stap 13. Stel je vraag

Start Claude Code in de projectmap en typ gewoon wat je wilt weten. Hij leest de
projectmap, ziet in `CLAUDE.md` welke functies er zijn, en schrijft er een klein
script omheen dat hij voor je uitvoert. Voorbeelden:

* Wat is het totale banksaldo over alle administraties, per vandaag?
* Geef me de omzet per maand in 2025 voor administratie <nummer>.
* Welke grootboekrekeningen zijn in 2025 nieuw ten opzichte van 2024?
* Zet de balans van 2025 naast die van 2024 in een tabel, met het verschil in
  procenten.
* Welke bankrekening heeft al meer dan drie maanden geen mutatie gehad?

**Begin met een vraag waarvan je het antwoord al kent.** Bijvoorbeeld het saldo
van één bankrekening op één datum. Leg dat naast Exact zelf. Klopt het, dan weet
je dat de koppeling de juiste administratie en de juiste periode pakt, en kun je
daarna vragen stellen waarvan je het antwoord niet kent.

Naast deze vrije vragen is er een vast script voor de bankstanden (`main.py`).

### Wat je Claude niet moet laten doen

De afspraak in `CLAUDE.md` is dat er alleen gelezen wordt uit Exact Online,
nooit geschreven. Vraag dus geen boekingen, correcties of mutaties. Gaat het mis
in je administratie, dan is dat via deze weg niet terug te draaien.

Laat hem ook niet de inhoud van `.env` of `tokens.json` tonen of verwerken. Daar
staan je sleutels in.

En blijf de uitkomsten controleren. Claude kan een rapportage produceren die er
verzorgd uitziet en toch op de verkeerde periode, de verkeerde administratie of
een verkeerde optelling gebaseerd is. Vraag bij twijfel om het tussenresultaat
per grootboekrekening en leg dat naast Exact zelf.

---

## Deel 5. Wat je moet weten voor daarna

**Welke administraties je ziet, hangt af van wie inlogt.** Niet van de client ID.
Mis je een administratie in de lijst, dan is dat een kwestie van rechten op je
Exact-gebruiker, niet van de app. Dat los je op in Exact Online zelf, niet in
deze tool.

**De koppeling verloopt als je hem lang niet gebruikt.** Het access token is maar
tien minuten geldig en wordt automatisch ververst. Het refresh token daarachter
vervalt na ongeveer dertig dagen zonder gebruik. Draai je de tool een maand niet,
dan vraagt hij bij de volgende run gewoon opnieuw om de autorisatie uit stap 11.

**Draai de tool niet op twee plekken tegelijk met hetzelfde account.** Exact geeft
per gebruiker en app één geldig refresh token uit en vervangt dat bij elke
verversing. Twee parallelle sessies loggen elkaar dus uit. Kopieer om dezelfde
reden `tokens.json` niet naar een tweede machine.

**Zet de projectmap niet in een map die met iCloud Drive synchroniseert**, zoals
Bureaublad of Documenten wanneer "Bureaublad- en Documentenmappen" in iCloud aan
staat. Dan belandt `tokens.json` op je andere Macs en in de cloud, en kunnen twee
apparaten elkaar via dat bestand uitloggen. Een map als `~/Projects` buiten
iCloud is veiliger.

**Er zit een limiet op het aantal API-aanroepen** per app per administratie per
dag. Bij normaal gebruik (een rapportage per dag) kom je daar niet in de buurt.
Ga je in een lus draaien, houd er dan rekening mee.

---

## Checklist

* [ ] Exact-gebruiker met beheerrechten beschikbaar
* [ ] App geregistreerd in het App Center
* [ ] Redirect URI exact `https://www.exact.com/login`
* [ ] Client ID en Client Secret veilig opgeslagen
* [ ] Regio gecontroleerd (NL, of `BASE_URL` aangepast)
* [ ] Claude Code geinstalleerd en ingelogd
* [ ] Terminal toegang gegeven tot de projectmap
* [ ] Python 3.10 of nieuwer (`python3 --version`) en de dependencies geinstalleerd
* [ ] `.env` aangemaakt met beide waarden, `chmod 600` gedaan
* [ ] `python main.py` zelf gedraaid en geautoriseerd
* [ ] Administraties zichtbaar in de output
* [ ] Projectmap staat niet in iCloud Drive
* [ ] Eerste vraag gesteld en het antwoord nagerekend in Exact
