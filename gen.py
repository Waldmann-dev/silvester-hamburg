#!/usr/bin/env python3
"""Generiert index.html für die Hamburg-Silvester-Seite aus den Recherche-Dateien."""
import json, html, re

BASE = "/home/hatch/workspace/silvester-hamburg"
routen = json.load(open(f"{BASE}/tagesrouten.json"))["varianten"]
locs = json.load(open(f"{BASE}/locations.json"))

MANUAL = {
    "landungsbrücken": (53.5464, 9.9669, "Landungsbrücken"),
    "reeperbahn": (53.5495, 9.9590, "Reeperbahn"),
    "schanze": (53.5641, 9.9640, "Sternschanze"),
    "speicherstadt": (53.5444, 9.9989, "Speicherstadt (Wasserschloss)"),
    "theater im hafen": (53.5442, 9.9725, "Stage Theater im Hafen (König der Löwen)"),
    "könig der löwen": (53.5442, 9.9725, "Stage Theater im Hafen (König der Löwen)"),
    "blankenese": (53.5565, 9.8110, "Blankenese Treppenviertel"),
    "fischmarkt": (53.5456, 9.9537, "Fischmarkt Altona"),
    "portugiesenviertel": (53.5467, 9.9630, "Portugiesenviertel (Ditmar-Koel-Straße)"),
    "hbf": (53.5528, 10.0067, "Hamburg Hauptbahnhof"),
    "flughafen": (53.6304, 9.9882, "Flughafen Hamburg"),
}

def norm(s):
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    return s.strip()

LOC = {}
for l in locs:
    LOC[norm(l["name"])] = l
for k, (lat, lon, name) in MANUAL.items():
    LOC[k] = {"name": name, "lat": lat, "lon": lon, "kurzinfo": "", "kategorie": "manuell"}

def find_coord(station_name):
    n = norm(station_name)
    # explizite Overrides vor Fuzzy-Matching
    if "michel" in n and "motel" not in n:
        l = LOC[norm("St. Michaelis (Michel)")]
        return l["lat"], l["lon"], l["name"]
    if "brücke 10" in n:
        lat, lon, _ = MANUAL["landungsbrücken"]
        return lat, lon, "Brücke 10 (Landungsbrücken)"
    if n in LOC:
        l = LOC[n]
        return l["lat"], l["lon"], l["name"]
    for key, l in LOC.items():
        if l.get("kategorie") == "hotel":
            continue  # Hotels sind keine Routen-Stationen
        if len(key) > 4 and (key in n or n in key):
            return l["lat"], l["lon"], l["name"]
    return None

SKIP = {"flug", "s1", "hotel", "check-in", "abendessen", "frühstück", "mittag", "ausschlafen",
        "silvesternacht", "hvv", "nacht", "rückflug", "anreise"}

def map_station(st):
    name = st["name"]
    nl = norm(name)
    if any(s in nl for s in SKIP):
        return None
    # Spezialfälle
    if "elbtunnel" in nl: return ("Alter Elbtunnel",)
    c = find_coord(name)
    if c:
        return (c[2], c[0], c[1], st.get("kurzinfo", ""))
    return None

# Routen-Daten für JS aufbereiten
routes_js = {}
for v in routen:
    days = []
    for di, tag in enumerate(v["tage"]):
        pts = []
        for st in tag["stationen"]:
            m = map_station(st)
            if m:
                if len(m) == 1:
                    l = LOC[norm("alter elbtunnel")]
                    pts.append({"n": st["name"], "lat": l["lat"], "lon": l["lon"], "info": st.get("kurzinfo", "")})
                else:
                    pts.append({"n": m[0], "lat": m[1], "lon": m[2], "info": st.get("kurzinfo", "")})
        days.append({"tag": tag["tag"], "pts": pts})
    routes_js[v["id"]] = days

VARIANT_INFO = {
    "A": {"titel": "Mi 30.12. → Fr 01.01.", "unter": "2 Tage · Anreise Mi abends",
          "flug": "LH2078, MUC 18:45 → HAM 20:05 / LH2059, HAM 10:55 → MUC 12:10 · <strong>ab ca. 211 €</strong> (Momondo 15.10. nachm., via Opodo; 215,66 € direkt bei Lufthansa) — Economy Basic, OHNE Aufgabegepäck",
          "flug_alt": "Morgens: LH2062 (11:30 → 12:50) / LH2063 (13:35 → 14:50) ab 214 € (+3 €) · Frühester: LH2054 (07:45 → 09:05) / VL2071 (16:35 → 17:50) ab 221 € · Mit 23 kg Aufgabegepäck (Comfort): ca. 274 €",
          "zug": "ICE hin 30.12. + zurück 01.01. (Trainline 15.10., Super Sparpreis): hin ICE 886, 06:18 → 11:58, direkt, 39,99 € · zurück ICE 783, 06:01 → 11:42, direkt, 17,99 € · Gesamt nur 57,98 € · Nightjet 30.12. abends → 31.12. morgens: spart eine Hotelnacht (Sitz ab 34,90 €)"},
    "B": {"titel": "Do 31.12. → Sa 02.01.", "unter": "2 Tage · direkt an Silvester",
          "flug": "LH4114 (City Airlines), MUC 15:00 → HAM 16:20 / LH2059, HAM 10:55 → MUC 12:10 · <strong>ab ca. 203 €</strong> (Momondo 15.10. nachm., via Expedia; 208,66 € direkt bei Lufthansa) — Economy Basic, OHNE Aufgabegepäck",
          "flug_alt": "Morgens: EW7171 (09:15 → 10:35) / LH2059 ab 207 € (+4 €) · LH-Alternative LH2062 (11:30 → 12:50) / LH2059 ab 209 € · Mit Aufgabegepäck ab 286 € (Kiwi.com)",
          "zug": "ICE hin 31.12. + zurück 02.01. (Trainline 15.10., Super Sparpreis): hin 06:29 → 12:24, ICE 1604 + RJ 384, 1 Umstieg Berlin Hbf, 39,99 € (direkt ICE 886, 06:18 → 11:58, 55,99 €) · zurück ICE 783, 06:01 → 11:42, direkt, 29,99 € · Gesamt 69,98 € · Nightjet 31.12. (22:52 → 08:47): direkt in die Silvesternacht (Sitz ab 34,90 €)"},
    "C": {"titel": "Mi 30.12. → Sa 02.01.", "unter": "3 Tage · entspannteste Variante",
          "flug": "LH2078, MUC 18:45 → HAM 20:05 / LH2059, HAM 10:55 → MUC 12:10 · <strong>ab ca. 200 €</strong> (Momondo 15.10. nachm.; ~204–205 € direkt bei Lufthansa) — Economy Basic, OHNE Aufgabegepäck",
          "flug_alt": "Morgens: LH2062 (11:30 → 12:50) / LH2059 ab 203 € (+3 €) · Frühester: LH2054 (07:45 → 09:05) / LH2059 ab 210 €",
          "zug": "ICE hin 30.12. + zurück 02.01. (Trainline 15.10., Super Sparpreis): hin ICE 886, 06:18 → 11:58, direkt, 39,99 € · zurück ICE 783, 06:01 → 11:42, direkt, 29,99 € · Gesamt 69,98 € · Nightjet 30.12. (22:52 → 08:47): Anreise + volle 3 Tage vor Ort (Liege ab 54,90 €)"},
    "D": {"titel": "Do 31.12. → So 03.01.", "unter": "3 Tage · Rückflug Sonntag",
          "flug": "LH2054, MUC 07:45 → HAM 09:05 / LH2079, HAM 20:50 → MUC 22:05 · <strong>ab ca. 161 €</strong> (Momondo 15.10. nachm.; 165,66 € direkt bei Lufthansa) — Economy Basic, OHNE Aufgabegepäck; günstigste = Morgenflug, kein Aufpreis",
          "flug_alt": "Alternativen morgens: EW7171 (09:15 → 10:35) / EW7174 (19:10 → 20:25) ab 166 € · LH2062 (11:30 → 12:50) / LH2079 ab 171 € · Mit Aufgabegepäck ab 215 € (Mytrip/Eurowings). Das Eurowings-Angebot (138 €, Stand 10.10.) ist nicht mehr verfügbar.",
          "zug": "ICE hin 31.12. + zurück 03.01. (Trainline 15.10., Super Sparpreis): hin 06:29 → 12:24, ICE 1604 + RJ 384, 1 Umstieg Berlin Hbf, 39,99 € (direkt ICE 886, 06:18 → 11:58, 55,99 €) · zurück ICE 783, 06:01 → 11:42, direkt, 29,99 € · Gesamt 69,98 € · Nightjet 31.12. (22:52 → 08:47): direkt in die Silvesternacht (Sitz ab 34,90 €)"},
}

BUDGETS = {
 "A": {"titel": "Variante A · Mi 30.12. → Fr 01.01. (2 Tage)",
       "rows": [
        ("Anreise", "Flug MUC→HAM→MUC Round-Trip (LH nonstop)", "211,00 €"),
        ("Aktivitäten", "König der Löwen 31.12. 17:00 (ab-Preis, verifiziert 10.10.)", "74,39 €"),
        ("Aktivitäten", "Dialog im Dunkeln (ab-Preis)", "18,50 €"),
        ("Aktivitäten", "Int. Maritimes Museum (01.01., verifiziert 10.10.)", "18,00 €"),
        ("Aktivitäten", "Elbphilharmonie Plaza (seit 05.10. kostenpflichtig)", "5,00 €"),
        ("Aktivitäten", "Elbtunnel / Fähre 62 / Speicherstadt / Reeperbahn-Bummel", "0,00 €"),
        ("Essen & Trinken", "Abendessen Tag 1 (Kiez Curry / Portugiesenviertel) (S)", "14,00 €"),
        ("Essen & Trinken", "Mittag Tag 2 (Fischbrötchen Brücke 10)", "6,00 €"),
        ("Essen & Trinken", "Abendessen Tag 2 (Labskaus) (S)", "22,00 €"),
        ("Essen & Trinken", "Frühstück Tag 3 (Franzbrötchen) (S)", "3,00 €"),
        ("Essen & Trinken", "Mittag Tag 3 (Portugiesenviertel) (S)", "15,00 €"),
        ("Essen & Trinken", "Cappuccino", "4,20 €"),
        ("Nahverkehr", "HVV Tagesticket 8,20 € × 3 Tage", "24,60 €"),
       ],
       "sub": "Anreise 211,00 € · Aktivitäten 115,89 € · Essen & Trinken 64,20 € · Nahverkehr 24,60 €",
       "total": "≈ 416 €",
       "extra": "zzgl. Hotel (2 Nächte) — echte Silvester-Preise werden gerade live geprüft",
       "opt": "Aufpreis-Optionen: Karoline All-Inclusive +105,01 € → ≈ 521 € · Kieztour +25 € (S) → ≈ 441 € · Anreise-Alternativen: ICE 57,98 € (Trainline 15.10.) · Nightjet ~69,80 € (S)"},
 "B": {"titel": "Variante B · Do 31.12. → Sa 02.01. (2 Tage)",
       "rows": [
        ("Anreise", "Flug MUC→HAM→MUC Round-Trip (LH nonstop)", "203,00 €"),
        ("Aktivitäten", "König der Löwen 31.12. 17:00 (ab-Preis, verifiziert 10.10.)", "74,39 €"),
        ("Aktivitäten", "Int. Maritimes Museum (01.01., verifiziert 10.10.)", "18,00 €"),
        ("Aktivitäten", "Miniatur Wunderland (S)", "22,00 €"),
        ("Aktivitäten", "Michel Turm", "8,00 €"),
        ("Aktivitäten", "Elbphilharmonie Plaza (seit 05.10. kostenpflichtig)", "5,00 €"),
        ("Aktivitäten", "Elbtunnel / Fähre 62 / Speicherstadt / Schanze / Chilehaus", "0,00 €"),
        ("Essen & Trinken", "Abendessen Tag 1 (Labskaus Old Commercial Room) (S)", "25,00 €"),
        ("Essen & Trinken", "Frühstück Tag 2 (S)", "10,00 €"),
        ("Essen & Trinken", "Mittag Tag 2 (Portugiesenviertel) (S)", "18,00 €"),
        ("Essen & Trinken", "Abendessen Tag 2 (S)", "18,00 €"),
        ("Essen & Trinken", "Frühstück Tag 3 (Franzbrötchen) (S)", "4,00 €"),
        ("Essen & Trinken", "Cappuccino", "4,20 €"),
        ("Nahverkehr", "HVV Tagesticket 8,20 € × 3 Tage", "24,60 €"),
       ],
       "sub": "Anreise 203,00 € · Aktivitäten 127,39 € · Essen & Trinken 79,20 € · Nahverkehr 24,60 €",
       "total": "≈ 434 €",
       "extra": "zzgl. Hotel (2 Nächte) — echte Silvester-Preise werden gerade live geprüft",
       "opt": "Aufpreis-Optionen: Karoline All-Inclusive +105,01 € → ≈ 539 € · Kieztour +25 € (S) → ≈ 459 € · Anreise-Alternativen: ICE 69,98 € (Trainline 15.10.) · Nightjet ~69,80 € (S)"},
 "C": {"titel": "Variante C · Mi 30.12. → Sa 02.01. (3 Tage)",
       "rows": [
        ("Anreise", "Flug MUC→HAM→MUC Round-Trip (LH nonstop)", "200,00 €"),
        ("Aktivitäten", "König der Löwen 31.12. 17:00 (ab-Preis, verifiziert 10.10.)", "74,39 €"),
        ("Aktivitäten", "Dialog im Dunkeln (ab-Preis)", "18,50 €"),
        ("Aktivitäten", "Int. Maritimes Museum (01.01., verifiziert 10.10.)", "18,00 €"),
        ("Aktivitäten", "Miniatur Wunderland (S)", "22,00 €"),
        ("Aktivitäten", "Michel Turm", "8,00 €"),
        ("Aktivitäten", "Elbphilharmonie Plaza (seit 05.10. kostenpflichtig)", "5,00 €"),
        ("Aktivitäten", "Blankenese / Elbtunnel / Fähre 62 / Speicherstadt / Schanze / Gängeviertel", "0,00 €"),
        ("Essen & Trinken", "Abendessen Tag 1 (S)", "14,00 €"),
        ("Essen & Trinken", "Mittag Tag 2 (Fischbrötchen)", "6,00 €"),
        ("Essen & Trinken", "Abendessen Tag 2 (Labskaus) (S)", "22,00 €"),
        ("Essen & Trinken", "Frühstück Tag 3 (S)", "10,00 €"),
        ("Essen & Trinken", "Mittag Tag 3 (Portugiesenviertel) (S)", "18,00 €"),
        ("Essen & Trinken", "Abendessen Tag 3 (S)", "18,00 €"),
        ("Essen & Trinken", "Mittag Tag 4 (Fischbrötchen Övelgönne) (S)", "6,00 €"),
        ("Essen & Trinken", "Franzbrötchen (S)", "3,00 €"),
        ("Essen & Trinken", "Cappuccino (S)", "4,20 €"),
        ("Nahverkehr", "HVV Tagesticket 8,20 € × 4 Tage", "32,80 €"),
       ],
       "sub": "Anreise 200,00 € · Aktivitäten 145,89 € · Essen & Trinken 101,20 € · Nahverkehr 32,80 €",
       "total": "≈ 480 €",
       "extra": "zzgl. Hotel (3 Nächte) — echte Silvester-Preise werden gerade live geprüft",
       "opt": "Aufpreis-Optionen: Karoline All-Inclusive +105,01 € → ≈ 585 € · Kieztour +25 € (S) → ≈ 505 € · Anreise-Alternativen: ICE 69,98 € (Trainline 15.10.) · Nightjet ~69,80 € (S)"},
 "D": {"titel": "Variante D · Do 31.12. → So 03.01. (3 Tage)",
       "rows": [
        ("Anreise", "Flug MUC→HAM→MUC Round-Trip (Lufthansa nonstop, Momondo 15.10., via Expedia)", "161,00 €"),
        ("Aktivitäten", "König der Löwen 31.12. 17:00 (ab-Preis, verifiziert 10.10.)", "74,39 €"),
        ("Aktivitäten", "Int. Maritimes Museum (01.01., verifiziert 10.10.)", "18,00 €"),
        ("Aktivitäten", "Miniatur Wunderland (S)", "22,00 €"),
        ("Aktivitäten", "Michel Turm", "8,00 €"),
        ("Aktivitäten", "Elbphilharmonie Plaza (seit 05.10. kostenpflichtig)", "5,00 €"),
        ("Aktivitäten", "Deichtorhallen (03.01.)", "14,00 €"),
        ("Aktivitäten", "Blankenese / Gängeviertel / Elbtunnel / Fähre 62 / Schanze", "0,00 €"),
        ("Essen & Trinken", "Abendessen Tag 1 (Labskaus Old Commercial Room) (S)", "25,00 €"),
        ("Essen & Trinken", "Frühstück Tag 2 (S)", "10,00 €"),
        ("Essen & Trinken", "Mittag Tag 2 (Portugiesenviertel) (S)", "18,00 €"),
        ("Essen & Trinken", "Abendessen Tag 2 (S)", "18,00 €"),
        ("Essen & Trinken", "Mittag Tag 3 (Fischbrötchen Nuggi's) (S)", "6,00 €"),
        ("Essen & Trinken", "Abendessen Tag 3 (Labskaus Krameramtsstuben) (S)", "22,00 €"),
        ("Essen & Trinken", "Frühstück Tag 4 (Franzbrötchen) (S)", "3,00 €"),
        ("Essen & Trinken", "Cappuccino (S)", "4,20 €"),
        ("Nahverkehr", "HVV Tagesticket 8,20 € × 4 Tage", "32,80 €"),
       ],
       "sub": "Anreise 161,00 € · Aktivitäten 141,39 € · Essen & Trinken 106,20 € · Nahverkehr 32,80 €",
       "total": "≈ 441 €",
       "extra": "zzgl. Hotel (3 Nächte 31.12./01.01./02.01.) — z. B. a&o Hbf Dorm 64,66 € (verifiziert)",
       "opt": "Aufpreis-Optionen: Karoline All-Inclusive +105,01 € → ≈ 546 € · Kieztour +25 € (S) → ≈ 466 € · Anreise-Alternativen: ICE 69,98 € (Trainline 15.10.) · Nightjet ~69,80 € (S)"},
}

# ---------- HTML ----------
def esc(s): return html.escape(s, quote=True)

CSS = """<style>
:root{
  --bg:#0b1026; --bg2:#111737; --card:#1a2148; --card2:#202a5c;
  --gold:#f5c542; --gold2:#ffe08a; --text:#eef1ff; --muted:#aab0d6;
  --accent:#5aa9ff; --green:#4ade80; --red:#f87171;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:linear-gradient(180deg,var(--bg),var(--bg2));color:var(--text);line-height:1.6}
.wrap{max-width:1020px;margin:0 auto;padding:0 20px}
header.hero{position:relative;text-align:center;padding:110px 20px 70px;overflow:hidden}
header.hero .bg{position:absolute;inset:0;background:url('img/hero-elbphi.jpg') center 30%/cover;filter:brightness(.45) saturate(1.1)}
header.hero .inner{position:relative;z-index:2}
.kicker{color:var(--gold);letter-spacing:3px;text-transform:uppercase;font-size:13px;font-weight:700}
h1{font-size:clamp(34px,6vw,58px);margin:12px 0 8px;line-height:1.15;text-shadow:0 2px 24px rgba(0,0,0,.6)}
h1 .gold{color:var(--gold)}
.sub{color:#dfe4ff;font-size:18px;max-width:660px;margin:0 auto;text-shadow:0 1px 12px rgba(0,0,0,.7)}
section{padding:40px 0}
h2{font-size:27px;margin-bottom:6px;color:var(--gold)}
.sec-sub{color:var(--muted);margin-bottom:20px;max-width:760px}
.sec-img{width:100%;height:220px;object-fit:cover;border-radius:14px;margin-bottom:18px;border:1px solid rgba(255,255,255,.1)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.card{background:var(--card);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:20px;transition:transform .15s}
.card:hover{transform:translateY(-2px)}
.card h3{font-size:18px;margin-bottom:8px}
.card p{color:var(--muted);font-size:15px}
.price{color:var(--green);font-weight:700;font-size:18px}
.tag{display:inline-block;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;margin-bottom:10px}
.tag.best{background:rgba(74,222,128,.15);color:var(--green);border:1px solid rgba(74,222,128,.4)}
.tag.info{background:rgba(90,169,255,.15);color:var(--accent);border:1px solid rgba(90,169,255,.4)}
.tag.warn{background:rgba(245,197,66,.15);color:var(--gold2);border:1px solid rgba(245,197,66,.4)}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.btn{display:inline-block;margin:10px 8px 0 0;background:var(--gold);color:#1a1405;font-weight:700;padding:10px 20px;border-radius:10px;font-size:15px;cursor:pointer;border:none}
.btn:hover{text-decoration:none;filter:brightness(1.08)}
.btn2{display:inline-block;margin:8px 8px 0 0;border:1px solid var(--gold);color:var(--gold2);font-weight:700;padding:9px 18px;border-radius:10px;font-size:14px;cursor:pointer;background:transparent}
.btn2:hover{text-decoration:none;background:rgba(245,197,66,.12)}
.btn2.active,.btn.active{background:var(--gold);color:#1a1405}
ul{margin:8px 0 8px 20px;color:var(--muted);font-size:15px}
li{margin-bottom:6px}
.est{font-size:13px;color:var(--muted);font-style:italic}
table{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}
th,td{text-align:left;padding:10px 8px;border-bottom:1px solid rgba(255,255,255,.08);vertical-align:top}
th{color:var(--gold);font-size:13px;text-transform:uppercase;letter-spacing:1px}
td{color:var(--muted)}
td strong,td b{color:var(--text)}
footer{text-align:center;color:var(--muted);font-size:13px;padding:36px 20px 48px;border-top:1px solid rgba(255,255,255,.08)}
.note{background:rgba(245,197,66,.08);border-left:3px solid var(--gold);padding:14px 18px;border-radius:0 10px 10px 0;color:var(--muted);font-size:15px;margin:16px 0}
.subh{color:var(--gold2);font-size:17px;margin:22px 0 10px;font-weight:700}
.hl{font-size:14px}.hl strong{color:var(--text)}.hl p{margin-top:4px}
.tabs{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 18px}
.tabpane{display:none}.tabpane.show{display:block}
/* Timeline */
.timeline{list-style:none;margin:0;padding:0}
.timeline li{position:relative;padding:0 0 18px 28px;margin:0}
.timeline li::before{content:attr(data-n);position:absolute;left:0;top:2px;width:20px;height:20px;border-radius:50%;background:var(--gold);color:#1a1405;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.timeline li::after{content:"";position:absolute;left:9px;top:26px;bottom:0;width:2px;background:rgba(245,197,66,.25)}
.timeline li:last-child::after{display:none}
.timeline .t{font-weight:700;color:var(--text)}
.timeline .d{color:var(--muted);font-size:14px}
.timeline .k{color:var(--green);font-size:14px;font-weight:600}
/* Leaflet */
.daymap{height:340px;border-radius:14px;margin:14px 0;border:1px solid rgba(255,255,255,.12);z-index:1}
.leaflet-container{font-family:inherit;background:#0b1026}
.mapnum{background:var(--gold);color:#1a1405;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;border:2px solid #fff}
/* 3D embed */
.embed16x9{position:relative;width:100%;padding-bottom:56.25%;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.12);margin:14px 0}
.embed16x9 iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.badge{display:inline-block;font-size:11px;font-weight:700;padding:2px 9px;border-radius:999px;margin-left:8px;vertical-align:middle}
.badge.ok{background:rgba(74,222,128,.15);color:var(--green)}
.badge.warnb{background:rgba(245,197,66,.15);color:var(--gold2)}
.badge.info{background:rgba(90,169,255,.15);color:var(--accent)}
.cathead td{color:var(--gold2);font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:1px;padding-top:14px}
.totalrow td{font-size:18px;border-top:2px solid var(--gold)}
@media(max-width:640px){.daymap{height:280px}}
</style>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
"""

def variant_panel(v):
    vid = v["id"]; info = VARIANT_INFO[vid]
    days = routes_js[vid]
    day_btns = "".join(
        f'<button class="btn2 daybtn{" active" if i==0 else ""}" data-v="{vid}" data-d="{i}">{esc(d["tag"].split("—")[0].strip())}</button>'
        for i, d in enumerate(days))
    panes = []
    for i, d in enumerate(days):
        items = []
        for j, st in enumerate(v["tage"][i]["stationen"]):
            items.append(
                f'<li data-n="{j+1}"><span class="t">{esc(st["name"])}</span>'
                + (f' <span class="k">{esc(st["kosten"])}</span>' if st.get("kosten") else "")
                + (f'<div class="d">{esc(st.get("dauer",""))}{" · " if st.get("dauer") and st.get("kurzinfo") else ""}{esc(st.get("kurzinfo",""))}</div>' if st.get("dauer") or st.get("kurzinfo") else "")
                + '</li>')
        panes.append(
            f'<div class="tabpane daypane{" show" if i==0 else ""}" id="day-{vid}-{i}">'
            f'<h3 style="margin:6px 0 10px">{esc(d["tag"])}</h3>'
            f'<ul class="timeline">{"".join(items)}</ul>'
            f'<div class="daymap" id="map-{vid}-{i}"></div>'
            f'<p class="est">Route des Tages auf der Karte — Nummern folgen dem Ablauf.</p>'
            f'</div>')
    return f"""
<div class="tabpane varpane{" show" if vid=="A" else ""}" id="var-{vid}">
  <div class="card" style="margin-bottom:16px">
    <span class="tag {"best" if vid=="D" else "info"}">{"Günstigster Flug" if vid=="D" else "Variante "+vid}</span>
    <h3>✈️ {esc(info["titel"])} <span class="est">— {esc(info["unter"])}</span></h3>
    <p>{info["flug"]}<br><span class="est">{esc(info["flug_alt"])}</span></p>
    <a class="btn" href="https://www.lufthansa.com" target="_blank" rel="noopener">Flug buchen</a>
    <p style="margin-top:14px">🚆 <strong>Zug-Alternative:</strong> {esc(info["zug"])}</p>
    <a class="btn2" href="https://www.bahn.de" target="_blank" rel="noopener">DB prüfen</a>
    <a class="btn2" href="https://www.nightjet.com" target="_blank" rel="noopener">Nightjet prüfen</a>
  </div>
  <div class="tabs">{"".join(day_btns)}</div>
  {"".join(panes)}
</div>"""

def budget_table(vid):
    b = BUDGETS[vid]
    rows = []; lastcat = None
    for cat, posten, preis in b["rows"]:
        if cat != lastcat:
            rows.append(f'<tr class="cathead"><td colspan="2">{esc(cat)}</td><td></td></tr>')
            lastcat = cat
        rows.append(f'<tr><td>{esc(posten)}</td><td></td><td style="white-space:nowrap"><strong>{esc(preis)}</strong></td></tr>')
    rows.append(f'<tr><td colspan="3" class="est">{esc(b["sub"])}</td></tr>')
    rows.append(f'<tr class="totalrow"><td><strong>GESAMT (Basis)</strong></td><td></td><td><span class="price"><strong>{esc(b["total"])}</strong></span></td></tr>')
    return f"""
<div class="card" style="margin-bottom:16px">
  <h3>{esc(b["titel"])}</h3>
  <table><tr><th>Posten</th><th></th><th>Preis</th></tr>{"".join(rows)}</table>
  <p class="est" style="margin-top:8px">{esc(b["extra"])}</p>
  <p class="est">{esc(b["opt"])}</p>
</div>"""
