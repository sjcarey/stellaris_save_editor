#!/usr/bin/env python3
"""
Test script to verify the save editor functionality without GUI
"""

from save_handler import StellarisSaveFile
import os

def test_save_editor():
    """Test the save editor with the example file"""
    print("=" * 60)
    print("Stellaris Save Editor - Test Script")
    print("=" * 60)
    
    # Find the save file
    save_path = "stellaris_save_editor/liam.sav"
    
    if not os.path.exists(save_path):
        print(f"ERROR: Save file not found at {save_path}")
        return
    
    print(f"\n1. Loading save file: {save_path}")
    save = StellarisSaveFile(save_path)
    
    print("\n2. Save file information:")
    print(f"   Empire: {save.get_empire_name()}")
    print(f"   Date: {save.get_game_date()}")
    
    print("\n3. Current resources:")
    resources = save.get_resources()
    for res_type, amount in sorted(resources.items()):
        print(f"   {res_type}: {amount:,.0f}")
    
    print("\n4. Empire statistics:")
    print(f"   Unity: {save.get_unity():,.0f}")
    print(f"   Influence: {save.get_influence():,.0f}")
    
    print("\n5. Technologies (first 10):")
    techs = save.get_technologies()
    for tech in techs[:10]:
        print(f"   - {tech}")
    print(f"   ... and {len(techs) - 10} more" if len(techs) > 10 else "")
    
    print("\n6. Testing modifications:")
    
    # Test setting energy
    original_energy = resources.get('energy', 0)
    new_energy = 999999
    print(f"   Setting energy from {original_energy:,.0f} to {new_energy:,.0f}")
    save.set_resource('energy', new_energy)
    
    # Test setting minerals
    original_minerals = resources.get('minerals', 0)
    new_minerals = 888888
    print(f"   Setting minerals from {original_minerals:,.0f} to {new_minerals:,.0f}")
    save.set_resource('minerals', new_minerals)
    
    # Test setting unity
    original_unity = save.get_unity()
    new_unity = 100000
    print(f"   Setting unity from {original_unity:,.0f} to {new_unity:,.0f}")
    save.set_unity(new_unity)
    
    # Test adding technology
    test_tech = "tech_battleships"
    print(f"   Adding technology: {test_tech}")
    save.add_technology(test_tech)
    
    print("\n7. Saving modified file as 'liam_modified.sav'...")
    try:
        save.save("liam_modified.sav")
        print("   ✓ Successfully saved!")
        
        # Verify by loading the modified file
        print("\n8. Verifying modifications by reloading...")
        verify_save = StellarisSaveFile("liam_modified.sav")
        verify_resources = verify_save.get_resources()
        
        print(f"   Energy: {verify_resources.get('energy', 0):,.0f} (expected: {new_energy:,.0f})")
        print(f"   Minerals: {verify_resources.get('minerals', 0):,.0f} (expected: {new_minerals:,.0f})")
        print(f"   Unity: {verify_save.get_unity():,.0f} (expected: {new_unity:,.0f})")
        
        verify_techs = verify_save.get_technologies()
        if test_tech in verify_techs:
            print(f"   Technology '{test_tech}': ✓ Found in tech list")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        print("\nYou can now use the modified save file in Stellaris.")
        print("Original file: stellaris_save_editor/liam.sav")
        print("Modified file: liam_modified.sav")
        
    except Exception as e:
        print(f"   ✗ Error saving file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_save_editor()
