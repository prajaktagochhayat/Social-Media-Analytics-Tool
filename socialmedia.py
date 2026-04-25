"""
Social Media Analytics Tool
Interactive dashboard to analyze Instagram & Twitter engagement metrics.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import os

class SocialMediaAnalytics:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Social Media Analytics Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        
        # Data storage
        self.instagram_data = pd.DataFrame()
        self.twitter_data = pd.DataFrame()
        self.insta_file = ""
        self.twitter_file = ""
        
        self.create_widgets()
    
    def load_file(self, platform):
        """Load CSV file using file browser"""
        filename = filedialog.askopenfilename(
            title=f"Select {platform} Data CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if platform == "Instagram":
                    self.instagram_data = pd.read_csv(filename)
                    self.insta_file = filename
                    messagebox.showinfo("Success", f"✅ Instagram data loaded!\n📊 Posts: {len(self.instagram_data)}")
                else:  # Twitter
                    self.twitter_data = pd.read_csv(filename)
                    self.twitter_file = filename
                    messagebox.showinfo("Success", f"✅ Twitter data loaded!\n📱 Tweets: {len(self.twitter_data)}")
                
                self.update_info()
                self.update_chart()
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to load {platform} data:\n{str(e)}")
    
    def create_widgets(self):
        """Create the dashboard UI"""
        # Header
        header = tk.Label(self.root, text="🌐 Social Media Analytics Tool", 
                         font=("Arial", 24, "bold"), bg="#f8f9fa", fg="#2c3e50")
        header.pack(pady=20)
        
        # File loading section
        file_frame = tk.LabelFrame(self.root, text="📁 Load Social Media Data", 
                                  font=("Arial", 14, "bold"), bg="#f8f9fa")
        file_frame.pack(pady=10, padx=30, fill="x")
        
        # Instagram load button
        insta_btn = tk.Button(file_frame, text="📸 Load Instagram CSV", 
                             command=lambda: self.load_file("Instagram"),
                             bg="#e4405f", fg="white", font=("Arial", 12, "bold"),
                             width=22, height=2)
        insta_btn.pack(pady=15, padx=20, side=tk.LEFT)
        
        # Twitter load button
        twitter_btn = tk.Button(file_frame, text="🐦 Load Twitter CSV", 
                               command=lambda: self.load_file("Twitter"),
                               bg="#1da1f2", fg="white", font=("Arial", 12, "bold"),
                               width=22, height=2)
        twitter_btn.pack(pady=15, padx=20, side=tk.LEFT)
        
        # Controls frame
        controls_frame = tk.Frame(self.root, bg="#f8f9fa")
        controls_frame.pack(pady=15)
        
        # Chart selector
        tk.Label(controls_frame, text="📊 Select Analysis:", 
                font=("Arial", 14, "bold"), bg="#f8f9fa").pack(side=tk.LEFT, padx=10)
        self.chart_var = tk.StringVar(value="Engagement Comparison")
        charts = ttk.Combobox(controls_frame, textvariable=self.chart_var,
                             values=["Engagement Comparison", "Likes Over Time", 
                                    "Platform Performance", "Top Content", "Engagement by Hashtag"],
                             state="readonly", width=25, font=("Arial", 11))
        charts.pack(side=tk.LEFT, padx=10)
        charts.bind('<<ComboboxSelected>>', self.update_chart)
        
        # Refresh button
        refresh_btn = tk.Button(controls_frame, text="🔄 Refresh Analysis", 
                               command=self.update_chart, bg="#27ae60", fg="white",
                               font=("Arial", 12, "bold"))
        refresh_btn.pack(side=tk.LEFT, padx=15)
        
        # Info display
        self.info_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.info_frame.pack(pady=10)
        self.info_label = tk.Label(self.info_frame, 
                                  text="👆 Load Instagram & Twitter CSV files to start analysis!",
                                  font=("Arial", 13), bg="#f8f9fa", fg="#7f8c8d")
        self.info_label.pack()
        
        self.files_label = tk.Label(self.info_frame, text="", font=("Arial", 10), 
                                   bg="#f8f9fa", fg="#95a5a6")
        self.files_label.pack()
        
        # Insights section
        insights_frame = tk.LabelFrame(self.root, text="💡 Key Insights", 
                                      font=("Arial", 14, "bold"), bg="#f8f9fa")
        insights_frame.pack(pady=10, padx=30, fill="x")
        self.insights_label = tk.Label(insights_frame, 
                                      text="Load data to see actionable insights here...",
                                      font=("Arial", 11), bg="#f8f9fa", fg="#7f8c8d")
        self.insights_label.pack(pady=15)
        
        # Chart area
        self.chart_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        welcome_msg = tk.Label(self.chart_frame, 
                              text="🎉 Welcome to Social Media Analytics!\n\n"
                                   "1. Click the Instagram & Twitter buttons above\n"
                                   "2. Select your CSV data files\n"
                                   "3. Choose analysis type from dropdown\n"
                                   "4. Watch insights & charts appear! ✨",
                              font=("Arial", 14), bg="#f8f9fa", fg="#2c3e50")
        welcome_msg.pack(expand=True)
    
    def update_info(self):
        """Update data info and files display"""
        insta_count = len(self.instagram_data)
        twitter_count = len(self.twitter_data)
        
        info_text = f"📸 Instagram: {insta_count} posts | 🐦 Twitter: {twitter_count} tweets"
        self.info_label.config(text=info_text, fg="#2c3e50")
        
        files_text = f"📁 Instagram: {os.path.basename(self.insta_file) if self.insta_file else 'Not loaded'} | "
        files_text += f"🐦 Twitter: {os.path.basename(self.twitter_file) if self.twitter_file else 'Not loaded'}"
        self.files_label.config(text=files_text)
    
    def generate_insights(self):
        """Generate actionable business insights"""
        insights = []
        
        if not self.instagram_data.empty:
            avg_likes_insta = self.instagram_data['Likes'].mean()
            insights.append(f"📈 Instagram avg likes/post: {avg_likes_insta:.0f}")
        
        if not self.twitter_data.empty:
            avg_likes_twitter = self.twitter_data['Likes'].mean()
            insights.append(f"📈 Twitter avg likes/tweet: {avg_likes_twitter:.0f}")
        
        if not self.instagram_data.empty and not self.twitter_data.empty:
            total_insta_eng = self.instagram_data['Likes'].sum() + self.instagram_data['Comments'].sum()
            total_twitter_eng = self.twitter_data['Likes'].sum() + self.twitter_data['Retweets'].sum()
            
            if total_insta_eng > total_twitter_eng:
                insights.append("🏆 Instagram has higher overall engagement!")
            else:
                insights.append("🏆 Twitter has higher overall engagement!")
        
        return "\n".join(insights) if insights else "Load data to see insights..."
    
    def create_engagement_comparison(self):
        """Bar chart comparing platforms"""
        if self.instagram_data.empty or self.twitter_data.empty:
            return False
        
        # Calculate metrics
        insta_likes = self.instagram_data['Likes'].sum()
        insta_comments = self.instagram_data['Comments'].sum()
        twitter_likes = self.twitter_data['Likes'].sum()
        twitter_retweets = self.twitter_data['Retweets'].sum()
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        platforms = ['Instagram Likes', 'Instagram Comments', 'Twitter Likes', 'Twitter Retweets']
        values = [insta_likes, insta_comments, twitter_likes, twitter_retweets]
        colors = ['#e4405f', '#e4405f', '#1da1f2', '#1da1f2']
        
        bars = self.ax.bar(platforms, values, color=colors, alpha=0.8)
        self.ax.set_title('📊 Engagement Comparison: Instagram vs Twitter', fontsize=18, fontweight='bold', pad=20)
        self.ax.set_ylabel('Total Count', fontsize=14)
        self.ax.tick_params(axis='x', rotation=15)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                        f'{int(value):,}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return True
    
    def create_likes_over_time(self):
        """Line chart of likes trend"""
        if self.instagram_data.empty and self.twitter_data.empty:
            return False
        
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        
        if not self.instagram_data.empty:
            self.instagram_data['Date'] = pd.to_datetime(self.instagram_data['Date'])
            daily_insta = self.instagram_data.groupby('Date')['Likes'].sum()
            daily_insta.plot(ax=self.ax, label='Instagram', marker='o', linewidth=3, markersize=8, color='#e4405f')
        
        if not self.twitter_data.empty:
            self.twitter_data['Date'] = pd.to_datetime(self.twitter_data['Date'])
            daily_twitter = self.twitter_data.groupby('Date')['Likes'].sum()
            daily_twitter.plot(ax=self.ax, label='Twitter', marker='s', linewidth=3, markersize=8, color='#1da1f2')
        
        self.ax.set_title('📈 Likes Over Time', fontsize=18, fontweight='bold', pad=20)
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Total Likes')
        self.ax.legend(fontsize=12)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        return True
    
    def create_platform_performance(self):
        """Pie chart of platform share"""
        if self.instagram_data.empty or self.twitter_data.empty:
            return False
        
        total_insta = self.instagram_data['Likes'].sum() + self.instagram_data['Comments'].sum()
        total_twitter = self.twitter_data['Likes'].sum() + self.twitter_data['Retweets'].sum()
        
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        sizes = [total_insta, total_twitter]
        labels = ['Instagram', 'Twitter']
        colors = ['#e4405f', '#1da1f2']
        
        wedges, texts, autotexts = self.ax.pie(sizes, labels=labels, colors=colors, 
                                               autopct='%1.1f%%', startangle=90, textprops={'fontsize': 14})
        self.ax.set_title('🥧 Platform Performance Share', fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        return True
    
    def create_top_content(self):
        """Bar chart of top performing posts"""
        if self.instagram_data.empty and self.twitter_data.empty:
            return False
        
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        
        top_posts = []
        if not self.instagram_data.empty:
            top_posts.extend(self.instagram_data.nlargest(5, 'Likes')[['Content', 'Likes']].values)
        if not self.twitter_data.empty:
            top_posts.extend(self.twitter_data.nlargest(5, 'Likes')[['Content', 'Likes']].values)
        
        top_posts = top_posts[:5]  # Top 5 overall
        contents = [post[0][:30] + "..." for post in top_posts]
        likes = [post[1] for post in top_posts]
        
        bars = self.ax.barh(contents, likes, color=['#e4405f']*len(contents))
        self.ax.set_title('⭐ Top 5 Performing Content', fontsize=18, fontweight='bold', pad=20)
        self.ax.set_xlabel('Likes')
        
        for i, (bar, like) in enumerate(zip(bars, likes)):
            self.ax.text(like + max(likes)*0.01, bar.get_y() + bar.get_height()/2, 
                        f'{int(like):,}', va='center', fontweight='bold')
        
        plt.tight_layout()
        return True
    
    def update_chart(self, event=None):
        """Main chart update function"""
        # Clear chart frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        self.update_info()
        
        # Update insights
        insights_text = self.generate_insights()
        self.insights_label.config(text=insights_text)
        
        chart_type = self.chart_var.get()
        
        # No data message
        if self.instagram_data.empty and self.twitter_data.empty:
            no_data = tk.Label(self.chart_frame, text="📊 Load Instagram & Twitter data first!", 
                              font=("Arial", 16), bg="#f8f9fa", fg="#e74c3c")
            no_data.pack(expand=True)
            return
        
        # Create specific chart
        chart_funcs = {
            "Engagement Comparison": self.create_engagement_comparison,
            "Likes Over Time": self.create_likes_over_time,
            "Platform Performance": self.create_platform_performance,
            "Top Content": self.create_top_content
        }
        
        if chart_type in chart_funcs:
            if chart_funcs[chart_type]():
                canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                error_msg = tk.Label(self.chart_frame, text=f"❌ Need {chart_type.split()[0]} data for this chart", 
                                   font=("Arial", 14), bg="#f8f9fa", fg="#e74c3c")
                error_msg.pack(expand=True)

def main():
    """Run the application"""
    root = tk.Tk()
    app = SocialMediaAnalytics(root)
    root.mainloop()

if __name__ == "__main__":
    main()