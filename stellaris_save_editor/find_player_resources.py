import zipfile, re

zf = zipfile.ZipFile('stellaris_save_editor/liam.sav', 'r')
content = zf.read('gamestate').decode('utf-8', errors='ignore')

# Find country 0 (player)
pattern = r'country=\s*\{\s*0=\s*\{'
match = re.search(pattern, content)
if match:
    start = match.end()
    
    # Find the end of this country block (next country or close brace)
    # Search for the player's resource values in first 50k chars
    country_section = content[start:start+50000]
    
    # Find energy and minerals in this section
    energy_match = re.search(r'^\s+energy=([\d.-]+)', country_section, re.MULTILINE)
    minerals_match = re.search(r'^\s+minerals=([\d.-]+)', country_section, re.MULTILINE)
    food_match = re.search(r'^\s+food=([\d.-]+)', country_section, re.MULTILINE)
    alloys_match = re.search(r'^\s+alloys=([\d.-]+)', country_section, re.MULTILINE)
    
    print("Found in player country section:")
    if energy_match:
        print(f"  Energy: {energy_match.group(1)} at position {energy_match.start()}")
        print(f"  Context: {country_section[max(0,energy_match.start()-50):energy_match.end()+50]}")
    if minerals_match:
        print(f"  Minerals: {minerals_match.group(1)} at position {minerals_match.start()}")
    if food_match:
        print(f"  Food: {food_match.group(1)}")
    if alloys_match:
        print(f"  Alloys: {alloys_match.group(1)}")
