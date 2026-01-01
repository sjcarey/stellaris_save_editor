"""
Stellaris Save File Handler
Manages loading, parsing, editing, and saving Stellaris save files
Uses regex-based editing for large files instead of full parsing
"""

import zipfile
import os
import shutil
import re
from typing import Dict, Any, Optional


class StellarisSaveFile:
    """Handler for Stellaris save files"""
    
    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath
        self.meta_content = ""
        self.gamestate_content = ""
        self.empire_name = ""
        self.game_date = ""
        
        if filepath:
            self.load(filepath)
    
    def load(self, filepath: str):
        """Load a Stellaris save file"""
        self.filepath = filepath
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
        
        print(f"Loading save file: {filepath}")
        
        # Extract the zip file
        with zipfile.ZipFile(filepath, 'r') as zf:
            # Read meta file
            self.meta_content = zf.read('meta').decode('utf-8', errors='ignore')
            
            # Read gamestate file
            self.gamestate_content = zf.read('gamestate').decode('utf-8', errors='ignore')
            print(f"Loaded gamestate ({len(self.gamestate_content) / 1024 / 1024:.1f} MB)")
        
        # Extract basic info
        name_match = re.search(r'name="([^"]+)"', self.meta_content)
        self.empire_name = name_match.group(1) if name_match else "Unknown"
        
        date_match = re.search(r'date="([^"]+)"', self.gamestate_content)
        self.game_date = date_match.group(1) if date_match else "Unknown"
        
        print("Save file loaded successfully!")
    
    def save(self, output_path: Optional[str] = None):
        """Save the modified save file"""
        if output_path is None:
            output_path = self.filepath
        
        # Create a backup
        if os.path.exists(output_path):
            backup_path = output_path + '.backup'
            shutil.copy2(output_path, backup_path)
            print(f"Backup created: {backup_path}")
        
        # Create the zip file
        print(f"Writing save file: {output_path}")
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('meta', self.meta_content.encode('utf-8'))
            zf.writestr('gamestate', self.gamestate_content.encode('utf-8'))
        
        print("Save complete!")
    
    def get_empire_name(self) -> str:
        """Get the empire name"""
        return self.empire_name
    
    def get_game_date(self) -> str:
        """Get the current game date"""
        return self.game_date
    
    def get_resources(self) -> Dict[str, float]:
        """Get the player's current resources"""
        resources = {}
        
        # Find the player section and country
        player_match = re.search(r'player=\s*\{\s*\{\s*name="[^"]*"\s*country=(\d+)', self.gamestate_content)
        if not player_match:
            return resources
        
        country_id = player_match.group(1)
        
        # Find resources for this country - look for patterns like:
        # resource={ type=energy accumulated=12345.0 }
        country_pattern = rf'country=\s*\{{\s*{country_id}='
        country_pos = re.search(country_pattern, self.gamestate_content)
        
        if country_pos:
            # Search in a reasonable range after the country definition
            search_start = country_pos.start()
            search_end = min(search_start + 500000, len(self.gamestate_content))
            country_section = self.gamestate_content[search_start:search_end]
            
            # Find resource entries
            resource_pattern = r'type=(\w+)\s+accumulated=([\d.]+)'
            for match in re.finditer(resource_pattern, country_section):
                resource_type = match.group(1)
                amount = float(match.group(2))
                resources[resource_type] = amount
        
        return resources
    
    def set_resource(self, resource_type: str, amount: float) -> bool:
        """Set a specific resource amount"""
        # Find the player's country
        player_match = re.search(r'player=\s*\{\s*\{\s*name="[^"]*"\s*country=(\d+)', self.gamestate_content)
        if not player_match:
            return False
        
        country_id = player_match.group(1)
        
        # Find the resource entry and replace it
        # Pattern: type=resource_name accumulated=12345.0
        pattern = rf'(type={resource_type}\s+accumulated=)([\d.]+)'
        
        def replace_func(match):
            return f'{match.group(1)}{amount}'
        
        new_content, count = re.subn(pattern, replace_func, self.gamestate_content, count=1)
        
        if count > 0:
            self.gamestate_content = new_content
            return True
        
        return False
    
    def get_unity(self) -> float:
        """Get unity points"""
        match = re.search(r'^\s*unity=([\d.]+)', self.gamestate_content, re.MULTILINE)
        return float(match.group(1)) if match else 0
    
    def set_unity(self, amount: float) -> bool:
        """Set unity points"""
        pattern = r'(^\s*unity=)([\d.]+)'
        new_content, count = re.subn(pattern, f'\\g<1>{amount}', self.gamestate_content, count=1, flags=re.MULTILINE)
        
        if count > 0:
            self.gamestate_content = new_content
            return True
        return False
    
    def get_influence(self) -> float:
        """Get influence points"""
        match = re.search(r'^\s*influence=([\d.]+)', self.gamestate_content, re.MULTILINE)
        return float(match.group(1)) if match else 0
    
    def set_influence(self, amount: float) -> bool:
        """Set influence points"""
        pattern = r'(^\s*influence=)([\d.]+)'
        new_content, count = re.subn(pattern, f'\\g<1>{amount}', self.gamestate_content, count=1, flags=re.MULTILINE)
        
        if count > 0:
            self.gamestate_content = new_content
            return True
        return False
    
    def get_technologies(self) -> list:
        """Get unlocked technologies"""
        techs = []
        
        # Find technology entries
        tech_pattern = r'technology="([^"]+)"'
        for match in re.finditer(tech_pattern, self.gamestate_content):
            tech = match.group(1)
            if tech not in techs:
                techs.append(tech)
        
        return techs[:50]  # Return first 50 to avoid overwhelming
    
    def add_technology(self, tech_id: str) -> bool:
        """Add a technology to the player's country"""
        # Find the player's country tech_status section
        player_match = re.search(r'player=\s*\{\s*\{\s*name="[^"]*"\s*country=(\d+)', self.gamestate_content)
        if not player_match:
            return False
        
        # Find tech_status section and add the technology
        tech_status_pattern = r'(tech_status=\s*\{\s*technology=\s*\{)'
        match = re.search(tech_status_pattern, self.gamestate_content)
        
        if match:
            # Insert the new technology after the opening brace
            insert_pos = match.end()
            new_tech_entry = f'\n\t\t\ttechnology="{tech_id}"'
            self.gamestate_content = (
                self.gamestate_content[:insert_pos] +
                new_tech_entry +
                self.gamestate_content[insert_pos:]
            )
            return True
        
        return False
