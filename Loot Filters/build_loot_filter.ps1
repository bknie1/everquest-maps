# Build LF_Emoda_Legends.ini — curated loot filter
# Filter IDs (per EQUI_LootFiltersWnd.xml column order): 1=Loot 2=Merge 3=Store 4=Sell
$ErrorActionPreference = 'Stop'

$myFile   = 'D:\EverQuest Legends\userdata\LF_My_Loot_Filter.ini'
$charFile = 'D:\EverQuest Legends\userdata\LF_Emoda_rivervale.ini'
$outFile  = Join-Path $PSScriptRoot 'LF_Emoda_Legends.ini'

function Parse($path) {
    Get-Content $path | Select-Object -Skip 1 | Where-Object { $_ -match '\^' } | ForEach-Object {
        $p = $_ -split '\^'
        [pscustomobject]@{ Id = $p[0]; Filter = [int]$p[1]; Icon = $p[2]; Name = $p[3] }
    }
}

$mine = Parse $myFile
$char = Parse $charFile

# Union by item ID. Base name = name without " +N" merge-suffix.
$items = [ordered]@{}
foreach ($e in $mine) {
    $items[$e.Id] = [pscustomobject]@{ Id=$e.Id; Icon=$e.Icon; Name=($e.Name -replace ' \+\d+$',''); Override=$null }
}
foreach ($e in $char) {
    $base = $e.Name -replace ' \+\d+$',''
    if (-not $items.Contains($e.Id)) {
        $items[$e.Id] = [pscustomobject]@{ Id=$e.Id; Icon=$e.Icon; Name=$base; Override=$null }
    }
    # Preserve deliberate in-game choices (Loot/Merge/Store); imported 4s get reclassified
    if ($e.Filter -in 1,2,3) { $items[$e.Id].Override = $e.Filter }
}

# Gear that would false-match material rules if checked in the wrong order --
# now routed to the general gear->omit rule below instead of being sold.
$gearForce = @(
    'Cloak of Leaves','Cloak of Scales','Crown of Leaves','Cudgel of Glowing Clay',
    'Dreadfangs Hide',"Frightchaser's Hide","Terrorclaw's Hide","Orb of the River's Essence",
    # exotic proper-noun weapons the keyword/icon passes can't reach (each is
    # the ONLY item on its icon, or its icon-siblings are equally unmatchable
    # by name, so icon-correlation has no keyword-matched sibling to anchor on)
    'Argent Defender','Ashenbone Abbasi',"Blackguard's Dudgeon",'Board of Bashing',
    'Bulwark of Shimmering Steel','Culler',"Hate's Edge",'Painbringer','Bloodmoon',
    'Curzon','Spiritguard'
)

# EQUIPMENT (Brandon, 2026-09-13): "any items that can have a +1 +2 etc.
# modifier is something I do not want to auto sell for sure... when in doubt,
# leave it off the list." Any weapon/armor/jewelry/instrument noun below marks
# an item as gear -> OMITTED from the curated list entirely (never sold by
# us), regardless of how mundane the base name looks -- a "Rusty Mining Pick"
# can drop as "Rusty Mining Pick +1", and the filter is keyed by item ID, not
# by the rolled modifier. Ammo (Arrow*) is deliberately NOT protected -- it
# doesn't carry +N bonuses in this itemization. Checked AFTER the material/
# gem/merge rules above so real tradeskill materials (Fang, Skin, Hide, etc.)
# keep matching those first; this only catches what would otherwise default
# to Sell.
#
# $gearWordsFused match with NO boundary at all (plain substring) -- these are
# the specific nouns that legitimately appear glued to a prefix with no space
# in this item set ("Legplates", "Warhammer", "Chainmail", "Webshield",
# "Longsword"/"Greatsword"/"Warblade"/"Throneblade"), so an unbounded match is
# required to catch them.
# $gearWords match with a LEFT boundary (not preceded by a letter) -- everyone
# else. This is what caught the real bug here 2026-09-13: an unbounded 'Harp'
# matched inside "Sharp Tooth", which (via the icon-correlation pass below)
# spread to falsely flag every other same-icon tooth trophy as gear. Keep
# short/common-English-word terms in THIS bucket, never the fused one.
$gearWordsFused = @('Sword','Blade','Hammer','Plate','Mail','Shield')
$gearWords = @(
    # weapons
    'Claymore','Falchion','Scimitar','Cutlass','Rapier','Saber','Sabre','Cleaver',
    'Axe','Hatchet','Tomahawk',
    'Mace','Club','Cudgel','Flail','Maul','Warclub','Morning Star','Mallet',
    'Dagger','Dirk','Knife','Stiletto','Kris','Shiv','Pugius','Seax','Jambiya','Estoc','Gauche','Razor',
    'Spear','Pike','Lance','Halberd','Glaive','Partisan','Trident','Harpoon',
    'Staff','Rod','Wand','Scepter','Crook',
    'Bow',
    'Whip','Lariat',
    'Pick',
    'Knuckles','Fist',
    'Yari','Jutte','Tanto','Wakizashi','Ulak','Kama','Sai',
    'Sling','Shuriken',
    'Zweihander','Katana','Kukri','Machete','Scythe','Flamberge',
    'Fer`Esh','Shan`Tok','Sheer Blade','Chopper',
    'Fishing Pole','Fishing Rod',
    # armor
    'Helm','Coif','Cap','Cowl','Hood','Mask','Visor','Circlet','Headband','Turban','Veil','Skullcap',
    'Breastplate','Chestplate','Cuirass','Hauberk','Tunic','Robe','Jerkin','Vest',
    'Armor','Coat','Shirt','Skirt',
    'Bracer','Vambrace','Wristband','Wristguard','Armguard','Armband','Cuff',
    'Gauntlet','Glove','Mitt',
    'Greaves','Boot','Sandal','Shoe','Slipper',
    'Legging','Pant','Trouser','Pantaloon','Kilt',
    'Girdle','Belt','Sash','Cord','Cinch','Waistband',
    'Cloak','Cape','Mantle','Shawl',
    'Buckler','Targ',
    'Pauldron','Spaulder','Epaulet','Shoulderpad',
    'Gorget','Collar','Neckguard',
    'Bandolier','Baldric',
    'Sleeve','Amice',
    # jewelry
    'Necklace','Ring','Band','Earring','Bracelet','Choker','Amulet','Pendant','Locket','Charm','Talisman','Trinket',
    'Crown','Diadem','Medallion','Brooch','Torc',
    # instruments (can carry bard stats)
    'Lute','Harp','Drum','Horn','Flute','Mandolin','Cittern'
)
$gearRegexFused = '(' + ($gearWordsFused -join '|') + ')'
$gearRegexBounded = '(?<![a-zA-Z])(' + ($gearWords -join '|') + ')'

# Exact-name jewelcraft gems (uncut gems only; 'Onyx Ring' etc. won't match)
$gems = @(
    'Malachite','Lapis Lazuli','Turquoise','Azurite','Jasper',"Cat's Eye Agate",'Flame Agate',
    'Carnelian','Bloodstone','Onyx','Amber','Opal','Large Opal','Hazy Opal','Fire Opal',
    'Storm Sky Opal','Ethereal Opal','Pearl','Topaz','Shimmering Topaz','Peridot','Jacinth',
    'Uncut Jacinth','Emerald','Fire Emerald','Nebulous Emerald','Ethereal Emerald',
    'Blood Sky Emerald',"Nature Walker's Sky Emerald",'Ruby','Star Ruby','Star Rose Quartz',
    'Rose Quartz','Sapphire','Small Sapphire','Black Sapphire','Uncut Black Sapphire',
    'Black Nebulous Sapphire','Blackened Sapphire','Bloodsky Sapphire','Large Sky Sapphire',
    'Diamond','Blue Diamond','Fabled Blue Diamond','Black Sky Diamond','Ivory Sky Diamond',
    'Large Sky Diamond','Harmonagate','Precious Garnet','Uncut Amethyst',
    'Raw Amber Nihilite','Raw Crimson Nihilite','Raw Indigo Nihilite','Raw Shimmering Nihilite'
)

# Exact-name extras: reagents, quest XP turn-ins, missed mats
$exactMerge = @(
    'Fire Beetle Eye','Crystallized Sulfur','Fresh Fish','Koalindl Fish','Grapes','Preserved Hops',
    'Bottle of Milk','Jar of Honey','Honeycomb','Honey Mead','Sylvan Berries','Ashroot',
    'Polished Jade Leaves','Swatch of Cryosilk','Viscid Silk Swatch','Silken Strands',
    'Parchment of Flayed Skin','Spider Venom',
    'Crushbone Belt','Crushbone Shoulderpads','Deathfist Shoulderpads','Gnoll Fang','Bandit Sash'
)

# Regex rules for Merge (2): stackable tradeskill materials
$mergeRules = @(
    '^Words of ', '^Rune of ', "Tasarin's Grimoire", "Salil's Writ", "Velishoul's Tome", '^Torn Page of',
    'Bone Chips$', 'Spinneret Fluid$', ' Marrow$', 'Silk$',
    '\bOre\b', '^Chunk of ', 'Clay$',
    'Meat$', ' Egg$',
    '^Vial of ', 'Blood Vial$', 'Ichor Vial$', 'Water Flask$',
    'Nectar$', 'ushroom',
    'Gland$', 'Venom Sac$', '^Consigned .* Sealed Poison Vial$',
    '^Essence of ', 'Essence$',
    ' Bark$', 'Roots?$', 'Pollen$', ' Leaf$',
    'Pelt$', 'Skin$', ' Hide$', ' Fur$', 'Scales?$', 'Feathers?$',
    '^(Giant )?Bat Wing$', 'Sewing Needle$'
)
$mergeRegex = ($mergeRules -join '|')

# Classify returns 1/2/3/4, or $null for "omit from the list entirely"
# (equipment that could roll a +N modifier -- never auto-sold by us).
# gearForce runs FIRST -- these are exact-named gear pieces that would
# otherwise false-match a material regex below (e.g. "Cloak of Scales" ends
# in "Scales" -> the tradeskill-scales rule would wrongly claim it).
function Classify($name) {
    if ($gearForce -contains $name)   { return $null }
    if ($name -match '^Mote of ')                        { return 1 }
    if ($name -match '^(Spell|Song): ')                  { return 1 }
    if ($name -match '^(Elemental|Timeless) Silk .*Pattern$') { return 1 }
    if ($gems -contains $name)        { return 2 }
    if ($exactMerge -contains $name)  { return 2 }
    if ($name -imatch $mergeRegex)    { return 2 }
    if ($name -imatch $gearRegexFused -or $name -imatch $gearRegexBounded) { return $null }
    return 4
}

# Pass 1: classify by name alone (ignoring in-game Overrides for now -- we
# need the pure name-based read to build the icon map below).
$byName = foreach ($e in $items.Values) {
    [pscustomobject]@{ Id=$e.Id; Icon=$e.Icon; Name=$e.Name; Override=$e.Override; NameFilter=(Classify $e.Name) }
}

# Icon-correlation pass: this game draws each weapon/armor TYPE with a
# consistent icon (every dagger uses the same icon regardless of material),
# so an exotic proper-noun weapon our keyword list can't parse ("Argent
# Defender", "Gladius", "Devlas Ilkvel") still shares its icon with a
# keyword-matched sibling ("Ghoulbane" shares icon 519 with "Two Handed
# Sword"). Icons used by BOTH a name-matched gear item and a name-matched
# material/spell are ambiguous (mixed use) and excluded from the extension.
$gearIcons    = [System.Collections.Generic.HashSet[string]]::new()
$nonGearIcons = [System.Collections.Generic.HashSet[string]]::new()
foreach ($r in $byName) {
    if ($null -eq $r.NameFilter) { [void]$gearIcons.Add($r.Icon) }
    elseif ($r.NameFilter -in 1,2) { [void]$nonGearIcons.Add($r.Icon) }
}
$safeGearIcons = [System.Collections.Generic.HashSet[string]]::new($gearIcons)
$safeGearIcons.ExceptWith($nonGearIcons)
$iconCaught = 0
foreach ($r in $byName) {
    if ($r.NameFilter -eq 4 -and $safeGearIcons.Contains($r.Icon)) {
        $r.NameFilter = $null
        $iconCaught++
    }
}

$all = foreach ($r in $byName) {
    $f = if ($r.Override) { $r.Override } else { $r.NameFilter }
    [pscustomobject]@{ Id=$r.Id; Filter=$f; Icon=$r.Icon; Name=$r.Name }
}
$omitted = $all | Where-Object { $null -eq $_.Filter }
$out     = $all | Where-Object { $null -ne $_.Filter }
"Gear caught by icon-correlation (name gave no hit): $iconCaught"

"=== COUNTS ==="
$out | Group-Object Filter | Sort-Object Name | ForEach-Object { "Filter $($_.Name): $($_.Count)" }
"Omitted (gear, not on the list): $($omitted.Count)"
"`n=== LOOT (1) ==="
($out | Where-Object Filter -eq 1 | Sort-Object Name).Name -join '; '
"`n=== STORE (3, preserved from your in-game choices) ==="
($out | Where-Object Filter -eq 3 | Sort-Object Name).Name -join '; '
"`n=== MERGE (2) ==="
($out | Where-Object Filter -eq 2 | Sort-Object Name).Name -join '; '
"`n=== OMITTED (gear -- never auto-sold, first 40 alphabetically) ==="
($omitted | Sort-Object Name | Select-Object -First 40).Name -join '; '

$lines = @('#ITEM_ID^FILTER_ID^ICON_ID^ITEM_NAME')
$lines += $out | Sort-Object Filter, Name | ForEach-Object { "$($_.Id)^$($_.Filter)^$($_.Icon)^$($_.Name)" }
[IO.File]::WriteAllLines($outFile, $lines, [Text.Encoding]::GetEncoding(1252))
"`nWrote $outFile ($($lines.Count) lines)"