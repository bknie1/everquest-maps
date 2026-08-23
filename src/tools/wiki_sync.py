"""wiki_sync.py -- pull zone lore/POI text from the EQL wiki into the repo.

Fetches each zone's wiki page, reduces it to readable text, and writes
src/data/wiki/<zone>.md with a fetch date. Re-running only rewrites files
whose content actually changed, so a daily run produces meaningful diffs --
which is the point: POI/mob updates on the wiki show up as commits here.

    python src/tools/wiki_sync.py              # all mapped zones
    python src/tools/wiki_sync.py unrest tox   # just these

Runs with the standard library only (urllib). Unknown/renamed pages 404 and
are reported, not fatal -- extend PAGES as they get resolved.
"""
import html
import os
import re
import sys
import time
import urllib.request
from datetime import date

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'wiki')
BASE = 'https://eqlwiki.com/'

# zone short name -> wiki page. EQL leans on EQOA-era naming for the overland
# ("The Western Plains of Karana"), classic names for dungeons and cities.
PAGES = {
    'unrest': 'Estate_of_Unrest', 'beholder': 'Gorge_of_King_Xorbb',
    'misty': 'Misty_Thicket', 'akanon': "Ak'Anon", 'halas': 'Halas',
    'qeynos': 'Qeynos', 'qeynos2': 'Qeynos', 'qcat': 'Qeynos_Catacombs',
    'paineel': 'Paineel', 'erudnext': 'Erudin', 'kaladima': 'Kaladim',
    'kaladimb': 'Kaladim', 'oggok': 'Oggok', 'grobb': 'Grobb',
    'rivervale': 'Rivervale', 'felwithea': 'Felwithe', 'felwitheb': 'Felwithe',
    'gfaydark': 'Greater_Faydark', 'lfaydark': 'Lesser_Faydark',
    'crushbone': 'Crushbone', 'butcher': 'Butcherblock_Mountains',
    'cauldron': "Dagnor's_Cauldron", 'kedge': 'Kedge_Keep',
    'mistmoore': 'Castle_Mistmoore', 'steamfont': 'Steamfont_Mountains',
    'freportn': 'North_Freeport', 'freportw': 'West_Freeport',
    'freporte': 'East_Freeport', 'freeportsewers': 'Freeport_Sewers',
    'neriaka': 'Neriak_Foreign_Quarter', 'neriakb': 'Neriak_Commons',
    'neriakc': 'Neriak_Third_Gate', 'nektulos': 'Nektulos_Forest',
    'lavastorm': 'Lavastorm_Mountains', 'najena': 'Najena',
    'soldunga': "Solusek's_Eye", 'soldungb': "Nagafen's_Lair",
    'soltemple': 'Temple_of_Solusek_Ro', 'highpass': 'Highpass_Hold',
    'highkeep': 'High_Keep', 'kithicor': 'Kithicor_Forest',
    'commons': 'West_Commonlands', 'ecommons': 'East_Commonlands',
    'befallen': 'Befallen', 'nro': 'North_Ro', 'sro': 'South_Ro',
    'oasis': 'Oasis_of_Marr', 'innothule': 'Innothule_Swamp',
    'feerrott': 'The_Feerrott', 'cazicthule': 'Cazic-Thule',
    'guktop': 'Upper_Guk', 'gukbottom': 'Lower_Guk',
    'rathemtn': 'Rathe_Mountains', 'lakerathe': 'Lake_Rathetear',
    'qeytoqrg': 'Qeynos_Hills', 'qrg': 'Surefall_Glade',
    'blackburrow': 'Blackburrow', 'everfrost': 'Everfrost_Peaks',
    'permafrost': 'Permafrost_Keep', 'qey2hh1': 'Western_Plains_of_Karana',
    'northkarana': 'Northern_Plains_of_Karana',
    'eastkarana': 'Eastern_Plains_of_Karana',
    'southkarana': 'Southern_Plains_of_Karana',
    'runnyeye': 'Runnyeye_Citadel', 'hateplaneb': 'Plane_of_Hate', 'paw': 'Splitpaw_Lair',
    'oot': 'Ocean_of_Tears', 'erudsxing': "Erud's_Crossing",
    'erudnint': 'Erudin_Palace', 'tox': 'Toxxulia_Forest',
    'kerraridge': 'Kerra_Isle', 'stonebrunt': 'Stonebrunt_Mountains',
    'warrens': 'The_Warrens', 'hole': 'The_Hole',
    'fearplane': 'Plane_of_Fear', 'hateplane': 'Plane_of_Hate',
    'airplane': 'Plane_of_Sky', 'newsebexp': 'New_Sebilis',
}


def fetch(page):
    url = BASE + urllib.request.quote(page)
    req = urllib.request.Request(url, headers={'User-Agent': 'emoda-maps-wiki-sync'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')


def to_text(raw):
    raw = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S | re.I)
    # keep table cell/row breaks readable
    raw = re.sub(r'</(tr|table|p|div|h[1-6]|li)>', '\n', raw, flags=re.I)
    raw = re.sub(r'</t[dh]>', ' | ', raw, flags=re.I)
    raw = re.sub(r'<[^>]+>', '', raw)
    raw = html.unescape(raw)
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in raw.splitlines()]
    lines = [l for l in lines if l and not l.startswith(('mw-', 'vector-'))]
    return '\n'.join(lines)


def main():
    zones = sys.argv[1:] or sorted(PAGES)
    os.makedirs(OUT, exist_ok=True)
    changed, failed = 0, []
    for z in zones:
        page = PAGES.get(z)
        if not page:
            failed.append((z, 'no page mapping'))
            continue
        try:
            body = to_text(fetch(page))
        except Exception as e:
            failed.append((z, str(e)[:60]))
            continue
        out_path = os.path.join(OUT, z + '.md')
        header = f'# {page} (eqlwiki.com)\n'
        stamp = f'fetched: {date.today().isoformat()}\n\n'
        new = header + stamp + body + '\n'
        old = ''
        if os.path.exists(out_path):
            old = open(out_path, encoding='utf-8').read()
        # ignore the date line when deciding whether content changed
        strip = lambda t: '\n'.join(l for l in t.splitlines() if not l.startswith('fetched:'))
        if strip(old) != strip(new):
            open(out_path, 'w', newline='\n', encoding='utf-8').write(new)
            changed += 1
            print('updated', z)
        time.sleep(1.0)
    print(f'{changed} changed, {len(failed)} failed')
    for z, why in failed:
        print('  FAIL', z, '-', why)


if __name__ == '__main__':
    main()
