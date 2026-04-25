#Data Visualization Dashboard 

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import os

class CompanyDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Company Data Visualization Dashboard")
        self.root.geometry("1100x750")
        
        # Initialize empty dataframes
        self.sales_data = pd.DataFrame()
        self.customer_data = pd.DataFrame()
        self.sales_file = ""
        self.customer_file = ""
        
        # Create GUI
        self.create_widgets()
    
    def browse_file(self, data_type):
        """Open file browser to select CSV file"""
        filename = filedialog.askopenfilename(
            title=f"Select {data_type} CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if data_type == "Sales":
                    self.sales_data = pd.read_csv(filename)
                    self.sales_file = filename
                    messagebox.showinfo("Success", f"✅ Sales data loaded!\nRows: {len(self.sales_data)}")
                elif data_type == "Customer":
                    self.customer_data = pd.read_csv(filename)
                    self.customer_file = filename
                    messagebox.showinfo("Success", f"✅ Customer data loaded!\nRows: {len(self.customer_data)}")
                
                self.update_info()
                self.update_chart()  # Refresh chart after loading
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error loading file:\n{str(e)}")
    
    def create_widgets(self):
        """Create main dashboard interface"""
        # Title
        title_label = tk.Label(self.root, text="🏢 Company Data Dashboard", 
                              font=("Arial", 20, "bold"), fg="#2c3e50")
        title_label.pack(pady=10)
        
        # File loading frame
        file_frame = tk.LabelFrame(self.root, text="📁 Load Data Files", font=("Arial", 12, "bold"))
        file_frame.pack(pady=10, padx=20, fill="x")
        
        # Sales file button
        sales_btn = tk.Button(file_frame, text="📊 Load Sales CSV", 
                             command=lambda: self.browse_file("Sales"),
                             bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                             width=20, height=2)
        sales_btn.pack(pady=10, padx=20, side=tk.LEFT)
        
        # Customer file button
        customer_btn = tk.Button(file_frame, text="👥 Load Customer CSV", 
                                command=lambda: self.browse_file("Customer"),
                                bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                                width=20, height=2)
        customer_btn.pack(pady=10, padx=20, side=tk.LEFT)
        
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Chart dropdown
        tk.Label(control_frame, text="📈 Select Chart:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.chart_var = tk.StringVar(value="Sales by Product")
        chart_combo = ttk.Combobox(control_frame, textvariable=self.chart_var,
                                  values=["Sales by Product", "Sales Over Time", 
                                         "Revenue by Region", "Customer Distribution"],
                                  state="readonly", width=20)
        chart_combo.pack(side=tk.LEFT, padx=5)
        chart_combo.bind('<<ComboboxSelected>>', self.update_chart)
        
        # Region filter
        tk.Label(control_frame, text="🌍 Filter Region:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(20,5))
        self.region_var = tk.StringVar(value="All")
        region_combo = ttk.Combobox(control_frame, textvariable=self.region_var,
                                   values=["All", "North", "South", "East", "West"],
                                   state="readonly", width=15)
        region_combo.pack(side=tk.LEFT, padx=5)
        region_combo.bind('<<ComboboxSelected>>', self.update_chart)
        
        # Refresh button
        refresh_btn = tk.Button(control_frame, text="🔄 Update Chart", 
                               command=self.update_chart, bg="#27ae60", fg="white",
                               font=("Arial", 10, "bold"))
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # Data info frame
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=5)
        self.info_label = tk.Label(self.info_frame, text="👆 Click buttons above to load CSV files first!", 
                                  font=("Arial", 11), fg="#7f8c8d")
        self.info_label.pack()
        
        # Current files display
        self.file_label = tk.Label(self.info_frame, text="", font=("Arial", 9), fg="#95a5a6")
        self.file_label.pack()
        
        # Chart frame
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Welcome message
        welcome_label = tk.Label(self.chart_frame, text="Welcome! Load your CSV files using the buttons above to start visualizing data.",
                                font=("Arial", 12), fg="#7f8c8d")
        welcome_label.pack(expand=True)
    
    def update_info(self):
        """Update data information display"""
        sales_count = len(self.sales_data)
        customer_count = len(self.customer_data)
        
        info_text = f"📊 Sales: {sales_count} rows | 👥 Customers: {customer_count} rows"
        
        if self.sales_file:
            info_text += f" | 📁 Sales: {os.path.basename(self.sales_file)}"
        if self.customer_file:
            info_text += f" | 📁 Customers: {os.path.basename(self.customer_file)}"
        
        self.info_label.config(text=info_text, fg="#2c3e50")
        
        # Update file label
        file_text = f"Loaded: {self.sales_file or 'No sales file'} | {self.customer_file or 'No customer file'}"
        self.file_label.config(text=file_text)
    
    def filter_data(self, data, region):
        """Filter data by region"""
        if region == "All" or data.empty:
            return data
        if 'Region' in data.columns:
            return data[data['Region'] == region]
        return data
    
    def create_chart(self, chart_type):
        """Create specific chart"""
        if chart_type == "Sales by Product" and not self.sales_data.empty:
            filtered_data = self.filter_data(self.sales_data, self.region_var.get())
            if filtered_data.empty: return
            product_sales = filtered_data.groupby('Product')['Units_Sold'].sum()
            
            self.fig, self.ax = plt.subplots(figsize=(9, 5))
            product_sales.plot(kind='bar', ax=self.ax, color=['#e74c3c', '#3498db'])
            self.ax.set_title('📊 Sales by Product', fontsize=16, fontweight='bold', pad=20)
            self.ax.set_xlabel('Product')
            self.ax.set_ylabel('Units Sold')
            self.ax.tick_params(axis='x', rotation=0)
            
        elif chart_type == "Sales Over Time" and not self.sales_data.empty:
            filtered_data = self.filter_data(self.sales_data, self.region_var.get())
            if filtered_data.empty: return
            filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
            daily_sales = filtered_data.groupby('Date')['Units_Sold'].sum()
            
            self.fig, self.ax = plt.subplots(figsize=(10, 5))
            daily_sales.plot(kind='line', ax=self.ax, marker='o', linewidth=3, markersize=8, color='#f39c12')
            self.ax.set_title('📈 Sales Over Time', fontsize=16, fontweight='bold', pad=20)
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Units Sold')
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
            
        elif chart_type == "Revenue by Region" and not self.sales_data.empty:
            filtered_data = self.filter_data(self.sales_data, self.region_var.get())
            if filtered_data.empty: return
            region_revenue = filtered_data.groupby('Region')['Revenue'].sum()
            
            self.fig, self.ax = plt.subplots(figsize=(8, 6))
            colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
            region_revenue.plot(kind='pie', ax=self.ax, autopct='%1.1f%%', 
                              startangle=90, colors=colors, textprops={'fontsize': 12})
            self.ax.set_title('💰 Revenue by Region', fontsize=16, fontweight='bold', pad=20)
            
        elif chart_type == "Customer Distribution" and not self.customer_data.empty:
            filtered_data = self.filter_data(self.customer_data, self.region_var.get())
            if filtered_data.empty: return
            region_customers = filtered_data['Region'].value_counts()
            
            self.fig, self.ax = plt.subplots(figsize=(9, 5))
            region_customers.plot(kind='bar', ax=self.ax, color=['#9b59b6', '#1abc9c', '#34495e', '#e67e22'])
            self.ax.set_title('👥 Customer Distribution by Region', fontsize=16, fontweight='bold', pad=20)
            self.ax.set_xlabel('Region')
            self.ax.set_ylabel('Number of Customers')
            self.ax.tick_params(axis='x', rotation=0)
        
        else:
            return False
        
        plt.tight_layout()
        return True
    
    def update_chart(self, event=None):
        """Update chart display"""
        # Clear previous widgets
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        self.update_info()
        
        chart_type = self.chart_var.get()
        
        # Show welcome if no data
        if self.sales_data.empty and self.customer_data.empty:
            welcome_label = tk.Label(self.chart_frame, 
                                   text="👆 Load CSV files first using the red/blue buttons above!",
                                   font=("Arial", 14), fg="#e74c3c")
            welcome_label.pack(expand=True)
            return
        
        # Create and display chart
        if self.create_chart(chart_type):
            canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            error_label = tk.Label(self.chart_frame, 
                                 text=f"❌ No data available for '{chart_type}' or selected filter",
                                 font=("Arial", 12), fg="#e74c3c")
            error_label.pack(expand=True)

def main():
    root = tk.Tk()
    app = CompanyDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()