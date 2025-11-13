import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from meteostat import Point, Daily

class WeatherDataAnalyzer:
    def __init__(self, data_file=None):
        """Initialize the Weather Data Analyzer"""
        self.df = None
        if data_file:
            self.load_data(data_file)
    
    def load_data(self, file_path):
        """Load weather data from CSV file"""
        try:
            self.df = pd.read_csv(file_path)
            print(f"Data loaded successfully! Shape: {self.df.shape}")
            print(f"\nColumns: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def create_sample_data(self, days=365):
        """Create sample weather data for demonstration"""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate realistic weather data
        temp_base = 20 + 10 * np.sin(np.arange(days) * 2 * np.pi / 365)
        
        self.df = pd.DataFrame({
            'date': dates,
            'temperature': temp_base + np.random.randn(days) * 3,
            'precipitation': np.maximum(0, np.random.exponential(2, days)),
            'wind_speed': np.maximum(0, np.random.gamma(2, 2, days)),
            'pressure': 1013 + np.random.randn(days) * 10
        })
        
        self.df['date'] = pd.to_datetime(self.df['date'])
        print("Sample data created successfully!")
        return self.df
    
    def summary_statistics(self):
        """Display summary statistics for weather data"""
        if self.df is None:
            print("No data loaded!")
            return
        
        print("\n" + "="*60)
        print("WEATHER DATA SUMMARY STATISTICS")
        print("="*60)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            print(f"\n{col.upper()}:")
            print(f"  Mean:     {self.df[col].mean():.2f}")
            print(f"  Median:   {self.df[col].median():.2f}")
            print(f"  Std Dev:  {self.df[col].std():.2f}")
            print(f"  Min:      {self.df[col].min():.2f}")
            print(f"  Max:      {self.df[col].max():.2f}")
    
    def plot_temperature_trend(self):
        """Plot temperature trends over time"""
        if self.df is None:
            print("No data loaded!")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['date'], self.df['temperature'], linewidth=1, alpha=0.7)
        plt.title('Temperature Trend Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Temperature (°C)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_heatmap(self):
        """Plot correlation heatmap of weather variables"""
        if self.df is None:
            print("No data loaded!")
            return
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', 
                    cmap='coolwarm', center=0, square=True,
                    linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Weather Variables Correlation Heatmap', 
                  fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_monthly_averages(self):
        """Plot monthly average temperatures"""
        if self.df is None or 'date' not in self.df.columns:
            print("No data loaded or date column missing!")
            return
        
        df_copy = self.df.copy()
        df_copy['month'] = pd.to_datetime(df_copy['date']).dt.month
        monthly_avg = df_copy.groupby('month')['temperature'].mean()
        
        plt.figure(figsize=(10, 6))
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.bar(range(1, 13), monthly_avg, color='skyblue', edgecolor='navy')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Temperature (°C)', fontsize=12)
        plt.title('Monthly Average Temperature', fontsize=16, fontweight='bold')
        plt.xticks(range(1, 13), months)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_all_variables(self):
        """Create subplots for all weather variables"""
        if self.df is None:
            print("No data loaded!")
            return
        
        numeric_cols = [col for col in self.df.columns if col != 'date' 
                       and self.df[col].dtype in [np.float64, np.int64]]
        
        n_cols = len(numeric_cols)
        fig, axes = plt.subplots(n_cols, 1, figsize=(12, 4*n_cols))
        
        if n_cols == 1:
            axes = [axes]
        
        for idx, col in enumerate(numeric_cols):
            axes[idx].plot(self.df['date'], self.df[col], linewidth=1)
            axes[idx].set_title(f'{col.title()} Over Time', fontsize=12, fontweight='bold')
            axes[idx].set_xlabel('Date')
            axes[idx].set_ylabel(col.title())
            axes[idx].grid(True, alpha=0.3)
            axes[idx].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def find_extreme_days(self):
        """Find days with extreme weather conditions"""
        if self.df is None:
            print("No data loaded!")
            return
        
        print("\n" + "="*60)
        print("EXTREME WEATHER DAYS")
        print("="*60)
        
        if 'temperature' in self.df.columns:
            hottest = self.df.loc[self.df['temperature'].idxmax()]
            coldest = self.df.loc[self.df['temperature'].idxmin()]
            print(f"\nHottest Day: {hottest['date']} - {hottest['temperature']:.2f}°C")
            print(f"Coldest Day: {coldest['date']} - {coldest['temperature']:.2f}°C")
        
        if 'precipitation' in self.df.columns:
            wettest = self.df.loc[self.df['precipitation'].idxmax()]
            print(f"\nWettest Day: {wettest['date']} - {wettest['precipitation']:.2f}mm")
        
        if 'wind_speed' in self.df.columns:
            windiest = self.df.loc[self.df['wind_speed'].idxmax()]
            print(f"\nWindiest Day: {windiest['date']} - {windiest['wind_speed']:.2f} km/h")
    
    def fetch_real_data(self, city="Nagpur", days=None):
        """Fetch real weather data for an Indian city using Meteostat

        Args:
            city (str): Name of the city.
            days (int, optional): Number of past days to fetch. Defaults to 30 if None.
        """
        city_coords = {
            "Nagpur": (21.1458, 79.0882),
            "New Delhi": (28.6139, 77.2090),
            "Mumbai": (19.0760, 72.8777),
            "Chennai": (13.0827, 80.2707),
            "Bengaluru": (12.9716, 77.5946),
            "Kolkata": (22.5726, 88.3639),
            "Hyderabad": (17.3850, 78.4867)
        }

        if city not in city_coords:
            raise ValueError(f"City '{city}' not supported! Available: {list(city_coords.keys())}")
        
        lat, lon = city_coords[city]
        location = Point(lat, lon)
        end = datetime.now()
        
        if days is None:
            days = 30  # Default to 1 month
        
        start = end - timedelta(days=days)
        
        data = Daily(location, start, end)
        df = data.fetch().reset_index()
        print(f"Fetched data columns: {list(df.columns)}")

        df = df.rename(columns={
            'time': 'date',
            'tavg': 'temperature',
            'prcp': 'precipitation',
            'wspd': 'wind_speed',
            'pres': 'pressure'
        })[['date', 'temperature', 'precipitation', 'wind_speed', 'pressure']].dropna()

        self.df = df
        print(f"✅ Loaded {len(df)} days of data for {city} (last {days} days)")
        return df
