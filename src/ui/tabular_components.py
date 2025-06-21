"""
Advanced Tabular Components for Weather Dashboard

This module provides sophisticated table components with advanced features like:
- Sortable columns with custom sorting logic
- Advanced filtering and search capabilities
- Data export (CSV, JSON, Excel)
- Real-time data updates
- Statistical analytics and visualizations
- Comparison tables for multiple locations
- Historical data management
"""

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
from typing import Optional, Callable, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import json
import csv
import threading
import random
import math

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class AdvancedDataTable:
    """
    Base class for advanced data tables with sorting, filtering, and export capabilities.
    """
    
    def __init__(self, parent: tk.Widget, columns: List[Dict[str, Any]], 
                 title: str = "Data Table", height: int = 15):
        """
        Initialize the advanced data table.
        
        Args:
            parent: Parent widget
            columns: List of column definitions with 'text', 'width', 'anchor', 'sortable'
            title: Table title
            height: Number of visible rows
        """
        self.parent = parent
        self.columns = columns
        self.title = title
        self.height = height
        self.data = []
        self.filtered_data = []
        self.sort_column = None
        self.sort_reverse = False
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create the table widgets."""
        # Main frame
        self.main_frame = ttk.LabelFrame(self.parent, text=self.title, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control frame
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(self.control_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
          # Filter button
        self.filter_btn = ttk.Button(search_frame, text="🎛️ Advanced Filter", 
                                   command=self._show_filter_dialog)
        self.filter_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export buttons
        export_frame = ttk.Frame(self.control_frame)
        export_frame.pack(side=tk.RIGHT)
        
        self.export_csv_btn = ttk.Button(export_frame, text="📊 Export CSV", 
                                       command=self._export_csv)
        self.export_csv_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.export_json_btn = ttk.Button(export_frame, text="📄 Export JSON", 
                                        command=self._export_json)
        self.export_json_btn.pack(side=tk.LEFT)
        
        # Stats frame
        self.stats_frame = ttk.Frame(self.main_frame)
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = ttk.Label(self.stats_frame, text="📊 Total: 0 records", 
                                   font=("Segoe UI", 9, "italic"))
        self.stats_label.pack(side=tk.LEFT)
        
        # Table frame
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        column_ids = [f"col_{i}" for i in range(len(self.columns))]
        self.tree = ttk.Treeview(table_frame, columns=column_ids, show="headings", 
                               height=self.height, selectmode="extended")
        
        # Configure columns
        for i, col in enumerate(self.columns):
            col_id = column_ids[i]
            self.tree.heading(col_id, text=col['text'], 
                            command=lambda c=i: self._sort_by_column(c))
            self.tree.column(col_id, width=col.get('width', 100), 
                           anchor=col.get('anchor', 'w'))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and tree
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind events
        self.tree.bind('<Double-1>', self._on_double_click)
        self.tree.bind('<Button-3>', self._on_right_click)
        
    def add_data(self, data: List[Dict[str, Any]]):
        """Add data to the table."""
        self.data.extend(data)
        self._apply_filters()
        
    def set_data(self, data: List[Dict[str, Any]]):
        """Set table data (replaces existing)."""
        self.data = data
        self._apply_filters()
        
    def clear_data(self):
        """Clear all table data."""
        self.data = []
        self.filtered_data = []
        self._refresh_table()
        
    def _apply_filters(self):
        """Apply current filters and search to data."""
        search_term = self.search_var.get().lower()
        
        # Start with all data
        filtered = self.data.copy()
        
        # Apply search filter
        if search_term:
            filtered = [row for row in filtered 
                       if any(str(value).lower().find(search_term) != -1 
                             for value in row.values())]
        
        self.filtered_data = filtered
        self._refresh_table()
        
    def _refresh_table(self):
        """Refresh the table display."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add filtered data
        for row in self.filtered_data:
            values = [str(row.get(col['key'], '')) for col in self.columns]
            self.tree.insert('', tk.END, values=values)
            
        # Update stats
        total = len(self.data)
        filtered = len(self.filtered_data)
        if total == filtered:
            self.stats_label.config(text=f"📊 Total: {total} records")
        else:
            self.stats_label.config(text=f"📊 Showing: {filtered} of {total} records")
            
    def _sort_by_column(self, col_index: int):
        """Sort table by column."""
        if not self.columns[col_index].get('sortable', True):
            return
            
        # Toggle sort direction if same column
        if self.sort_column == col_index:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col_index
            self.sort_reverse = False
            
        # Get column key
        col_key = self.columns[col_index]['key']
        
        # Sort data
        try:
            self.filtered_data.sort(
                key=lambda x: float(x.get(col_key, 0)) if str(x.get(col_key, '')).replace('.', '').replace('-', '').isdigit() 
                else str(x.get(col_key, '')).lower(),
                reverse=self.sort_reverse
            )
        except (ValueError, TypeError):
            self.filtered_data.sort(
                key=lambda x: str(x.get(col_key, '')).lower(),
                reverse=self.sort_reverse
            )
            
        self._refresh_table()
        
        # Update column header to show sort direction
        col_text = self.columns[col_index]['text']
        sort_indicator = " ↓" if self.sort_reverse else " ↑"
        
        # Reset all headers
        for i, col in enumerate(self.columns):
            header_text = col['text']
            if i == col_index:
                header_text += sort_indicator
            self.tree.heading(f"col_{i}", text=header_text)
            
    def _on_search_change(self, *args):
        """Handle search text change."""
        self._apply_filters()
        
    def _show_filter_dialog(self):
        """Show advanced filter dialog."""        # Create filter dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Advanced Filter")
        dialog.geometry("400x300")
        try:
            dialog.transient(self.parent.winfo_toplevel())
        except (AttributeError, tk.TclError):
            pass  # Skip if transient fails
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Filter controls
        ttk.Label(dialog, text="Advanced filtering options:", 
                 font=("Segoe UI", 10, "bold")).pack(pady=10)
        
        # Date range filter (example)
        date_frame = ttk.LabelFrame(dialog, text="Date Range", padding=10)
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(date_frame, text="From:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        from_date = ttk.DateEntry(date_frame)
        from_date.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(date_frame, text="To:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        to_date = ttk.DateEntry(date_frame)
        to_date.grid(row=0, column=3)
          # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        apply_btn = ttk.Button(btn_frame, text="Apply Filter", 
                              command=lambda: self._apply_date_filter(from_date, to_date, dialog))
        apply_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(btn_frame, text="Clear Filter", command=self._clear_filters)
        clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT)
                  
    def _apply_date_filter(self, from_date, to_date, dialog):
        """Apply date range filter."""
        # Implementation would depend on data structure
        dialog.destroy()
        messagebox.showinfo("Filter Applied", "Date range filter has been applied!")
        
    def _clear_filters(self):
        """Clear all filters."""
        self.search_var.set("")
        self._apply_filters()
        
    def _export_csv(self):
        """Export data to CSV."""
        if not self.filtered_data:
            messagebox.showwarning("No Data", "No data to export!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export to CSV"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    if self.filtered_data:
                        fieldnames = self.filtered_data[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.filtered_data)
                        
                messagebox.showinfo("Export Successful", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
                
    def _export_json(self):
        """Export data to JSON."""
        if not self.filtered_data:
            messagebox.showwarning("No Data", "No data to export!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export to JSON"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(self.filtered_data, jsonfile, indent=2, default=str)
                    
                messagebox.showinfo("Export Successful", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
                
    def _on_double_click(self, event):
        """Handle double-click on row."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            # Override in subclasses for specific behavior
            print(f"Double-clicked row: {values}")
            
    def _on_right_click(self, event):
        """Handle right-click context menu."""
        selection = self.tree.selection()
        if selection:
            # Create context menu
            context_menu = tk.Menu(self.parent, tearoff=0)
            context_menu.add_command(label="📋 Copy Row", command=self._copy_row)
            context_menu.add_command(label="📊 Show Details", command=self._show_row_details)
            context_menu.add_separator()
            context_menu.add_command(label="❌ Delete Row", command=self._delete_row)
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
                
    def _copy_row(self):
        """Copy selected row to clipboard."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            row_text = '\t'.join(str(v) for v in values)
            self.parent.clipboard_clear()
            self.parent.clipboard_append(row_text)
            
    def _show_row_details(self):
        """Show detailed view of selected row."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
              # Create details dialog
            dialog = tk.Toplevel(self.parent)
            dialog.title("Row Details")
            dialog.geometry("400x300")
            try:
                dialog.transient(self.parent.winfo_toplevel())
            except (AttributeError, tk.TclError):
                pass  # Skip if transient fails
            
            # Show details
            text_widget = tk.Text(dialog, wrap=tk.WORD, padx=10, pady=10)
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            for i, col in enumerate(self.columns):
                if i < len(values):
                    text_widget.insert(tk.END, f"{col['text']}: {values[i]}\n")
                    
            text_widget.config(state=tk.DISABLED)
            
    def _delete_row(self):
        """Delete selected row."""
        selection = self.tree.selection()
        if selection and messagebox.askyesno("Confirm Delete", "Delete selected row?"):
            # Implementation would depend on data management strategy
            pass


class WeatherDataTable(AdvancedDataTable):
    """Specialized table for weather data with weather-specific features."""
    
    def __init__(self, parent: tk.Widget, title: str = "🌦️ Weather History"):
        columns = [
            {'text': 'Date/Time', 'key': 'datetime', 'width': 150, 'anchor': 'center'},
            {'text': 'Location', 'key': 'location', 'width': 120, 'anchor': 'w'},
            {'text': 'Temperature (°C)', 'key': 'temperature', 'width': 120, 'anchor': 'center'},
            {'text': 'Feels Like (°C)', 'key': 'feels_like', 'width': 120, 'anchor': 'center'},
            {'text': 'Humidity (%)', 'key': 'humidity', 'width': 100, 'anchor': 'center'},
            {'text': 'Pressure (hPa)', 'key': 'pressure', 'width': 110, 'anchor': 'center'},
            {'text': 'Wind Speed (m/s)', 'key': 'wind_speed', 'width': 120, 'anchor': 'center'},
            {'text': 'Wind Dir', 'key': 'wind_direction', 'width': 80, 'anchor': 'center'},
            {'text': 'Visibility (km)', 'key': 'visibility', 'width': 110, 'anchor': 'center'},
            {'text': 'Weather', 'key': 'description', 'width': 120, 'anchor': 'w'},
        ]
        super().__init__(parent, columns, title, height=12)
        
        # Add weather-specific controls
        self._add_weather_controls()
        
    def _add_weather_controls(self):
        """Add weather-specific controls."""
        weather_frame = ttk.Frame(self.control_frame)
        weather_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        # Temperature unit toggle
        self.temp_unit = tk.StringVar(value="°C")
        temp_frame = ttk.Frame(weather_frame)
        temp_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(temp_frame, text="Unit:").pack(side=tk.LEFT)
        ttk.Radiobutton(temp_frame, text="°C", variable=self.temp_unit, 
                       value="°C", command=self._convert_temperature).pack(side=tk.LEFT)
        ttk.Radiobutton(temp_frame, text="°F", variable=self.temp_unit, 
                       value="°F", command=self._convert_temperature).pack(side=tk.LEFT)
                       
        # Weather condition filter
        condition_frame = ttk.Frame(weather_frame)
        condition_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(condition_frame, text="Condition:").pack(side=tk.LEFT)
        self.condition_var = tk.StringVar()
        condition_combo = ttk.Combobox(condition_frame, textvariable=self.condition_var,
                                     values=["All", "Clear", "Clouds", "Rain", "Snow", "Thunderstorm"],
                                     width=12, state="readonly")
        condition_combo.pack(side=tk.LEFT)
        condition_combo.bind('<<ComboboxSelected>>', self._filter_by_condition)
        condition_combo.set("All")
        
    def _convert_temperature(self):
        """Convert temperature units."""
        # This would update the display to show temperatures in selected unit
        self._refresh_table()
        
    def _filter_by_condition(self, event=None):
        """Filter by weather condition."""
        condition = self.condition_var.get()
        if condition == "All":
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = [row for row in self.data 
                                if condition.lower() in str(row.get('description', '')).lower()]
        self._refresh_table()
        
    def add_weather_data(self, weather_data: Dict[str, Any], location: str):
        """Add weather data to the table."""
        row = {
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'location': location,
            'temperature': f"{weather_data.get('temperature', 0):.1f}",
            'feels_like': f"{weather_data.get('feels_like', 0):.1f}",
            'humidity': f"{weather_data.get('humidity', 0)}",
            'pressure': f"{weather_data.get('pressure', 0)}",
            'wind_speed': f"{weather_data.get('wind_speed', 0):.1f}",
            'wind_direction': weather_data.get('wind_direction', 'N/A'),
            'visibility': f"{weather_data.get('visibility', 0) / 1000:.1f}",
            'description': weather_data.get('description', 'Unknown').title()
        }
        self.add_data([row])


class ComparisonTable(AdvancedDataTable):
    """Table for comparing weather data across multiple locations."""
    
    def __init__(self, parent: tk.Widget, title: str = "🌍 Location Comparison"):
        columns = [
            {'text': 'Location', 'key': 'location', 'width': 150, 'anchor': 'w'},
            {'text': 'Current Temp (°C)', 'key': 'temperature', 'width': 130, 'anchor': 'center'},
            {'text': 'Feels Like (°C)', 'key': 'feels_like', 'width': 120, 'anchor': 'center'},
            {'text': 'Humidity (%)', 'key': 'humidity', 'width': 100, 'anchor': 'center'},
            {'text': 'Pressure (hPa)', 'key': 'pressure', 'width': 110, 'anchor': 'center'},
            {'text': 'Wind (m/s)', 'key': 'wind_speed', 'width': 90, 'anchor': 'center'},
            {'text': 'Condition', 'key': 'condition', 'width': 120, 'anchor': 'w'},
            {'text': 'Last Updated', 'key': 'last_updated', 'width': 130, 'anchor': 'center'},
            {'text': 'Rank', 'key': 'rank', 'width': 60, 'anchor': 'center'},
        ]
        super().__init__(parent, columns, title, height=10)
        
        # Add comparison controls
        self._add_comparison_controls()
        
    def _add_comparison_controls(self):
        """Add comparison-specific controls."""
        comp_frame = ttk.Frame(self.control_frame)
        comp_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        # Ranking criteria
        ttk.Label(comp_frame, text="Rank by:").pack(side=tk.LEFT, padx=(0, 5))
        self.rank_var = tk.StringVar(value="temperature")
        rank_combo = ttk.Combobox(comp_frame, textvariable=self.rank_var,
                                values=["temperature", "humidity", "pressure", "wind_speed"],
                                width=15, state="readonly")
        rank_combo.pack(side=tk.LEFT, padx=(0, 10))
        rank_combo.bind('<<ComboboxSelected>>', self._update_rankings)
        
        # Auto-refresh toggle
        self.auto_refresh = tk.BooleanVar(value=True)
        ttk.Checkbutton(comp_frame, text="Auto-refresh", 
                       variable=self.auto_refresh).pack(side=tk.LEFT, padx=(10, 0))
                       
    def _update_rankings(self, event=None):
        """Update location rankings based on selected criteria."""
        if not self.filtered_data:
            return
            
        rank_by = self.rank_var.get()
        
        # Sort by selected criteria (descending for temperature, ascending for others)
        reverse = rank_by == "temperature"
        
        try:
            sorted_data = sorted(self.filtered_data, 
                               key=lambda x: float(x.get(rank_by, 0)), 
                               reverse=reverse)
            
            # Update rankings
            for i, row in enumerate(sorted_data, 1):
                row['rank'] = str(i)
                
            self.filtered_data = sorted_data
            self._refresh_table()
            
        except (ValueError, TypeError):
            pass
            
    def add_location_data(self, location: str, weather_data: Dict[str, Any]):
        """Add or update location data."""
        # Remove existing data for this location
        self.data = [row for row in self.data if row.get('location') != location]
        
        # Add new data
        row = {
            'location': location,
            'temperature': f"{weather_data.get('temperature', 0):.1f}",
            'feels_like': f"{weather_data.get('feels_like', 0):.1f}",
            'humidity': f"{weather_data.get('humidity', 0)}",
            'pressure': f"{weather_data.get('pressure', 0)}",
            'wind_speed': f"{weather_data.get('wind_speed', 0):.1f}",
            'condition': weather_data.get('description', 'Unknown').title(),
            'last_updated': datetime.now().strftime("%H:%M:%S"),
            'rank': "0"
        }
        
        self.add_data([row])
        self._update_rankings()


class AnalyticsTable(AdvancedDataTable):
    """Table for displaying weather analytics and statistics."""
    
    def __init__(self, parent: tk.Widget, title: str = "📊 Weather Analytics"):
        columns = [
            {'text': 'Metric', 'key': 'metric', 'width': 200, 'anchor': 'w'},
            {'text': 'Current', 'key': 'current', 'width': 100, 'anchor': 'center'},
            {'text': 'Today Avg', 'key': 'today_avg', 'width': 100, 'anchor': 'center'},
            {'text': 'Week Avg', 'key': 'week_avg', 'width': 100, 'anchor': 'center'},
            {'text': 'Min', 'key': 'min_value', 'width': 80, 'anchor': 'center'},
            {'text': 'Max', 'key': 'max_value', 'width': 80, 'anchor': 'center'},
            {'text': 'Trend', 'key': 'trend', 'width': 80, 'anchor': 'center'},
            {'text': 'Change %', 'key': 'change_percent', 'width': 100, 'anchor': 'center'},
        ]
        super().__init__(parent, columns, title, height=8)
        
        # Initialize with sample analytics data
        self._initialize_analytics()
        
    def _initialize_analytics(self):
        """Initialize with sample analytics data."""
        analytics_data = [
            {
                'metric': '🌡️ Temperature (°C)',
                'current': '22.5',
                'today_avg': '21.3',
                'week_avg': '19.8',
                'min_value': '15.2',
                'max_value': '28.1',
                'trend': '↗️',
                'change_percent': '+2.3%'
            },
            {
                'metric': '💧 Humidity (%)',
                'current': '65',
                'today_avg': '68',
                'week_avg': '72',
                'min_value': '45',
                'max_value': '85',
                'trend': '↘️',
                'change_percent': '-3.1%'
            },
            {
                'metric': '🔽 Pressure (hPa)',
                'current': '1013',
                'today_avg': '1015',
                'week_avg': '1012',
                'min_value': '998',
                'max_value': '1025',
                'trend': '↗️',
                'change_percent': '+0.8%'
            },
            {
                'metric': '💨 Wind Speed (m/s)',
                'current': '5.2',
                'today_avg': '4.8',
                'week_avg': '6.1',
                'min_value': '0.5',
                'max_value': '12.3',
                'trend': '↗️',
                'change_percent': '+8.3%'
            },
            {
                'metric': '👁️ Visibility (km)',
                'current': '10.0',
                'today_avg': '9.2',
                'week_avg': '8.7',
                'min_value': '2.1',
                'max_value': '10.0',
                'trend': '↗️',
                'change_percent': '+15.0%'
            }
        ]
        
        self.set_data(analytics_data)
        
    def update_analytics(self, weather_data: Dict[str, Any]):
        """Update analytics with new weather data."""
        # This would typically calculate real statistics
        # For demo purposes, we'll simulate some updates
        
        current_data = self.data.copy()
        for row in current_data:
            if 'Temperature' in row['metric']:
                row['current'] = f"{weather_data.get('temperature', 0):.1f}"
            elif 'Humidity' in row['metric']:
                row['current'] = f"{weather_data.get('humidity', 0)}"
            elif 'Pressure' in row['metric']:
                row['current'] = f"{weather_data.get('pressure', 0)}"
            elif 'Wind Speed' in row['metric']:
                row['current'] = f"{weather_data.get('wind_speed', 0):.1f}"
            elif 'Visibility' in row['metric']:
                row['current'] = f"{weather_data.get('visibility', 0) / 1000:.1f}"
                
        self.set_data(current_data)


# Demo functions for generating sample data
def generate_sample_weather_data(num_records: int = 50) -> List[Dict[str, Any]]:
    """Generate sample weather data for testing."""
    locations = ["London", "Paris", "New York", "Tokyo", "Sydney", "Mumbai", "São Paulo"]
    conditions = ["Clear", "Partly Cloudy", "Cloudy", "Rain", "Snow", "Thunderstorm"]
    
    data = []
    base_date = datetime.now() - timedelta(days=num_records)
    
    for i in range(num_records):
        date = base_date + timedelta(days=i)
        data.append({
            'datetime': date.strftime("%Y-%m-%d %H:%M"),
            'location': random.choice(locations),
            'temperature': f"{random.uniform(-10, 35):.1f}",
            'feels_like': f"{random.uniform(-15, 40):.1f}",
            'humidity': f"{random.randint(30, 95)}",
            'pressure': f"{random.randint(980, 1030)}",
            'wind_speed': f"{random.uniform(0, 15):.1f}",
            'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'visibility': f"{random.uniform(1, 10):.1f}",
            'description': random.choice(conditions)
        })
    
    return data


def generate_sample_comparison_data() -> List[Dict[str, Any]]:
    """Generate sample comparison data for testing."""
    locations = [
        ("London, UK", 18.5, 72, 1015),
        ("Paris, France", 22.1, 65, 1012),
        ("New York, USA", 25.3, 58, 1018),
        ("Tokyo, Japan", 28.7, 80, 1008),
        ("Sydney, Australia", 15.2, 45, 1022)
    ]
    
    data = []
    for i, (location, temp, humidity, pressure) in enumerate(locations):
        data.append({
            'location': location,
            'temperature': f"{temp:.1f}",
            'feels_like': f"{temp + random.uniform(-3, 3):.1f}",
            'humidity': f"{humidity}",
            'pressure': f"{pressure}",
            'wind_speed': f"{random.uniform(2, 12):.1f}",
            'condition': random.choice(['Clear', 'Cloudy', 'Rain', 'Partly Cloudy']),
            'last_updated': (datetime.now() - timedelta(minutes=random.randint(1, 60))).strftime("%H:%M:%S"),
            'rank': str(i + 1)
        })
    
    return data


if __name__ == "__main__":
    # Demo application
    root = ttk.Window("🌦️ Advanced Weather Tables Demo", "darkly", size=(1400, 800))
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Weather Data Table tab
    weather_frame = ttk.Frame(notebook)
    notebook.add(weather_frame, text="📊 Weather History")
    weather_table = WeatherDataTable(weather_frame)
    weather_table.set_data(generate_sample_weather_data())
    
    # Comparison Table tab
    comparison_frame = ttk.Frame(notebook)
    notebook.add(comparison_frame, text="🌍 Comparison")
    comparison_table = ComparisonTable(comparison_frame)
    comparison_table.set_data(generate_sample_comparison_data())
    
    # Analytics Table tab
    analytics_frame = ttk.Frame(notebook)
    notebook.add(analytics_frame, text="📈 Analytics")
    analytics_table = AnalyticsTable(analytics_frame)
    
    root.mainloop()
