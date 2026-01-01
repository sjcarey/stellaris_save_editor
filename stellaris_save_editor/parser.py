"""
Stellaris Save File Parser
Handles parsing and writing of Clausewitz engine format files
"""

import re
from typing import Any, Dict, List, Union


class ClausewitzParser:
    """Parser for Clausewitz engine format (used by Stellaris save files)"""
    
    def __init__(self):
        self.data = {}
        self.max_depth = 50  # Prevent stack overflow on deeply nested structures
    
    def parse(self, content: str, parse_all: bool = False) -> Dict[str, Any]:
        """Parse Clausewitz format content into a dictionary
        
        Args:
            content: The text content to parse
            parse_all: If False, only parse top-level structure for large files
        """
        self.data = {}
        
        # For very large files, only parse the top level to avoid hanging
        if not parse_all and len(content) > 10000000:  # > 10MB
            print("Large file detected, using fast parse mode...")
            return self._fast_parse(content)
        
        self._parse_block(content, self.data)
        return self.data
    
    def _fast_parse(self, content: str) -> Dict[str, Any]:
        """Fast parse that only gets top-level keys and keeps raw content"""
        result = {}
        i = 0
        
        while i < len(content):
            # Skip whitespace
            while i < len(content) and content[i].isspace():
                i += 1
            
            if i >= len(content):
                break
            
            # Look for key=value or key={ patterns
            match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*', content[i:])
            if match:
                key = match.group(1)
                i += match.end()
                
                # Skip whitespace after =
                while i < len(content) and content[i].isspace():
                    i += 1
                
                if i < len(content) and content[i] == '{':
                    # Find matching closing brace
                    start = i
                    depth = 0
                    while i < len(content):
                        if content[i] == '{':
                            depth += 1
                        elif content[i] == '}':
                            depth -= 1
                            if depth == 0:
                                i += 1
                                break
                        i += 1
                    
                    # Store raw content for this block
                    raw_content = content[start:i]
                    result[key] = {'_raw': raw_content, '_parsed': False}
                else:
                    # Simple value
                    value_match = re.match(r'("[^"]*"|[^\s\n]+)', content[i:])
                    if value_match:
                        result[key] = value_match.group(1).strip('"')
                        i += value_match.end()
            else:
                i += 1
        
        return result
    
    def _parse_block(self, content: str, parent: Dict[str, Any], start: int = 0) -> int:
        """Recursively parse a block of Clausewitz format"""
        i = start
        key = None
        
        while i < len(content):
            char = content[i]
            
            # Skip whitespace and newlines
            if char.isspace():
                i += 1
                continue
            
            # Handle comments
            if char == '#':
                while i < len(content) and content[i] != '\n':
                    i += 1
                continue
            
            # Handle block end
            if char == '}':
                return i + 1
            
            # Handle block start
            if char == '{':
                if key is not None:
                    # Parse nested block
                    sub_dict = {}
                    i = self._parse_block(content, sub_dict, i + 1)
                    
                    # Handle multiple values for the same key
                    if key in parent:
                        if not isinstance(parent[key], list):
                            parent[key] = [parent[key]]
                        parent[key].append(sub_dict)
                    else:
                        parent[key] = sub_dict
                    key = None
                else:
                    # Anonymous block (list item)
                    sub_dict = {}
                    i = self._parse_block(content, sub_dict, i + 1)
                    
                    # Add to parent as list item
                    if isinstance(parent, dict) and '' not in parent:
                        parent[''] = []
                    if isinstance(parent, dict):
                        parent[''].append(sub_dict)
                continue
            
            # Parse key=value or key
            match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*', content[i:])
            if match:
                key = match.group(1)
                i += match.end()
                continue
            
            # Parse quoted string value
            if char == '"':
                end_quote = i + 1
                while end_quote < len(content) and content[end_quote] != '"':
                    if content[end_quote] == '\\':
                        end_quote += 2
                    else:
                        end_quote += 1
                value = content[i + 1:end_quote]
                i = end_quote + 1
                
                if key:
                    if key in parent:
                        if not isinstance(parent[key], list):
                            parent[key] = [parent[key]]
                        parent[key].append(value)
                    else:
                        parent[key] = value
                    key = None
                continue
            
            # Parse unquoted value (number or identifier)
            match = re.match(r'(-?[0-9]+\.?[0-9]*|yes|no|[a-zA-Z_][a-zA-Z0-9_]*)', content[i:])
            if match:
                value_str = match.group(1)
                i += match.end()
                
                # Try to convert to appropriate type
                if value_str == 'yes':
                    value = True
                elif value_str == 'no':
                    value = False
                elif '.' in value_str:
                    try:
                        value = float(value_str)
                    except ValueError:
                        value = value_str
                else:
                    try:
                        value = int(value_str)
                    except ValueError:
                        value = value_str
                
                if key:
                    if key in parent:
                        if not isinstance(parent[key], list):
                            parent[key] = [parent[key]]
                        parent[key].append(value)
                    else:
                        parent[key] = value
                    key = None
                continue
            
            # Skip unknown characters
            i += 1
        
        return i
    
    def serialize(self, data: Dict[str, Any], indent: int = 0) -> str:
        """Serialize a dictionary back to Clausewitz format"""
        lines = []
        indent_str = '\t' * indent
        
        for key, value in data.items():
            if key == '':  # Anonymous list items
                for item in value:
                    lines.append(f"{indent_str}{{")
                    if isinstance(item, dict):
                        lines.append(self.serialize(item, indent + 1))
                    lines.append(f"{indent_str}}}")
            elif isinstance(value, dict):
                lines.append(f"{indent_str}{key}=")
                lines.append(f"{indent_str}{{")
                lines.append(self.serialize(value, indent + 1))
                lines.append(f"{indent_str}}}")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{indent_str}{key}=")
                        lines.append(f"{indent_str}{{")
                        lines.append(self.serialize(item, indent + 1))
                        lines.append(f"{indent_str}}}")
                    else:
                        lines.append(f"{indent_str}{key}={self._format_value(item)}")
            else:
                lines.append(f"{indent_str}{key}={self._format_value(value)}")
        
        return '\n'.join(lines)
    
    def _format_value(self, value: Any) -> str:
        """Format a value for serialization"""
        if isinstance(value, bool):
            return 'yes' if value else 'no'
        elif isinstance(value, str):
            # Quote strings that contain spaces or special characters
            if ' ' in value or any(c in value for c in '{}="'):
                return f'"{value}"'
            return f'"{value}"'
        else:
            return str(value)
