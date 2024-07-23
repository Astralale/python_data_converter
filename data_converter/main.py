import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from loader import load_csv, save_csv, load_json, save_json, load_xml, save_xml, load_yaml, save_yaml
from stats import calculate_stats, display_stats
from filter import filter_data, advanced_filter_data
from sorter import sort_data, sort_data_multiple


class DataConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Converter and Filter")

        # Load File
        self.load_label = tk.Label(root, text="Load File")
        self.load_label.grid(row=0, column=0, padx=10, pady=10)

        self.load_file_button = tk.Button(root, text="Choose File", command=self.load_file)
        self.load_file_button.grid(row=0, column=1, padx=10, pady=10)

        self.load_format = tk.StringVar(value="csv")
        self.load_format_menu = tk.OptionMenu(root, self.load_format, "csv", "json", "xml", "yaml")
        self.load_format_menu.grid(row=0, column=2, padx=10, pady=10)

        # Save File
        self.save_label = tk.Label(root, text="Save File")
        self.save_label.grid(row=1, column=0, padx=10, pady=10)

        self.save_file_button = tk.Button(root, text="Save File", command=self.save_file)
        self.save_file_button.grid(row=1, column=1, padx=10, pady=10)

        self.save_format = tk.StringVar(value="csv")
        self.save_format_menu = tk.OptionMenu(root, self.save_format, "csv", "json", "xml", "yaml")
        self.save_format_menu.grid(row=1, column=2, padx=10, pady=10)

        # Display Stats
        self.stats_button = tk.Button(root, text="Display Stats", command=self.display_stats)
        self.stats_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Filter Data
        self.filter_label = tk.Label(root, text="Filter Criteria")
        self.filter_label.grid(row=3, column=0, padx=10, pady=10)

        self.filter_entry = tk.Entry(root)
        self.filter_entry.grid(row=3, column=1, padx=10, pady=10)

        self.filter_button = tk.Button(root, text="Filter Data", command=self.filter_data)
        self.filter_button.grid(row=3, column=2, padx=10, pady=10)

        # Advanced Filter Data
        self.adv_filter_label = tk.Label(root, text="Advanced Filter Criteria")
        self.adv_filter_label.grid(row=4, column=0, padx=10, pady=10)

        self.adv_filter_entry = tk.Entry(root)
        self.adv_filter_entry.grid(row=4, column=1, padx=10, pady=10)

        self.adv_filter_button = tk.Button(root, text="Advanced Filter Data", command=self.advanced_filter_data)
        self.adv_filter_button.grid(row=4, column=2, padx=10, pady=10)

        # Sort Data
        self.sort_label = tk.Label(root, text="Sort Key")
        self.sort_label.grid(row=5, column=0, padx=10, pady=10)

        self.sort_entry = tk.Entry(root)
        self.sort_entry.grid(row=5, column=1, padx=10, pady=10)

        self.sort_button = tk.Button(root, text="Sort Data", command=self.sort_data)
        self.sort_button.grid(row=5, column=2, padx=10, pady=10)

        # Sort Multiple Data
        self.sort_multiple_label = tk.Label(root, text="Sort Keys (comma separated)")
        self.sort_multiple_label.grid(row=6, column=0, padx=10, pady=10)

        self.sort_multiple_entry = tk.Entry(root)
        self.sort_multiple_entry.grid(row=6, column=1, padx=10, pady=10)

        self.sort_multiple_button = tk.Button(root, text="Sort Multiple Data", command=self.sort_multiple_data)
        self.sort_multiple_button.grid(row=6, column=2, padx=10, pady=10)

        # Text Box for Output
        self.output_text = tk.Text(root, wrap='word', height=20, width=60)
        self.output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

        self.data = None

    def load_file(self):
        file_path = filedialog.askopenfilename()
        file_format = self.load_format.get()
        if not file_path:
            return

        try:
            if file_format == "csv":
                self.data = load_csv(file_path)
            elif file_format == "json":
                self.data = load_json(file_path)
            elif file_format == "xml":
                self.data = load_xml(file_path)
            elif file_format == "yaml":
                self.data = load_yaml(file_path)
            else:
                messagebox.showerror("Error", f"Unsupported format: {file_format}")
                return

            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(self.data))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension="." + self.save_format.get())
        file_format = self.save_format.get()
        if not file_path:
            return

        try:
            if file_format == "csv":
                save_csv(self.data, file_path)
            elif file_format == "json":
                save_json(self.data, file_path)
            elif file_format == "xml":
                save_xml(self.data, file_path)
            elif file_format == "yaml":
                save_yaml(self.data, file_path)
            else:
                messagebox.showerror("Error", f"Unsupported format: {file_format}")
                return

            messagebox.showinfo("Success", f"Data saved to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_stats(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded")
            return

        try:
            stats = calculate_stats(self.data)
            self.output_text.delete('1.0', tk.END)
            for key, stat in stats.items():
                self.output_text.insert(tk.END, f"Stats for {key}:\n")
                for stat_key, stat_value in stat.items():
                    self.output_text.insert(tk.END, f"  {stat_key}: {stat_value}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def filter_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded")
            return

        criteria_str = self.filter_entry.get()
        if not criteria_str:
            messagebox.showerror("Error", "No criteria provided")
            return

        try:
            criteria = {kv.split("=")[0]: kv.split("=")[1] for kv in criteria_str.split(",")}
            filtered_data = filter_data(self.data, criteria)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(filtered_data))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def advanced_filter_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded")
            return

        criteria_str = self.adv_filter_entry.get()
        if not criteria_str:
            messagebox.showerror("Error", "No criteria provided")
            return

        try:
            criteria = {}
            for kv in criteria_str.split(","):
                key, val = kv.split("=")
                if ":" in val:
                    op, value = val.split(":")
                    criteria[key] = (op, value)
                else:
                    criteria[key] = val

            advanced_filtered_data = advanced_filter_data(self.data, criteria)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(advanced_filtered_data))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def sort_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded")
            return

        key = self.sort_entry.get()
        if not key:
            messagebox.showerror("Error", "No key provided")
            return

        try:
            sorted_data = sort_data(self.data, key)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(sorted_data))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def sort_multiple_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded")
            return

        keys_str = self.sort_multiple_entry.get()
        if not keys_str:
            messagebox.showerror("Error", "No keys provided")
            return

        try:
            keys = keys_str.split(",")
            sorted_data = sort_data_multiple(self.data, keys)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, str(sorted_data))

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataConverterApp(root)
    root.mainloop()
