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

# Gear that would false-match material rules -> stays Sell
$gearExclude = @(
    'Cloak of Leaves','Cloak of Scales','Crown of Leaves','Cudgel of Glowing Clay',
    'Dreadfangs Hide',"Frightchaser's Hide","Terrorclaw's Hide","Orb of the River's Essence"
)

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

function Classify($name) {
    if ($gearExclude -contains $name) { return 4 }
    if ($name -match '^Mote of ')                        { return 1 }
    if ($name -match '^(Spell|Song): ')                  { return 1 }
    if ($name -match '^(Elemental|Timeless) Silk .*Pattern$') { return 1 }
    if ($gems -contains $name)        { return 2 }
    if ($exactMerge -contains $name)  { return 2 }
    if ($name -imatch $mergeRegex)    { return 2 }
    return 4
}

$out = foreach ($e in $items.Values) {
    $f = if ($e.Override) { $e.Override } else { Classify $e.Name }
    [pscustomobject]@{ Id=$e.Id; Filter=$f; Icon=$e.Icon; Name=$e.Name }
}

"=== COUNTS ==="
$out | Group-Object Filter | Sort-Object Name | ForEach-Object { "Filter $($_.Name): $($_.Count)" }
"`n=== LOOT (1) ==="
($out | Where-Object Filter -eq 1 | Sort-Object Name).Name -join '; '
"`n=== STORE (3, preserved from your in-game choices) ==="
($out | Where-Object Filter -eq 3 | Sort-Object Name).Name -join '; '
"`n=== MERGE (2) ==="
($out | Where-Object Filter -eq 2 | Sort-Object Name).Name -join '; '

$lines = @('#ITEM_ID^FILTER_ID^ICON_ID^ITEM_NAME')
$lines += $out | Sort-Object Filter, Name | ForEach-Object { "$($_.Id)^$($_.Filter)^$($_.Icon)^$($_.Name)" }
[IO.File]::WriteAllLines($outFile, $lines, [Text.Encoding]::GetEncoding(1252))
"`nWrote $outFile ($($lines.Count) lines)"