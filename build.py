exec(open("/home/hatch/workspace/silvester-hamburg/gen.py").read())
exec(open("/home/hatch/workspace/silvester-hamburg/gen2.py").read())

import json
routes_json = json.dumps(routes_js, ensure_ascii=False)

var_btns = "".join(
    f'<button class="btn varbtn{" active" if vid=="A" else ""}" data-v="{vid}">{VARIANT_INFO[vid]["titel"]}</button>'
    for vid in ["A", "B", "C", "D"])
var_panes = "".join(variant_panel(v) for v in routen)
budget_blocks = "".join(budget_table(vid) for vid in ["A", "B", "C", "D"])

ANREISE_DETAIL = """
<section id="anreise-detail">
  <h2>🚆✈️ Anreise im Detail</h2>
  <p class="sec-sub">Alle Flug- und Bahn-Optionen mit Zeiten, Flug-/Zugnummern und Preisen. Stand: 15.10.2026 nachmittags. Alle Preise pro Person (1 Erwachsener).</p>

  <h3>✈️ Flüge München → Hamburg → München (nur Direktflüge)</h3>
  <p class="sec-sub">Quelle: Momondo + lufthansa.com (Skyscanner-Stichprobe nur Variante A). Round-Trip-Gesamtpreis inkl. Steuern/Gebühren. Alle Optionen Economy Basic OHNE Aufgabegepäck (siehe Gepäck-Hinweis unten). Preise dynamisch — während der Recherche: D 165 € → 161 €, C 204 € → 200 €.</p>

  <div class="card">
    <h3>Variante A · Mi 30.12.2026 → Fr 01.01.2027</h3>
    <table>
      <tr><th>Option</th><th>Hin (MUC → HAM)</th><th>Zurück (HAM → MUC)</th><th>Preis</th><th>Quelle</th></tr>
      <tr><td><strong>Günstigste insgesamt</strong></td><td>LH2078, 30.12., 18:45 → 20:05</td><td>LH2059, 01.01., 10:55 → 12:10</td><td><strong>211 €</strong></td><td>Momondo via Opodo; LH direkt 215,66 €</td></tr>
      <tr><td><strong>Günstigste morgens</strong></td><td>LH2062, 30.12., 11:30 → 12:50</td><td>LH2063, 01.01., 13:35 → 14:50</td><td><strong>214 €</strong> (+3 €)</td><td>Momondo; LH direkt 218,66 €</td></tr>
      <tr><td>Alternative (frühester)</td><td>LH2054, 30.12., 07:45 → 09:05</td><td>VL2071, 01.01., 16:35 → 17:50</td><td>221 €</td><td>Momondo</td></tr>
      <tr><td>Alternative (Eurowings)</td><td>EW, 30.12., 09:15 → 10:35</td><td>EW, 01.01., 19:10 → 20:25</td><td>245 €</td><td>Momondo</td></tr>
    </table>
    <p class="est">Zum Preis von 211 € auch mit Rückflug 13:35 (LH2063), 16:35 (VL2071) oder 19:35 (LH2077). Skyscanner-Cross-Check: direkt ab 215 €, morgens ab 217 €.</p>
  </div>

  <div class="card">
    <h3>Variante B · Do 31.12.2026 → Sa 02.01.2027</h3>
    <table>
      <tr><th>Option</th><th>Hin (MUC → HAM)</th><th>Zurück (HAM → MUC)</th><th>Preis</th><th>Quelle</th></tr>
      <tr><td><strong>Günstigste insgesamt</strong></td><td>LH4114 (City Airlines), 31.12., 15:00 → 16:20</td><td>LH2059, 02.01., 10:55 → 12:10</td><td><strong>203 €</strong></td><td>Momondo via Expedia; LH direkt 208,66 €</td></tr>
      <tr><td><strong>Günstigste morgens</strong></td><td>EW7171, 31.12., 09:15 → 10:35</td><td>LH2059, 02.01., 10:55 → 12:10</td><td><strong>207 €</strong> (+4 €)</td><td>Momondo via Opodo; mit Aufgabegepäck ab 286 € (Kiwi.com)</td></tr>
      <tr><td>Alternative (LH, morgens)</td><td>LH2062, 31.12., 11:30 → 12:50</td><td>LH2059, 02.01., 10:55 → 12:10</td><td>209 €</td><td>Momondo; LH direkt 214,66 €</td></tr>
      <tr><td>Alternative (frühester)</td><td>LH2054, 31.12., 07:45 → 09:05</td><td>LH2059, 02.01., 10:55 → 12:10</td><td>209 €</td><td>Momondo</td></tr>
      <tr><td>Alternative (nicht morgens)</td><td>LH4114, 31.12., 15:00 → 16:20</td><td>LH2071, 02.01., 17:05 → 18:20</td><td>208 €</td><td>Momondo</td></tr>
    </table>
    <p class="est">Am 31.12. gibt es keinen 18:45-Abflug ab MUC; letzter LH-Abflug ist 15:00, dazu Eurowings 09:15.</p>
  </div>

  <div class="card">
    <h3>Variante C · Mi 30.12.2026 → Sa 02.01.2027</h3>
    <table>
      <tr><th>Option</th><th>Hin (MUC → HAM)</th><th>Zurück (HAM → MUC)</th><th>Preis</th><th>Quelle</th></tr>
      <tr><td><strong>Günstigste insgesamt</strong></td><td>LH2078, 30.12., 18:45 → 20:05</td><td>LH2059, 02.01., 10:55 → 12:10</td><td><strong>200 €</strong></td><td>Momondo; LH direkt ca. 204–205 €</td></tr>
      <tr><td><strong>Günstigste morgens</strong></td><td>LH2062, 30.12., 11:30 → 12:50</td><td>LH2059, 02.01., 10:55 → 12:10</td><td><strong>203 €</strong> (+3 €)</td><td>Momondo</td></tr>
      <tr><td>Alternative (frühester)</td><td>LH2054, 30.12., 07:45 → 09:05</td><td>LH2059, 02.01., 10:55 → 12:10</td><td>210 €</td><td>Momondo</td></tr>
      <tr><td>Alternative (nicht morgens)</td><td>LH2078, 30.12., 18:45 → 20:05</td><td>LH2071, 02.01., 17:05 → 18:20</td><td>204 €</td><td>Momondo</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Variante D · Do 31.12.2026 → So 03.01.2027 (günstigste Variante insgesamt)</h3>
    <table>
      <tr><th>Option</th><th>Hin (MUC → HAM)</th><th>Zurück (HAM → MUC)</th><th>Preis</th><th>Quelle</th></tr>
      <tr><td><strong>Günstigste insgesamt = morgens</strong></td><td>LH2054, 31.12., 07:45 → 09:05</td><td>LH2079, 03.01., 20:50 → 22:05</td><td><strong>161 €</strong></td><td>Momondo; LH direkt 165,66 € — kein Morgen-Aufpreis</td></tr>
      <tr><td>Alternative (morgens, Eurowings)</td><td>EW7171, 31.12., 09:15 → 10:35</td><td>EW7174, 03.01., 19:10 → 20:25</td><td>166 €</td><td>Momondo via Expedia; EW direkt 175 € Basic; mit 1 Aufgabegepäck ab 215 € (Mytrip)</td></tr>
      <tr><td>Alternative (morgens)</td><td>LH2062, 31.12., 11:30 → 12:50</td><td>LH2079, 03.01., 20:50 → 22:05</td><td>171 €</td><td>Momondo; LH direkt 175,66 €</td></tr>
    </table>
    <p class="est">Zum Preis von 161 € auch mit Rückflug 18:05 statt 20:50 (Momondo). Das Eurowings-Angebot (138 €, Stand 10.10.) ist nicht mehr verfügbar.</p>
  </div>

  <div class="note"><strong>🧳 Gepäck bei Lufthansa (verifiziert auf lufthansa.com):</strong> Economy <strong>Basic</strong> = nur kleiner persönlicher Gegenstand (max. 40 × 30 × 15 cm) — KEIN Kabinen-Trolley, KEIN Aufgabegepäck, keine Umbuchung. Das gilt für ALLE günstigsten Optionen oben (OTA und direkt). Economy <strong>Light</strong> = + 1 × 8 kg Handgepäck (55 × 40 × 23), kein Aufgabegepäck (Aufpreis ggü. Basic ca. +10 € pro Strecke). Economy <strong>Comfort</strong> = + 1 × 23 kg Aufgabegepäck + Sitzplatzreservierung beim Check-in. Eurowings <strong>Basic</strong> ohne Hand-/Aufgabegepäck; <strong>Smart</strong> inkl. Hand- + Aufgabegepäck. Achtung: Momondo zeigt für LH-Basic teilweise fälschlich „Aufgabegepäck inklusive" — maßgeblich ist lufthansa.com. Mit Gepäck (nicht alle Varianten einzeln geprüft): A Comfort ca. 274 €, D mit Gepäck ab 215 €, B mit Gepäck ab 286 €.</div>

  <p class="sec-sub"><strong>Rangfolge Bestpreise:</strong> D 161 € &lt; C 200 € &lt; B 203 € &lt; A 211 €. <strong>Günstigste Morgenflüge:</strong> D 161 € (07:45), C 203 € (11:30), B 207 € (09:15, Eurowings), A 214 € (11:30). Morgen-Aufpreis: A +3 €, B +4 €, C +3 €, D 0 €. In keiner Variante fehlt ein Morgenflug.</p>

  <h3>🚆 Bahn München Hbf ↔ Hamburg Hbf (Trainline)</h3>
  <p class="sec-sub">Quelle: Trainline (thetrainline.com/de), 15.10.2026 nachmittags, 1 Erwachsener, 2. Klasse, ohne BahnCard, alle Tarife Super Sparpreis, Suche jeweils ab 06:00, Morgen = Abfahrt vor 12:00.</p>

  <div class="card">
    <h3>Hin · Mi 30.12.2026 (München Hbf → Hamburg Hbf)</h3>
    <table>
      <tr><th>Option</th><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td><strong>Günstigste Morgen + Direkt</strong></td><td>ICE 886</td><td>06:18 → 11:58</td><td>5:40 h</td><td>direkt</td><td><strong>39,99 €</strong></td></tr>
      <tr><td>Alternative direkt</td><td>ICE 684</td><td>07:20 → 12:58</td><td>5:38 h</td><td>direkt</td><td>39,99 €</td></tr>
      <tr><td>Mit 1 Umstieg</td><td>ICE 1102 + ICE 602</td><td>07:25 → 13:24</td><td>5:59 h</td><td>Berlin Hbf (tief), 13 Min.</td><td>49,99 €</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Hin · Do 31.12.2026 (München Hbf → Hamburg Hbf)</h3>
    <table>
      <tr><th>Option</th><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td><strong>Günstigste Morgen + 1 Umstieg</strong></td><td>ICE 1604 + RJ 384</td><td>06:29 → 12:24</td><td>5:55 h</td><td>Berlin Hbf (tief), 11 Min.</td><td><strong>39,99 €</strong></td></tr>
      <tr><td>Günstigste Direkt</td><td>ICE 886</td><td>06:18 → 11:58</td><td>5:40 h</td><td>direkt</td><td>55,99 €</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Zurück · Fr 01.01.2027 (Hamburg Hbf → München Hbf)</h3>
    <table>
      <tr><th>Option</th><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td><strong>Günstigste Morgen + Direkt</strong></td><td>ICE 783</td><td>06:01 → 11:42</td><td>5:41 h</td><td>direkt</td><td><strong>17,99 €</strong></td></tr>
      <tr><td>Alternative direkt</td><td>Zugnummer nicht erfasst</td><td>07:01 → 12:41</td><td>—</td><td>direkt</td><td>17,99 €</td></tr>
      <tr><td>Mit 1 Umstieg</td><td>ICE 505 + ICE 1005</td><td>06:34 → 12:37</td><td>6:03 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>17,99 €</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Zurück · Sa 02.01.2027 (Hamburg Hbf → München Hbf)</h3>
    <table>
      <tr><th>Option</th><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td><strong>Günstigste Morgen + Direkt</strong></td><td>ICE 783</td><td>06:01 → 11:42</td><td>5:41 h</td><td>direkt</td><td><strong>29,99 €</strong></td></tr>
      <tr><td>Mit 1 Umstieg</td><td>ICE 505 + ICE 1005</td><td>06:34 → 12:37</td><td>6:03 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>49,99 €</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Zurück · So 03.01.2027 (Hamburg Hbf → München Hbf)</h3>
    <table>
      <tr><th>Option</th><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td><strong>Günstigste Morgen + Direkt</strong></td><td>ICE 783</td><td>06:01 → 11:42</td><td>5:41 h</td><td>direkt</td><td><strong>29,99 €</strong></td></tr>
      <tr><td>Alternative direkt</td><td>Zugnummer nicht erfasst</td><td>07:01 → 12:41</td><td>—</td><td>direkt</td><td>29,99 €</td></tr>
      <tr><td>Mit 1 Umstieg</td><td>ICE 505 + ICE 1005</td><td>06:34 → 12:37</td><td>6:03 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>49,99 €</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Günstigste Hin+Rück-Gesamtpreise Bahn (jeweils günstigste Morgenverbindung)</h3>
    <table>
      <tr><th>Variante</th><th>Hin</th><th>Zurück</th><th>Gesamt</th></tr>
      <tr><td><strong>A</strong> (30.12. / 01.01.)</td><td>39,99 €</td><td>17,99 €</td><td><strong>57,98 €</strong></td></tr>
      <tr><td><strong>B</strong> (31.12. / 02.01.)</td><td>39,99 €</td><td>29,99 €</td><td><strong>69,98 €</strong></td></tr>
      <tr><td><strong>C</strong> (30.12. / 02.01.)</td><td>39,99 €</td><td>29,99 €</td><td><strong>69,98 €</strong></td></tr>
      <tr><td><strong>D</strong> (31.12. / 03.01.)</td><td>39,99 €</td><td>29,99 €</td><td><strong>69,98 €</strong></td></tr>
    </table>
    <p class="est">Bahn ist damit in allen Varianten deutlich günstiger als der Flug. Probe BahnCard 25: 17,90 € / 3 Monate → 25 % Rabatt auf DB-Tarife. ÖBB Nightjet NJ40420 (22:52 → 08:47, Sitz ab 34,90 €, Liege ab 54,90 €) spart eine Hotel-Nacht — Verkauf läuft bereits.</p>
  </div>

  <h3>🌙 Abend-Rückfahrten (Abfahrt ab 17:00)</h3>
  <p class="sec-sub">Wer abends länger in Hamburg bleiben will: Alle Abend-Rückflüge und die wichtigsten Abend-Züge. Stand: 15.10.2026 nachmittags.</p>

  <div class="card">
    <h3>Abend-Rückflüge · Fr 01.01.2027 (Variante A)</h3>
    <table>
      <tr><th>Rückflug (HAM → MUC)</th><th>Round-Trip mit LH2062 (11:30 hin)</th><th>Round-Trip mit LH2054 (07:45 hin)</th></tr>
      <tr><td><strong>LH2077, 19:35 → 20:50</strong> — günstigster + spätester Abend-Rückflug</td><td><strong>214 €</strong></td><td>221 €</td></tr>
      <tr><td>EW7174, 19:10 → 20:25</td><td>233 €</td><td>242 €</td></tr>
    </table>
    <p class="est">Tagesangebot 01.01.: 10:55, 13:35, 16:35, 19:10, 19:35. Alle Preise Round-Trip gesamt, Economy Basic ohne Aufgabegepäck.</p>
  </div>

  <div class="card">
    <h3>Abend-Rückflüge · Sa 02.01.2027 (Varianten B/C)</h3>
    <table>
      <tr><th>Rückflug (HAM → MUC)</th><th>Variante C (hin 30.12.)</th><th>Variante B (hin 31.12.)</th></tr>
      <tr><td><strong>LH2071, 17:05 → 18:20</strong> — günstigster Abend-Rückflug</td><td><strong>211 €</strong> (mit LH2062) / 219 € (mit LH2054)</td><td><strong>215 €</strong> (mit LH2054/LH2062) / 224 € (mit EW7171)</td></tr>
      <tr><td><strong>LH2079, 20:50 → 22:05</strong> — spätester Rückflug</td><td>219 € (mit LH2062) / 226 € (mit LH2054)</td><td>220 € (mit LH2054/LH2062) / 237 € (mit EW7171)</td></tr>
    </table>
    <p class="est">Tagesangebot 02.01.: 06:15, 09:05, 10:55, 13:35, 15:05, 17:05, 20:50; kein Eurowings-Abendflug.</p>
  </div>

  <div class="card">
    <h3>Abend-Rückflüge · So 03.01.2027 (Variante D)</h3>
    <table>
      <tr><th>Rückflug (HAM → MUC)</th><th>Mit LH2054 (07:45 hin)</th><th>Mit LH2062 (11:30 hin)</th><th>Mit EW7171 (09:15 hin)</th></tr>
      <tr><td><strong>LH2073, 18:05 → 19:20</strong> — günstigster Abend-Rückflug (gleichauf)</td><td><strong>161 €</strong></td><td>171 €</td><td>nicht angezeigt</td></tr>
      <tr><td><strong>LH2079, 20:50 → 22:05</strong> — günstigster + spätester</td><td><strong>161 €</strong></td><td>171 €</td><td>237 €</td></tr>
      <tr><td>EW7174, 19:10 → 20:25</td><td>232 €</td><td>nicht angezeigt</td><td>166 €</td></tr>
      <tr><td>LH2077, 19:35 → 20:50</td><td>186 €</td><td>194 €</td><td>227 €</td></tr>
    </table>
    <p class="est">Tagesangebot 03.01.: 08:55, 10:55, 13:35, 15:05, 18:05, 19:10, 19:35, 20:50. Zwei Kombis (EW7171 + LH2073, LH2062 + EW7174) zeigte Momondo nicht an — ändert nichts an günstigstem/spätestem Flug.</p>
  </div>

  <div class="card">
    <h3>Abend-Züge · Fr 01.01.2027 (Hamburg Hbf → München Hbf)</h3>
    <table>
      <tr><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td>ICE 683</td><td>17:01 → 22:41</td><td>5:40 h</td><td>direkt</td><td>29,99 €</td></tr>
      <tr><td>RJ 179 + ICE 1605</td><td>17:34 → 23:31</td><td>5:57 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>23,99 €</td></tr>
      <tr><td>ICE 885</td><td>18:01 → 23:42</td><td>5:41 h</td><td>direkt</td><td>29,99 €</td></tr>
      <tr><td>ICE 607 + ICE 1107</td><td>18:35 → 00:37 (+1)</td><td>6:02 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>23,99 €</td></tr>
      <tr><td><strong>ICE 685</strong> — günstigste + direkt</td><td><strong>19:01 → 00:42 (+1)</strong></td><td>5:41 h</td><td>direkt</td><td><strong>23,99 €</strong></td></tr>
      <tr><td>Späteste Abfahrt: ICE 921 (+ Anschluss)</td><td>22:46 → 09:01 / 09:20 (+1)</td><td>10:15 / 10:34 h</td><td>3 / 2 Umstiege</td><td>69,99 € / 56,99 €</td></tr>
    </table>
    <p class="est">11 Verbindungen ab 17:00, inkl. Nachtzüge (z. B. ICE 619, 19:45 → 06:03, direkt, 65,99 €). Nightjet NJ 40491 (20:28 → 07:15) über Trainline nicht verkäuflich (kein Preis).</p>
  </div>

  <div class="card">
    <h3>Abend-Züge · Sa 02.01.2027 (Hamburg Hbf → München Hbf)</h3>
    <table>
      <tr><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td>ICE 683</td><td>17:01 → 22:41</td><td>5:40 h</td><td>direkt</td><td>39,99 €</td></tr>
      <tr><td>ICE 885</td><td>18:01 → 23:42</td><td>5:41 h</td><td>direkt</td><td>39,99 €</td></tr>
      <tr><td>ICE 607 + ICE 1107</td><td>18:35 → 00:37 (+1)</td><td>6:02 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>39,99 €</td></tr>
      <tr><td><strong>ICE 1277 + ICE 619</strong> — günstigste</td><td><strong>19:29 → 06:03 (+1)</strong></td><td>10:34 h</td><td>Frankfurt (Main) Hbf, 1:03 h</td><td><strong>29,99 €</strong></td></tr>
      <tr><td>Späteste Abfahrt: ICE 921 (+ Anschluss)</td><td>22:46 → 09:20 (+1)</td><td>10:34 h</td><td>2 Umstiege</td><td>49,99 €</td></tr>
    </table>
    <p class="est">10 Verbindungen ab 17:00. Am 02.01. gibt es KEINE 19:01-Direktverbindung (anders als am 01.01. und 03.01.). Nightjet NJ 40491 (20:28 → 07:15) über Trainline nicht verkäuflich.</p>
  </div>

  <div class="card">
    <h3>Abend-Züge · So 03.01.2027 (Hamburg Hbf → München Hbf)</h3>
    <table>
      <tr><th>Verbindung</th><th>Abfahrt → Ankunft</th><th>Dauer</th><th>Umstiege</th><th>Preis</th></tr>
      <tr><td>ICE 683</td><td>17:01 → 22:41</td><td>5:40 h</td><td>direkt</td><td>39,99 €</td></tr>
      <tr><td>RJ 179 + ICE 1605</td><td>17:34 → 23:31</td><td>5:57 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>39,99 €</td></tr>
      <tr><td>ICE 885</td><td>18:01 → 23:42</td><td>5:41 h</td><td>direkt</td><td>39,99 €</td></tr>
      <tr><td>ICE 607 + ICE 1107</td><td>18:35 → 00:37 (+1)</td><td>6:02 h</td><td>Berlin Hbf (tief), 15 Min.</td><td>29,99 €</td></tr>
      <tr><td><strong>ICE 685</strong> — günstigste + direkt</td><td><strong>19:01 → 00:42 (+1)</strong></td><td>5:41 h</td><td>direkt</td><td><strong>23,99 €</strong></td></tr>
      <tr><td>Späteste Abfahrt: ICE 921 (+ Anschluss)</td><td>22:46 → 09:15 / 09:20 / 09:38 (+1)</td><td>10:29–10:52 h</td><td>3 / 2 / 4 Umstiege</td><td>ab 39,99 €</td></tr>
    </table>
    <p class="est">12 Verbindungen ab 17:00, inkl. Nachtzüge. Nightjet NJ 40491 (20:28 → 07:15) über Trainline nicht verkäuflich (kein Preis).</p>
  </div>

  <div class="card">
    <h3>Bahn: Hin+Rück-Gesamtpreise mit Abend-Rückfahrt (günstigster Morgen-Hinzug + günstigste Abend-Rückfahrt)</h3>
    <table>
      <tr><th>Variante</th><th>Hin (morgens)</th><th>Zurück (abends, günstigste)</th><th>Gesamt</th></tr>
      <tr><td><strong>A</strong> (30.12. / 01.01.)</td><td>39,99 €</td><td>23,99 € (ICE 685, 19:01, direkt)</td><td><strong>63,98 €</strong></td></tr>
      <tr><td><strong>B</strong> (31.12. / 02.01.)</td><td>39,99 €</td><td>29,99 € (19:29, 1 Umstieg Frankfurt)</td><td><strong>69,98 €</strong></td></tr>
      <tr><td><strong>C</strong> (30.12. / 02.01.)</td><td>39,99 €</td><td>29,99 € (19:29, 1 Umstieg Frankfurt)</td><td><strong>69,98 €</strong></td></tr>
      <tr><td><strong>D</strong> (31.12. / 03.01.)</td><td>39,99 €</td><td>23,99 € (ICE 685, 19:01, direkt)</td><td><strong>63,98 €</strong></td></tr>
    </table>
    <p class="est">Alle Abend-Preise Super Sparpreis (Trainline, 15.10.2026 nachmittags). Eine eventuelle Trainline-Buchungsgebühr ist in den Preisen nicht bestätigt enthalten.</p>
  </div>

  <div class="note"><strong>Hinweise zur Bahn-Recherche:</strong> Trainline zeigt nur die schnellsten Verbindungen mit den wenigsten Umstiegen — langsamere/günstigere mit mehr Umstiegen ggf. nicht enthalten. Eine eventuelle Trainline-Buchungsgebühr ist in den Preisen nicht bestätigt enthalten (bis zur Fahrgastdaten-Seite keine separate Gebührenzeile; der letzte Zahlungsschritt war ohne Eingabe persönlicher Daten nicht prüfbar). bahn.de hat die Abfrage am 15.10. mit Bot-Sperre blockiert (Fehler 751, kein lösbares CAPTCHA); der ÖBB-Ticketshop hing in einer Cloudflare-Schleife — Preise dort ggf. auf eigenem Gerät prüfen. Preise dynamisch (z. B. 03.01.-Rückfahrt, 07:01-Verbindung, während der Prüfung 39,99 € → 29,99 €).</div>
</section>
"""

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

""" + ANREISE_DETAIL + FIREWORKS + ELBPHI_3D + HIGHLIGHTS + MUSEUMS + FOOD + HOTELS + """

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
