"""
Stellaris Save Editor - Main GUI Application
A graphical interface for editing Stellaris save files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from save_handler import StellarisSaveFile


class StellarisSaveEditor:
    """Main GUI application for the Stellaris Save Editor"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Stellaris Save Editor")
        self.root.geometry("900x700")
        
        self.save_file = None
        self.current_file_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Save File...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file_cmd)
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # File info section
        info_frame = ttk.LabelFrame(main_frame, text="Save File Information", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.file_label = ttk.Label(info_frame, text="No file loaded", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="Empire:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.empire_label = ttk.Label(info_frame, text="-", foreground="gray")
        self.empire_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="Date:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.date_label = ttk.Label(info_frame, text="-", foreground="gray")
        self.date_label.grid(row=2, column=1, sticky=tk.W)
        
        # Quick actions
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(actions_frame, text="Open Save File", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Reload", command=self.reload_file, state=tk.DISABLED).pack(side=tk.LEFT, padx=(0, 5))
        self.reload_button = ttk.Button(actions_frame, text="Reload", command=self.reload_file, state=tk.DISABLED)
        self.reload_button.pack_forget()
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Resources tab
        self.resources_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.resources_frame, text="Resources")
        self.setup_resources_tab()
        
        # Empire tab
        self.empire_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.empire_frame, text="Empire")
        self.setup_empire_tab()
        
        # Technologies tab
        self.tech_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tech_frame, text="Technologies")
        self.setup_tech_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def setup_resources_tab(self):
        """Setup the resources editing tab"""
        # Instructions
        ttk.Label(self.resources_frame, text="Edit your empire's resources:", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Resource entries
        self.resource_entries = {}
        resources = [
            ('energy', 'Energy Credits'),
            ('minerals', 'Minerals'),
            ('food', 'Food'),
            ('alloys', 'Alloys'),
            ('consumer_goods', 'Consumer Goods'),
            ('exotic_gases', 'Exotic Gases'),
            ('rare_crystals', 'Rare Crystals'),
            ('volatile_motes', 'Volatile Motes'),
            ('sr_living_metal', 'Living Metal'),
            ('sr_zro', 'Zro'),
            ('sr_dark_matter', 'Dark Matter'),
        ]
        
        for idx, (res_id, res_name) in enumerate(resources, start=1):
            ttk.Label(self.resources_frame, text=f"{res_name}:").grid(row=idx, column=0, sticky=tk.W, padx=(0, 10), pady=2)
            
            entry = ttk.Entry(self.resources_frame, width=20)
            entry.grid(row=idx, column=1, sticky=tk.W, pady=2)
            self.resource_entries[res_id] = entry
            
            btn = ttk.Button(self.resources_frame, text="Set", 
                           command=lambda r=res_id: self.set_resource(r))
            btn.grid(row=idx, column=2, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Apply all button
        ttk.Button(self.resources_frame, text="Apply All Changes", 
                  command=self.apply_all_resources,
                  style='Accent.TButton').grid(row=len(resources)+2, column=0, columnspan=3, pady=20)
    
    def setup_empire_tab(self):
        """Setup the empire statistics tab"""
        ttk.Label(self.empire_frame, text="Empire Statistics:", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Unity
        ttk.Label(self.empire_frame, text="Unity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.unity_entry = ttk.Entry(self.empire_frame, width=20)
        self.unity_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Button(self.empire_frame, text="Set", 
                  command=self.set_unity).grid(row=1, column=2, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Influence
        ttk.Label(self.empire_frame, text="Influence:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.influence_entry = ttk.Entry(self.empire_frame, width=20)
        self.influence_entry.grid(row=2, column=1, sticky=tk.W, pady=2)
        ttk.Button(self.empire_frame, text="Set", 
                  command=self.set_influence).grid(row=2, column=2, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Apply all button
        ttk.Button(self.empire_frame, text="Apply All Changes", 
                  command=self.apply_all_empire,
                  style='Accent.TButton').grid(row=4, column=0, columnspan=3, pady=20)
    
    def setup_tech_tab(self):
        """Setup the technologies tab"""
        ttk.Label(self.tech_frame, text="Technologies:", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Tech list
        list_frame = ttk.Frame(self.tech_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.tech_frame.rowconfigure(1, weight=1)
        self.tech_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tech_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=20)
        self.tech_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tech_listbox.yview)
        
        # Add tech section
        add_frame = ttk.Frame(self.tech_frame)
        add_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(add_frame, text="Add Technology:").pack(side=tk.LEFT, padx=(0, 5))
        self.tech_entry = ttk.Entry(add_frame, width=40)
        self.tech_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(add_frame, text="Add", command=self.add_technology).pack(side=tk.LEFT)
        
        ttk.Label(self.tech_frame, text="Example: tech_battleships, tech_jump_drive, tech_mega_engineering", 
                 foreground="gray", font=('TkDefaultFont', 8)).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
    
    def open_file(self):
        """Open a save file"""
        filename = filedialog.askopenfilename(
            title="Select Stellaris Save File",
            filetypes=[("Stellaris Save Files", "*.sav"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.status_bar.config(text="Loading save file...")
                self.root.update()
                
                self.save_file = StellarisSaveFile(filename)
                self.current_file_path = filename
                
                # Update UI
                self.file_label.config(text=os.path.basename(filename), foreground="black")
                self.empire_label.config(text=self.save_file.get_empire_name(), foreground="black")
                self.date_label.config(text=self.save_file.get_game_date(), foreground="black")
                
                # Load resources
                self.load_resources()
                self.load_empire_stats()
                self.load_technologies()
                
                self.status_bar.config(text=f"Loaded: {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Save file loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load save file:\n{str(e)}")
                self.status_bar.config(text="Error loading file")
    
    def reload_file(self):
        """Reload the current file"""
        if self.current_file_path:
            try:
                self.save_file.load(self.current_file_path)
                self.load_resources()
                self.load_empire_stats()
                self.load_technologies()
                self.status_bar.config(text="File reloaded")
                messagebox.showinfo("Success", "Save file reloaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reload file:\n{str(e)}")
    
    def load_resources(self):
        """Load resources into the UI"""
        if not self.save_file:
            return
        
        resources = self.save_file.get_resources()
        for res_id, entry in self.resource_entries.items():
            value = resources.get(res_id, 0)
            entry.delete(0, tk.END)
            entry.insert(0, str(int(value)))
    
    def load_empire_stats(self):
        """Load empire statistics into the UI"""
        if not self.save_file:
            return
        
        unity = self.save_file.get_unity()
        self.unity_entry.delete(0, tk.END)
        self.unity_entry.insert(0, str(int(unity)))
        
        influence = self.save_file.get_influence()
        self.influence_entry.delete(0, tk.END)
        self.influence_entry.insert(0, str(int(influence)))
    
    def load_technologies(self):
        """Load technologies into the UI"""
        if not self.save_file:
            return
        
        self.tech_listbox.delete(0, tk.END)
        techs = self.save_file.get_technologies()
        for tech in techs:
            self.tech_listbox.insert(tk.END, tech)
    
    def set_resource(self, resource_id):
        """Set a specific resource"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        entry = self.resource_entries[resource_id]
        try:
            value = float(entry.get())
            self.save_file.set_resource(resource_id, value)
            self.status_bar.config(text=f"Updated {resource_id} to {value}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def apply_all_resources(self):
        """Apply all resource changes"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        try:
            for res_id, entry in self.resource_entries.items():
                value = float(entry.get())
                self.save_file.set_resource(res_id, value)
            
            self.status_bar.config(text="All resources updated")
            messagebox.showinfo("Success", "All resources have been updated!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all resources!")
    
    def set_unity(self):
        """Set unity value"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        try:
            value = float(self.unity_entry.get())
            self.save_file.set_unity(value)
            self.status_bar.config(text=f"Updated Unity to {value}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def set_influence(self):
        """Set influence value"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        try:
            value = float(self.influence_entry.get())
            self.save_file.set_influence(value)
            self.status_bar.config(text=f"Updated Influence to {value}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def apply_all_empire(self):
        """Apply all empire stat changes"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        try:
            unity = float(self.unity_entry.get())
            influence = float(self.influence_entry.get())
            
            self.save_file.set_unity(unity)
            self.save_file.set_influence(influence)
            
            self.status_bar.config(text="Empire statistics updated")
            messagebox.showinfo("Success", "Empire statistics have been updated!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def add_technology(self):
        """Add a technology"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        tech_id = self.tech_entry.get().strip()
        if not tech_id:
            messagebox.showwarning("Warning", "Please enter a technology ID!")
            return
        
        if self.save_file.add_technology(tech_id):
            self.tech_listbox.insert(tk.END, tech_id)
            self.tech_entry.delete(0, tk.END)
            self.status_bar.config(text=f"Added technology: {tech_id}")
        else:
            messagebox.showwarning("Warning", "Technology may already exist or could not be added!")
    
    def save_file_cmd(self):
        """Save the current file"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        try:
            self.save_file.save()
            self.status_bar.config(text="Save file saved successfully")
            messagebox.showinfo("Success", "Save file has been saved!\n\nA backup was created with .backup extension.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def save_as_file(self):
        """Save as a new file"""
        if not self.save_file:
            messagebox.showwarning("Warning", "Please load a save file first!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".sav",
            filetypes=[("Stellaris Save Files", "*.sav"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.save_file.save(filename)
                self.current_file_path = filename
                self.file_label.config(text=os.path.basename(filename))
                self.status_bar.config(text=f"Saved as: {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Save file has been saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                          "Stellaris Save Editor v1.0\n\n"
                          "A tool for editing Stellaris save files.\n\n"
                          "Features:\n"
                          "- Edit resources\n"
                          "- Modify empire statistics\n"
                          "- Add technologies\n\n"
                          "Always backup your save files!")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = StellarisSaveEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
