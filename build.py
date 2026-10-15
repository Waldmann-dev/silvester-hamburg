exec(open("/home/hatch/workspace/silvester-hamburg/gen.py").read())
exec(open("/home/hatch/workspace/silvester-hamburg/gen2.py").read())

import json
routes_json = json.dumps(routes_js, ensure_ascii=False)

var_btns = "".join(
    f'<button class="btn varbtn{" active" if vid=="A" else ""}" data-v="{vid}">{VARIANT_INFO[vid]["titel"]}</button>'
    for vid in ["A", "B", "C", "D"])
var_panes = "".join(variant_panel(v) for v in routen)
budget_blocks = "".join(budget_table(vid) for vid in ["A", "B", "C", "D"])

JS = """
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const ROUTES = __ROUTES__;
const maps = {};
function showVariant(v){
  document.querySelectorAll('.varbtn').forEach(b=>b.classList.toggle('active', b.dataset.v===v));
  document.querySelectorAll('.varpane').forEach(p=>p.classList.toggle('show', p.id==='var-'+v));
  showDay(v, 0);
}
function showDay(v, d){
  document.querySelectorAll('.daybtn[data-v="'+v+'"]').forEach(b=>b.classList.toggle('active', +b.dataset.d===d));
  document.querySelectorAll('#var-'+v+' .daypane').forEach(p=>p.classList.remove('show'));
  const pane = document.getElementById('day-'+v+'-'+d);
  pane.classList.add('show');
  initMap(v, d);
}
function initMap(v, d){
  const key = v+'-'+d;
  const el = document.getElementById('map-'+key);
  if(maps[key]){ setTimeout(()=>maps[key].invalidateSize(), 100); return; }
  const pts = ROUTES[v][d].pts;
  const map = L.map(el, {scrollWheelZoom:false}).setView([53.55, 9.99], 12);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {attribution:'© OpenStreetMap · © CARTO', maxZoom:18}).addTo(map);
  if(pts.length){
    const latlngs = pts.map(p=>[p.lat, p.lon]);
    pts.forEach((p,i)=>{
      L.marker([p.lat,p.lon], {icon:L.divIcon({className:'', html:'<div class="mapnum">'+(i+1)+'</div>', iconSize:[24,24], iconAnchor:[12,12]})})
        .addTo(map).bindPopup('<b>'+p.n+'</b>'+(p.info?'<br>'+p.info:''));
    });
    if(latlngs.length>1) L.polyline(latlngs, {color:'#f5c542', weight:3, opacity:.8, dashArray:'6 6'}).addTo(map);
    map.fitBounds(L.latLngBounds(latlngs).pad(0.25));
  }
  maps[key]=map;
  setTimeout(()=>map.invalidateSize(), 150);
}
document.querySelectorAll('.varbtn').forEach(b=>b.addEventListener('click', ()=>showVariant(b.dataset.v)));
document.querySelectorAll('.daybtn').forEach(b=>b.addEventListener('click', ()=>showDay(b.dataset.v, +b.dataset.d)));
document.querySelectorAll('.gotoplan').forEach(b=>b.addEventListener('click', ()=>{
  showVariant(b.dataset.v);
  document.getElementById('reiseplan').scrollIntoView({behavior:'smooth'});
}));
showVariant('A');
</script>
""".replace("__ROUTES__", routes_json)

html_doc = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Silvester in Hamburg 2026/27 — ab München, Budget</title>
""" + CSS + """
</head>
<body>

<header class="hero">
  <div class="bg"></div>
  <div class="inner">
    <div class="kicker">Silvester 2026/27 · ab München · Budget</div>
    <h1>Silvester in <span class="gold">Hamburg</span></h1>
    <p class="sub">2–3 Tage Hafen, Kiez &amp; König der Löwen — mit Tagesplänen, Karten, Food-Guide, echten Hotelpreisen und Budgets pro Variante.</p>
    <div class="tabs" style="justify-content:center;margin-top:22px">
      <button class="btn gotoplan" data-v="A">Mi 30.12. → Fr 01.01.</button>
      <button class="btn gotoplan" data-v="B">Do 31.12. → Sa 02.01.</button>
      <button class="btn gotoplan" data-v="C">Mi 30.12. → Sa 02.01.</button>
      <button class="btn gotoplan" data-v="D">Do 31.12. → So 03.01.</button>
    </div>
  </div>
</header>

<div class="wrap">

<section id="reiseplan">
  <h2>🗺️ Dein Reiseplan</h2>
  <p class="sec-sub">Variante wählen, dann Tag für Tag durchklicken — jeder Tag mit Ablauf und eigener Karte mit den Stationen als Route.</p>
  <div class="tabs">
    """ + var_btns + """
  </div>
  """ + var_panes + """
  <div class="note"><strong>Zug-Alternative für alle Varianten (Trainline, 15.10.2026 nachmittags, 1 Pers., 2. Klasse, Super Sparpreis):</strong> ICE München–Hamburg ca. 5:40–6 h. Günstigste Hin+Rück-Gesamtpreise (jeweils günstigste Morgenverbindung): A (30.12./01.01.) <strong>57,98 €</strong> · B/C/D je <strong>69,98 €</strong>. Einzelpreise: hin 30.12. ICE 886, 06:18 → 11:58, direkt, 39,99 € · hin 31.12. 06:29 → 12:24, ICE 1604 + RJ 384, 1 Umstieg Berlin Hbf, 39,99 € (direkt ICE 886, 06:18 → 11:58, 55,99 €) · zurück 01.01. ICE 783, 06:01 → 11:42, direkt, 17,99 € · zurück 02./03.01. ICE 783, 06:01 → 11:42, direkt, 29,99 €. Trainline zeigt nur die schnellsten Verbindungen mit den wenigsten Umstiegen — langsamere/günstigere mit mehr Umstiegen ggf. nicht enthalten; eine eventuelle Trainline-Buchungsgebühr ist in den Preisen nicht bestätigt enthalten. bahn.de hat die Abfrage am 15.10. mit Bot-Sperre blockiert, der ÖBB-Ticketshop ebenfalls (Cloudflare-Schleife) — Preise dort ggf. auf eigenem Gerät prüfen. Probe BahnCard 25: 17,90 €/3 Monate. ÖBB Nightjet NJ40420 (22:52 → 08:47, Sitz ab 34,90 €, Liege ab 54,90 €) spart eine Hotel-Nacht — Verkauf läuft bereits.</div>
</section>

""" + FIREWORKS + ELBPHI_3D + HIGHLIGHTS + MUSEUMS + FOOD + HOTELS + """

<section>
  <h2>💰 Gesamtbudget pro Variante</h2>
  <p class="sec-sub">Alle Preise als Einzelposten (keine Pauschalen). (S) = Schätzung. Flugpreise: Momondo-Round-Trip-Preise vom 15.10.2026 nachmittags (Hin+Rück als buchbare Einheit, via Drittanbieter; Direktpreise bei Lufthansa 3–5 € höher). Alle Flugpreise Economy Basic OHNE Aufgabegepäck (nur kleiner persönlicher Gegenstand) — mit 23 kg Aufgabegepäck (Comfort) deutlich teurer. Zugpreise: Trainline 15.10.2026. Stand: 15.10.2026.</p>
  """ + budget_blocks + """
  <div class="card">
    <h3>Vergleich (Basis, ohne Hotel, ohne Party)</h3>
    <table>
      <tr><th>Variante</th><th>Anreise</th><th>Aktivitäten</th><th>Essen</th><th>Nahverkehr</th><th>Gesamt</th></tr>
      <tr><td><strong>A (2 Tage)</strong></td><td>211,00 €</td><td>115,89 €</td><td>64,20 €</td><td>24,60 €</td><td><span class="price"><strong>≈ 416 €</strong></span></td></tr>
      <tr><td><strong>B (2 Tage)</strong></td><td>203,00 €</td><td>127,39 €</td><td>79,20 €</td><td>24,60 €</td><td><span class="price"><strong>≈ 434 €</strong></span></td></tr>
      <tr><td><strong>C (3 Tage)</strong></td><td>200,00 €</td><td>145,89 €</td><td>101,20 €</td><td>32,80 €</td><td><span class="price"><strong>≈ 480 €</strong></span></td></tr>
      <tr><td><strong>D (3 Tage)</strong></td><td>161,00 €</td><td>141,39 €</td><td>106,20 €</td><td>32,80 €</td><td><span class="price"><strong>≈ 441 €</strong></span></td></tr>
    </table>
    <p class="est">zzgl. Hotel — verifizierte Silvester-Preise (15.10.) z. B.: a&amp;o City Dorm (b) 42,64 € / (d) 58,00 € · a&amp;o Hbf Dorm (b) 50,00 € / (d) 64,66 € · Generator (b) 50,15 € · MEININGER (b) 86,00 €, (d) ausverkauft · ibis budget (b) 244,80 € / (d) 310,89 €.</p>
  </div>
</section>

</div>

<footer>
  Stand: 15.10.2026 · Zugpreise: Trainline, verifiziert 15.10. (bahn.de + ÖBB-Ticketshop blockiert) · Flugpreise: Momondo + Lufthansa, verifiziert 15.10. nachmittags · Hotelpreise ibis budget live verifiziert, übrige im Live-Check · (S) = Schätzung — vor Buchung prüfen.<br>
  Bilder: Wikimedia Commons (CC-Lizenzen) · 3D-Modell: Holocreators/Richtig-Druck via Sketchfab · Karte: © OpenStreetMap · © CARTO<br>
  Alle Angaben ohne Gewähr. Nichts gebucht.
</footer>

""" + JS + """
</body>
</html>
"""

open("/home/hatch/workspace/silvester-hamburg/index.html", "w").write(html_doc)
print("index.html geschrieben:", len(html_doc), "Zeichen")
