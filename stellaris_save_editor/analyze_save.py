import zipfile, re

zf = zipfile.ZipFile('stellaris_save_editor/liam.sav', 'r')
content = zf.read('gamestate').decode('utf-8', errors='ignore')

# Find player country ID
player_match = re.search(r'player=.*?country=(\d+)', content, re.DOTALL)
if player_match:
    cid = player_match.group(1)
    print(f'Player country ID: {cid}')
    
    # Find country section in the country= block
    pattern = rf'country=\s*\{{\s*{cid}='
    match = re.search(pattern, content)
    if match:
        start = match.start()
        # Print first 3000 chars of country data
        sample = content[start:start+3000]
        print("\n" + "="*60)
        print("Country data sample:")
        print("="*60)
        print(sample)
        
        # Look for resource patterns
        resource_matches = re.findall(r'(type=\w+.*?accumulated=[\d.]+)', sample, re.DOTALL)
        if resource_matches:
            print("\n" + "="*60)
            print("Found resource entries:")
            print("="*60)
            for r in resource_matches[:5]:
                print(r[:200])
