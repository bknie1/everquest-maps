"""races.py -- one index from a race/homeland to the kit shapes that suit it.

Written so a zone build never has to invent decoration inline. If a race's entry
here is thin, that is the thing to extend -- not the build script.

    from races import RACE_KITS
    RACE_KITS['gnome']['decor']      -> callables (cx, cy, r) -> [(x1,y1,x2,y2,ink)]
    RACE_KITS['gnome']['figure']     -> the fauna figure
    RACE_KITS['gnome']['flora']      -> plants that belong in that homeland
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import flora as FL, fauna as FA, terrain as TR
import gnome_decor as GN
import civic_decor as CV
import nse_decor as IK
import darkelf as DE

FP, TP = FL.PALETTE, TR.PALETTE

RACE_KITS = {
    'gnome': dict(
        figure=FA.RACES['gnome'], homeland='akanon',
        decor=[GN.gear, GN.gear_pair, GN.pump, GN.cog_tower, GN.lantern, GN.pipe_run],
        flora=[FL.mushrooms], terrain=[TR.rock_band]),
    'iksar': dict(
        figure=FA.RACES['iksar'], homeland='cabilis',
        decor=[IK.iksar_glyph, IK.bookshelf, IK.standard, IK.wall_candle,
               IK.root_bunch, IK.root_drip, IK.root_burst],
        flora=[FL.fern, FL.mushrooms], terrain=[TR.rock_band]),
    'dark_elf': dict(
        figure=FA.RACES['dark_elf'], homeland='neriak',
        decor=[DE.monolith, DE.brazier, DE.rune_panel, DE.teirdal_sigil,
               DE.web_corner, DE.arched_gate, DE.torch],
        flora=[FL.mushrooms], terrain=[TR.rock_band]),
    'barbarian': dict(
        figure=FA.RACES['barbarian'], homeland='halas',
        decor=[CV.hide_tent, CV.totem, CV.fire_pit], flora=[FL.fir], terrain=[TR.peak, TR.snowdrift]),
    'troll': dict(
        figure=FA.RACES['troll'], homeland='grobb',
        decor=[CV.swamp_hut, CV.bone_pile, CV.totem], flora=[FL.reeds, FL.dead_tree, FL.mushrooms],
        terrain=[TR.mudflat]),
    'ogre': dict(
        figure=FA.RACES['ogre'], homeland='oggok',
        decor=[CV.crude_pillar, CV.aqueduct, CV.war_drum], flora=[FL.broadleaf, FL.fern], terrain=[TR.ruin_arch]),
    'dwarf': dict(
        figure=FA.RACES['dwarf'], homeland='kaladim',
        decor=[CV.anvil, CV.forge, CV.ore_cart], flora=[FL.mushrooms], terrain=[TR.rock_band]),
    'high_elf': dict(
        figure=FA.RACES['high_elf'], homeland='felwithe',
        decor=[CV.elf_spire], flora=[FL.willow, FL.flowers], terrain=[]),
    'wood_elf': dict(
        figure=FA.RACES['wood_elf'], homeland='kelethin',
        decor=[CV.treehouse, CV.elf_spire], flora=[FL.broadleaf, FL.fern, FL.flowers], terrain=[]),
    'halfling': dict(
        figure=FA.RACES['halfling'], homeland='rivervale',
        decor=[CV.burrow_door, CV.pie], flora=[FL.broadleaf, FL.flowers, FL.grass_tuft], terrain=[TR.hill]),
    'erudite': dict(
        figure=FA.RACES['erudite'], homeland='erudin',
        decor=[CV.tome, CV.orrery, CV.obelisk], flora=[], terrain=[]),
    'qeynos_human': dict(
        figure=FA.RACES['qeynos_human'], homeland='qeynos',
        decor=[CV.banner, CV.market_stall], flora=[FL.broadleaf, FL.grass_tuft], terrain=[TR.hill]),
    'freeport_human': dict(
        figure=FA.RACES['freeport_human'], homeland='freeport',
        decor=[CV.caravel, CV.market_stall, CV.banner], flora=[FL.palm], terrain=[]),
    'kerran': dict(
        figure=FA.RACES['kerran'], homeland='kerraisle',
        decor=[CV.fish_rack], flora=[FL.palm], terrain=[]),
    'froglok': dict(
        figure=FA.RACES['froglok'], homeland='gukta',
        decor=[CV.lily_pad], flora=[FL.reeds, FL.mushrooms], terrain=[TR.mudflat]),
}


def missing_decor():
    """Races with no bespoke decoration kit yet -- the honest to-do list."""
    return sorted(k for k, v in RACE_KITS.items() if not v['decor'])
