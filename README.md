# Weather Data Analyzer 🌤️

A comprehensive weather data analysis dashboard built with Python Dash that allows users to visualize, analyze, and explore weather patterns through an interactive web interface.

## Features

### 📊 Data Sources
- **Upload CSV**: Import your own weather data in CSV format
- **Fetch Real Data**: Retrieve actual weather data for major Indian cities using the Meteostat API

### 📈 Analysis Capabilities
1. **Statistics Tab**: View comprehensive summary statistics (mean, median, std dev, min, max) for all weather variables
2. **Visualizations Tab**: 
   - Temperature trends over time
   - Monthly average temperatures
   - Multi-variable comparison plots
   - Distribution plots with histograms and box plots
3. **Extremes Tab**: Identify extreme weather days (hottest, coldest, wettest, windiest)
4. **Data View Tab**: Browse raw data in a paginated table with download capability
5. **Insights Tab**: Get automated insights including seasonal analysis and temperature trends

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
- dash - Web application framework
- plotly - Interactive visualizations
- pandas - Data manipulation
- numpy - Numerical operations
- matplotlib - Static plotting
- seaborn - Statistical visualizations
- meteostat - Real weather data API

## Usage

### Starting the Application

Run the main application:
```bash
python app.py
```

The dashboard will be available at `http://localhost:8050` in your web browser.

### Using Your Own Data

#### CSV Format
Your CSV file should contain the following columns:
- `date`: Date in YYYY-MM-DD format
- `temperature`: Temperature in °C
- `precipitation`: Precipitation in mm
- `wind_speed`: Wind speed in km/h
- `pressure`: Atmospheric pressure in hPa

Example CSV:
```csv
date,temperature,precipitation,wind_speed,pressure
2024-01-01,25.5,0,15,1013
2024-01-02,26.3,2.5,18,1015
2024-01-03,24.8,1.2,12,1012
```

### Fetching Real Data

The app supports fetching real weather data for these Indian cities:
- Nagpur
- New Delhi
- Mumbai
- Chennai
- Bengaluru
- Kolkata
- Hyderabad

Simply select "Get Real Data" option, choose a city and time period (30-365 days), then click "Get Data".

## File Structure

```
weather-analyzer/
│
├── app.py              # Main Dash application with UI and callbacks
├── weather.py          # Weather data analysis class and utilities
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Core Components

### `app.py`
The main application file containing:
- Dashboard layout and UI components
- Interactive callbacks for data loading and visualization
- Tab-based navigation system
- Real-time data updates

### `weather.py`
The `WeatherDataAnalyzer` class provides:
- Data loading and validation
- Statistical analysis methods
- Data fetching from Meteostat API
- Sample data generation for testing

## Key Features Explained

### Interactive Visualizations
- **Line Charts**: Track temperature and other variables over time
- **Bar Charts**: Compare monthly averages
- **Histograms**: View data distributions
- **Box Plots**: Identify outliers and quartiles

### Smart Insights
- Automatic trend detection (warming/cooling)
- Seasonal temperature analysis
- Extreme weather event identification

### Data Export
Download analyzed data as CSV for further processing or reporting.

## API Reference

### WeatherDataAnalyzer Class

```python
from weather import WeatherDataAnalyzer

# Initialize analyzer
analyzer = WeatherDataAnalyzer()

# Fetch real data
analyzer.fetch_real_data(city="Nagpur", days=365)

# Create sample data
analyzer.create_sample_data(days=365)

# Get summary statistics
analyzer.summary_statistics()

# Find extreme weather days
analyzer.find_extreme_days()
```

### Main Methods

#### `fetch_real_data(city="Nagpur", days=30)`
Fetches real weather data from Meteostat API.
- **Parameters:**
  - `city` (str): City name from supported list
  - `days` (int): Number of past days to fetch (default: 30)
- **Returns:** pandas DataFrame with weather data

#### `create_sample_data(days=365)`
Generates synthetic weather data for testing.
- **Parameters:**
  - `days` (int): Number of days to generate
- **Returns:** pandas DataFrame with sample data

#### `summary_statistics()`
Prints summary statistics for all numeric columns.

#### `find_extreme_days()`
Identifies and prints extreme weather events.

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in app.py, last line:
app.run(host='0.0.0.0', port=8051)  # Change 8050 to 8051
```

**Meteostat data not loading:**
- Check internet connection
- Verify city name spelling
- Try reducing the number of days requested
- Meteostat may have rate limits or data availability issues

**CSV upload fails:**
- Ensure CSV has required columns: `date`, `temperature`, `precipitation`, `wind_speed`, `pressure`
- Check date format is YYYY-MM-DD
- Verify numeric values are not text
- Ensure file encoding is UTF-8

**Module not found errors:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

## Advanced Usage

### Customizing the Dashboard

You can modify `app.py` to:
- Add new visualization types
- Change color schemes (modify hex colors in style dictionaries)
- Add new analysis tabs
- Customize data processing logic

### Adding New Cities

In `weather.py`, add coordinates to the `city_coords` dictionary:
```python
city_coords = {
    "Your City": (latitude, longitude),
    # ... existing cities
}
```

### Extending Analysis

Add custom analysis methods to the `WeatherDataAnalyzer` class:
```python
def custom_analysis(self):
    # Your analysis code here
    pass
```

## Performance Tips

- For large datasets (>10,000 rows), consider:
  - Using data sampling for visualizations
  - Implementing pagination in data views
  - Caching processed results

## Contributing

Contributions are welcome! Areas for improvement:
- Additional visualization types
- More statistical analyses
- Support for additional cities/countries
- Enhanced UI features
- Machine learning predictions
- Export to different formats (Excel, JSON)

## Known Limitations

- Meteostat data availability varies by location and time period
- Large CSV files (>100MB) may cause performance issues
- Real-time data updates are not supported
- Limited to daily weather data (no hourly data)

## Future Enhancements

- [ ] Weather forecasting using ML models
- [ ] Comparison between multiple cities
- [ ] Export visualizations as images
- [ ] Mobile-responsive design improvements
- [ ] User authentication and saved sessions
- [ ] API endpoint for programmatic access

## License

This project is open source and available for educational and personal use.

## Acknowledgments

- Weather data provided by [Meteostat](https://meteostat.net/)
- Built with [Dash by Plotly](https://dash.plotly.com/)
- Icons from Unicode emoji set

## Support

For issues, questions, or suggestions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the code comments in `app.py` and `weather.py`
- Consult the [Dash documentation](https://dash.plotly.com/)

---

**Built with ❤️ using Dash 🌤️**

*Last updated: November 2024*