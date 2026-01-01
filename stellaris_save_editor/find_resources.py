import zipfile, re

zf = zipfile.ZipFile('stellaris_save_editor/liam.sav', 'r')
content = zf.read('gamestate').decode('utf-8', errors='ignore')

# Find country 0 (player)
pattern = r'country=\s*\{\s*0=\s*\{'
match = re.search(pattern, content)
if match:
    start = match.end()
    # Search in the country section
    country_chunk = content[start:start+200000]
    
    # Look for resource= patterns
    resource_match = re.search(r'resource=\s*\[', country_chunk)
    if resource_match:
        res_pos = resource_match.start()
        print("Found resources at offset:", res_pos)
        print("\n" + "="*60)
        print(country_chunk[res_pos:res_pos+2000])
    else:
        print("Checking for { style...")
        resource_match = re.search(r'resource=\s*\{', country_chunk)
        if resource_match:
            res_pos = resource_match.start()
            print("Found resources (brace style) at offset:", res_pos)
            print("\n" + "="*60)
            print(country_chunk[res_pos:res_pos+2000])
        else:
            print("No resource section found. Searching for 'minerals' or 'energy'...")
            minerals = re.search(r'(minerals|energy).{0,100}', country_chunk)
            if minerals:
                print(minerals.group(0))
