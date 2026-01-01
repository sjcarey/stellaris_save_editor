import zipfile, re

zf = zipfile.ZipFile('stellaris_save_editor/liam.sav', 'r')
content = zf.read('gamestate').decode('utf-8', errors='ignore')

# Find country 0
pattern = r'country=\s*\{\s*0=\s*\{'
match = re.search(pattern, content)
if match:
    start = match.end()
    country_section = content[start:start+35000]
    
    # Look for standalone resource key=value lines (the stockpile)
    resources = ['energy', 'minerals', 'food', 'alloys', 'consumer_goods', 
                 'volatile_motes', 'exotic_gases', 'rare_crystals',
                 'sr_living_metal', 'sr_zro', 'sr_dark_matter']
    
    for resource in resources:
        # Match resource=value where it's at the start of a country property (few tabs/spaces)
        pattern = rf'^\t+{resource}=([\d.-]+)$'
        match = re.search(pattern, country_section, re.MULTILINE)
        if match:
            print(f"{resource}: {match.group(1)} (found at position {match.start()})")
            # Show context
            ctx_start = max(0, match.start() - 100)
            ctx_end = min(len(country_section), match.end() + 100)
            print(f"Context:\n{country_section[ctx_start:ctx_end]}\n")
            break  # Just show first one for now

print("\n" + "="*60)
print("First 2000 chars of country:")
print("="*60)
print(country_section[:2000])
