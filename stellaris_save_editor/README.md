# Stellaris Save Editor

A Python-based GUI application for editing Stellaris save files. This tool allows you to modify resources, empire statistics, and technologies in your Stellaris game saves.

## Features

- **Resource Editing**: Modify all major resources including:
  - Energy Credits
  - Minerals
  - Food
  - Alloys
  - Consumer Goods
  - Strategic Resources (Exotic Gases, Rare Crystals, Volatile Motes)
  - Special Resources (Living Metal, Zro, Dark Matter)

- **Empire Statistics**: Edit empire-wide values:
  - Unity points
  - Influence points

- **Technology Management**: Add technologies to your empire's research pool

- **Safe Editing**: Automatic backup creation before saving changes

- **User-Friendly GUI**: Simple tabbed interface built with tkinter

## Requirements

- Python 3.7 or higher
- tkinter (usually comes with Python)

## Installation

1. Clone or download this repository
2. No additional packages required - uses Python standard library only!

## Usage

### Running the Application

```bash
python stellaris_save_editor.py
```

### Editing a Save File

1. **Open a Save File**:
   - Click "File" → "Open Save File..." or use the "Open Save File" button
   - Navigate to your Stellaris save directory (usually in `Documents/Paradox Interactive/Stellaris/save games/`)
   - Select your `.sav` file

2. **Edit Resources**:
   - Go to the "Resources" tab
   - Enter the desired values for each resource
   - Click "Set" for individual resources or "Apply All Changes" for all at once

3. **Edit Empire Statistics**:
   - Go to the "Empire" tab
   - Modify Unity and Influence values
   - Click the respective "Set" buttons or "Apply All Changes"

4. **Add Technologies**:
   - Go to the "Technologies" tab
   - View currently unlocked technologies in the list
   - Enter a technology ID in the text field (e.g., `tech_battleships`)
   - Click "Add" to unlock the technology

5. **Save Your Changes**:
   - Click "File" → "Save" to overwrite the original file (backup created automatically)
   - Or click "File" → "Save As..." to save to a new file

## File Structure

```
save_editor/
├── parser.py                    # Clausewitz format parser
├── save_handler.py              # Save file handler and editor
├── stellaris_save_editor.py     # Main GUI application
└── README.md                    # This file
```

## How It Works

Stellaris save files are ZIP archives containing two files:
- `meta`: Metadata about the save (empire name, date, etc.)
- `gamestate`: The actual game state in Clausewitz engine format

The editor:
1. Extracts the ZIP archive
2. Parses the Clausewitz format text files
3. Modifies the data structure
4. Serializes back to Clausewitz format
5. Creates a new ZIP archive

## Common Technology IDs

Here are some popular technology IDs you can add:

### Ship Types
- `tech_destroyers`
- `tech_cruisers`
- `tech_battleships`
- `tech_titans`
- `tech_colossus`

### FTL & Movement
- `tech_jump_drive`
- `tech_psi_jump_drive_1`

### Megastructures
- `tech_mega_engineering`
- `tech_ring_world`
- `tech_dyson_sphere`
- `tech_matter_decompressor`
- `tech_strategic_coordination`

### Weapons
- `tech_energy_lance_1`
- `tech_arc_emitter_1`
- `tech_energy_torpedoes_1`
- `tech_antimatter_missile`

### Defense
- `tech_shields_5`
- `tech_armor_5`
- `tech_psionic_shield`

## Important Notes

⚠️ **Always backup your save files before editing!** The application creates automatic backups with `.backup` extension, but it's good practice to keep your own backups.

⚠️ **Ironman saves cannot be edited** - This tool only works with regular (non-ironman) save files.

⚠️ **Game version compatibility** - This editor is designed for current versions of Stellaris. If the game format changes significantly in future updates, the parser may need adjustments.

## Troubleshooting

### "Failed to load save file"
- Ensure the file is a valid Stellaris save file (`.sav`)
- Make sure the file isn't corrupted
- Check that you have read permissions for the file

### "Failed to save file"
- Verify you have write permissions in the target directory
- Make sure the original file isn't open in another application
- Check available disk space

### Changes not appearing in-game
- Make sure you loaded the edited save file in Stellaris
- Verify the save file was actually modified (check file timestamp)
- Some changes may require game restart to take effect

## Limitations

- Cannot edit Ironman saves (they're encrypted)
- Some complex game mechanics may not be fully editable
- Technology prerequisites are not validated
- Changes to some values may be recalculated by the game on load

## License

This is a community tool for educational and personal use. Stellaris is owned by Paradox Interactive.

## Contributing

Feel free to submit issues, feature requests, or pull requests!

## Disclaimer

Use this tool at your own risk. Always backup your save files. This is an unofficial tool and is not affiliated with or endorsed by Paradox Interactive.
