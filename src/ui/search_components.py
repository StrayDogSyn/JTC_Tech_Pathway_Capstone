"""
Search components and functionality for the weather dashboard.

This module provides search bar, suggestions, and search history management.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Callable, List, Any, Union
from threading import Timer

from ..utils.logging import get_logger
from .settings_manager import SettingsManager


logger = get_logger()


class SearchBarComponent:
    """Enhanced search bar with autocomplete and suggestions."""
    
    def __init__(self, parent: tk.Widget, settings_manager: SettingsManager):
        """Initialize the search bar component."""
        self.parent = parent
        self.settings = settings_manager
        self.search_callback: Optional[Callable[[str], None]] = None
        
        # Search variables
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        
        # UI components
        self.search_frame: Optional[tk.Widget] = None
        self.search_entry: Optional[tk.Entry] = None
        self.suggestions_listbox: Optional[tk.Listbox] = None
        self.suggestions_frame: Optional[tk.Widget] = None
        
        # State
        self._suggestion_timer: Optional[Timer] = None
        self._suggestions_visible = False
        
        logger.debug("SearchBarComponent initialized")
    
    def create_ui(self) -> tk.Widget:
        """Create the search bar UI."""
        try:
            # Main search frame
            self.search_frame = ttk.Frame(self.parent)
            
            # Search label
            search_label = ttk.Label(
                self.search_frame,
                text="🔍 Search Location:",
                font=("Segoe UI", 11, "bold")
            )
            search_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Search entry with enhanced styling
            self.search_entry = ttk.Entry(
                self.search_frame,
                textvariable=self.search_var,
                font=("Segoe UI", 11),
                width=30
            )
            self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
            
            # Bind events
            self.search_entry.bind('<Return>', self._on_search_submit)
            self.search_entry.bind('<FocusIn>', self._on_focus_in)
            self.search_entry.bind('<FocusOut>', self._on_focus_out)
            self.search_entry.bind('<KeyPress>', self._on_key_press)
            
            # Search button
            search_btn = ttk.Button(
                self.search_frame,
                text="Search",
                command=self._on_search_submit,
                style='success.TButton'
            )
            search_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Favorites button
            favorites_btn = ttk.Button(
                self.search_frame,
                text="⭐",
                command=self._show_favorites,
                width=3
            )
            favorites_btn.pack(side=tk.LEFT)
            
            # Create suggestions frame (initially hidden)
            self._create_suggestions_frame()
            
            logger.info("Search bar UI created successfully")
            return self.search_frame
            
        except Exception as e:
            logger.error(f"Error creating search bar UI: {e}")
            raise
    
    def _create_suggestions_frame(self) -> None:
        """Create the suggestions dropdown frame."""
        try:
            # Create frame positioned below search entry
            self.suggestions_frame = ttk.Frame(self.parent)
            
            # Suggestions listbox
            self.suggestions_listbox = tk.Listbox(
                self.suggestions_frame,
                height=6,
                font=("Segoe UI", 10),
                selectmode=tk.SINGLE
            )
            self.suggestions_listbox.pack(fill=tk.BOTH, expand=True)
            
            # Bind events
            self.suggestions_listbox.bind('<Double-Button-1>', self._on_suggestion_select)
            self.suggestions_listbox.bind('<Return>', self._on_suggestion_select)
            
            # Initially hidden
            self.suggestions_frame.pack_forget()
            
        except Exception as e:
            logger.error(f"Error creating suggestions frame: {e}")
    
    def _on_search_change(self, *args) -> None:
        """Handle search text changes for live suggestions."""
        try:
            # Cancel previous timer
            if self._suggestion_timer:
                self._suggestion_timer.cancel()
            
            # Set new timer for delayed suggestions
            self._suggestion_timer = Timer(0.3, self._update_suggestions)
            self._suggestion_timer.start()
            
        except Exception as e:
            logger.error(f"Error handling search change: {e}")
    
    def _update_suggestions(self) -> None:
        """Update the suggestions list based on current search text."""
        try:
            search_text = self.search_var.get().strip().lower()
            
            if len(search_text) < 2:
                self._hide_suggestions()
                return
            
            # Get suggestions from settings manager
            all_suggestions = self.settings.get_search_suggestions()
            
            # Filter suggestions based on search text
            filtered_suggestions = [
                suggestion for suggestion in all_suggestions
                if search_text in suggestion.lower()
            ]
            
            if filtered_suggestions:
                self._show_suggestions(filtered_suggestions)
            else:
                self._hide_suggestions()
                
        except Exception as e:
            logger.error(f"Error updating suggestions: {e}")
    
    def _show_suggestions(self, suggestions: List[str]) -> None:
        """Show the suggestions dropdown."""
        try:
            if not self.suggestions_listbox:
                return
            
            # Clear current suggestions
            self.suggestions_listbox.delete(0, tk.END)
            
            # Add new suggestions
            for suggestion in suggestions[:6]:  # Limit to 6 suggestions
                self.suggestions_listbox.insert(tk.END, suggestion)
            
            # Position and show the suggestions frame
            if not self._suggestions_visible and self.suggestions_frame:
                self.suggestions_frame.pack(fill=tk.X, pady=(5, 0))
                self._suggestions_visible = True
                
        except Exception as e:
            logger.error(f"Error showing suggestions: {e}")
    
    def _hide_suggestions(self) -> None:
        """Hide the suggestions dropdown."""
        try:
            if self._suggestions_visible and self.suggestions_frame:
                self.suggestions_frame.pack_forget()
                self._suggestions_visible = False
                
        except Exception as e:
            logger.error(f"Error hiding suggestions: {e}")
    
    def _on_focus_in(self, event=None) -> None:
        """Handle focus in event."""
        try:
            # Show recent searches/favorites when focused
            if not self.search_var.get().strip():
                suggestions = self.settings.get_search_suggestions()[:6]
                if suggestions:
                    self._show_suggestions(suggestions)
                    
        except Exception as e:
            logger.error(f"Error handling focus in: {e}")
    
    def _on_focus_out(self, event=None) -> None:
        """Handle focus out event."""
        try:
            # Delay hiding to allow suggestion selection
            Timer(0.2, self._hide_suggestions).start()
            
        except Exception as e:
            logger.error(f"Error handling focus out: {e}")
    
    def _on_key_press(self, event) -> Union[str, None]:
        """Handle key press events for navigation."""
        try:
            if not self._suggestions_visible:
                return None
            
            if event.keysym == 'Down':
                # Move to suggestions list
                if self.suggestions_listbox and self.suggestions_listbox.size() > 0:
                    self.suggestions_listbox.focus_set()
                    self.suggestions_listbox.selection_set(0)
                return 'break'
            elif event.keysym == 'Escape':
                self._hide_suggestions()
                return 'break'
                
        except Exception as e:
            logger.error(f"Error handling key press: {e}")
        return None
    
    def _on_suggestion_select(self, event=None) -> None:
        """Handle suggestion selection."""
        try:
            if not self.suggestions_listbox:
                return
            
            selection = self.suggestions_listbox.curselection()
            if selection:
                selected_text = self.suggestions_listbox.get(selection[0])
                self.search_var.set(selected_text)
                self._hide_suggestions()
                self._on_search_submit()
                
        except Exception as e:
            logger.error(f"Error handling suggestion selection: {e}")
    
    def _on_search_submit(self, event=None) -> None:
        """Handle search submission."""
        try:
            search_text = self.search_var.get().strip()
            if search_text and self.search_callback:
                # Add to recent searches
                self.settings.add_recent_search(search_text)
                
                # Hide suggestions
                self._hide_suggestions()
                
                # Call the search callback
                self.search_callback(search_text)
                
                logger.info(f"Search submitted: {search_text}")
                
        except Exception as e:
            logger.error(f"Error handling search submit: {e}")
    
    def _show_favorites(self) -> None:
        """Show favorites in suggestions."""
        try:
            favorites = self.settings.favorites_list
            if favorites:
                self._show_suggestions(favorites)
            else:
                logger.info("No favorites to show")
                
        except Exception as e:
            logger.error(f"Error showing favorites: {e}")
    
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set the search callback function."""
        self.search_callback = callback
        logger.debug("Search callback set")
    
    def set_text(self, text: str) -> None:
        """Set the search text."""
        try:
            self.search_var.set(text)
            
        except Exception as e:
            logger.error(f"Error setting search text: {e}")
    
    def get_text(self) -> str:
        """Get the current search text."""
        return self.search_var.get().strip()
    
    def clear(self) -> None:
        """Clear the search text."""
        try:
            self.search_var.set("")
            self._hide_suggestions()
            
        except Exception as e:
            logger.error(f"Error clearing search: {e}")
    
    def focus(self) -> None:
        """Set focus to the search entry."""
        try:
            if self.search_entry:
                self.search_entry.focus_set()
                
        except Exception as e:
            logger.error(f"Error setting focus: {e}")
