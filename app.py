import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from weather import WeatherDataAnalyzer
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Weather Data Analyzer",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #667eea;
        text-align: center;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = WeatherDataAnalyzer()
    st.session_state.data_loaded = False

# Title
st.title("🌤️ Weather Data Analyzer")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Data Source")
    
    data_option = st.radio(
        "Choose data source:",
        ["Upload CSV File", "Get Data"]
    )
    
    if data_option == "Upload CSV File":
        uploaded_file = st.file_uploader("Upload your weather CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                st.session_state.analyzer.df = pd.read_csv(uploaded_file)
                st.session_state.analyzer.df['date'] = pd.to_datetime(
                    st.session_state.analyzer.df['date']
                )
                st.session_state.data_loaded = True
                st.success(f"✅ File loaded! {len(st.session_state.analyzer.df)} rows")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    else:
        days = st.slider("Number of days", min_value=30, max_value=365, value=365)
        city = st.selectbox("Select a city:", ["Nagpur", "New Delhi", "Mumbai", "Chennai", "Bengaluru", "Kolkata", "Hyderabad"])

        if st.button("Get Data", type="primary"):
            st.session_state.analyzer.fetch_real_data(city=city, days=days)
            st.session_state.data_loaded = True
            st.success(f"✅ Data fetched for {days} days in {city}!")

    
    st.markdown("---")
    
    if st.session_state.data_loaded:
        st.header("📋 Quick Info")
        st.metric("Total Records", len(st.session_state.analyzer.df))
        st.metric("Columns", len(st.session_state.analyzer.df.columns))
        
        if 'date' in st.session_state.analyzer.df.columns:
            date_range = st.session_state.analyzer.df['date']
            st.metric(
                "Date Range", 
                f"{date_range.min().date()} to {date_range.max().date()}"
            )

# Main content
if not st.session_state.data_loaded:
    st.info("👈 Please upload a CSV file or generate sample data from the sidebar to begin analysis")
    
    # Show sample CSV format
    st.subheader("Expected CSV Format:")
    sample_df = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'temperature': [25.5, 26.3, 24.8],
        'precipitation': [0, 2.5, 1.2],
        'wind_speed': [15, 18, 12],
        'pressure': [1013, 1015, 1012]
    })
    st.dataframe(sample_df, use_container_width=True)

else:
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Statistics", 
        "📈 Visualizations", 
        "🌡️ Extremes", 
        "📋 Data View",
        "🔍 Insights"
    ])
    
    # Tab 1: Statistics
    with tab1:
        st.header("Summary Statistics")
        
        numeric_cols = st.session_state.analyzer.df.select_dtypes(include=[np.number]).columns
        
        # Display statistics for each numeric column
        for col in numeric_cols:
            with st.expander(f"📊 {col.upper()}", expanded=True):
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Mean", f"{st.session_state.analyzer.df[col].mean():.2f}")
                with col2:
                    st.metric("Median", f"{st.session_state.analyzer.df[col].median():.2f}")
                with col3:
                    st.metric("Std Dev", f"{st.session_state.analyzer.df[col].std():.2f}")
                with col4:
                    st.metric("Min", f"{st.session_state.analyzer.df[col].min():.2f}")
                with col5:
                    st.metric("Max", f"{st.session_state.analyzer.df[col].max():.2f}")
    
    # Tab 2: Visualizations
    with tab2:
        st.header("Data Visualizations")
        
        viz_option = st.selectbox(
            "Choose visualization:",
            [
                "Temperature Trend",
                "Monthly Averages",
                "Correlation Heatmap",
                "All Variables",
                "Distribution Plots"
            ]
        )
        
        if viz_option == "Temperature Trend":
            if 'temperature' in st.session_state.analyzer.df.columns:
                st.subheader("🌡️ Temperature Trend Over Time")
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(
                    st.session_state.analyzer.df['date'], 
                    st.session_state.analyzer.df['temperature'], 
                    linewidth=1.5, 
                    color='#e74c3c'
                )
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('Temperature (°C)', fontsize=12)
                ax.set_title('Temperature Trend Over Time', fontsize=16, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("Temperature column not found in data")
        
        elif viz_option == "Monthly Averages":
            if 'temperature' in st.session_state.analyzer.df.columns:
                st.subheader("📅 Monthly Average Temperature")
                
                df_copy = st.session_state.analyzer.df.copy()
                df_copy['month'] = pd.to_datetime(df_copy['date']).dt.month
                monthly_avg = df_copy.groupby('month')['temperature'].mean()
                
                # Sort months in ascending order
                monthly_avg = monthly_avg.sort_index()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                months_present = monthly_avg.index.tolist()
                month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                labels_to_show = [month_labels[m-1] for m in months_present]
                
                ax.bar(months_present, monthly_avg, color='skyblue', edgecolor='navy', alpha=0.7)
                ax.set_xlabel('Month', fontsize=12)
                ax.set_ylabel('Average Temperature (°C)', fontsize=12)
                ax.set_title('Monthly Average Temperature', fontsize=16, fontweight='bold')
                ax.set_xticks(months_present)
                ax.set_xticklabels(labels_to_show)
                ax.grid(axis='y', alpha=0.3)
                
                # Add value labels on top of bars
                for m, val in zip(months_present, monthly_avg):
                    ax.text(m, val + 0.1, f"{val:.1f}", ha='center', va='bottom', fontsize=10)
                
                st.pyplot(fig)
            else:
                st.warning("Temperature column not found in data")

        elif viz_option == "Correlation Heatmap":
            st.subheader("🔥 Correlation Heatmap")
            numeric_df = st.session_state.analyzer.df.select_dtypes(include=[np.number])
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(
                numeric_df.corr(), 
                annot=True, 
                fmt='.2f', 
                cmap='coolwarm', 
                center=0, 
                square=True,
                linewidths=1, 
                cbar_kws={"shrink": 0.8},
                ax=ax
            )
            ax.set_title('Weather Variables Correlation Heatmap', fontsize=16, fontweight='bold')
            st.pyplot(fig)
        
        elif viz_option == "All Variables":
            st.subheader("📊 All Weather Variables")

            df = st.session_state.analyzer.df.copy()
            
            # Ensure 'date' is datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            else:
                st.warning("Date column not found in data.")
                st.stop()
            
            # Select numeric columns safely
            from pandas.api.types import is_numeric_dtype
            numeric_cols = [col for col in df.columns if col != 'date' and is_numeric_dtype(df[col])]
            
            if not numeric_cols:
                st.warning("No numeric columns found to plot.")
            else:
                n_cols = len(numeric_cols)
                fig, axes = plt.subplots(n_cols, 1, figsize=(12, 4*n_cols))
                
                if n_cols == 1:
                    axes = [axes]
                
                for idx, col in enumerate(numeric_cols):
                    axes[idx].plot(df['date'], df[col], linewidth=1, color='royalblue')
                    axes[idx].set_title(f'{col.title()} Over Time', fontsize=12, fontweight='bold')
                    axes[idx].set_xlabel('Date', fontsize=10)
                    axes[idx].set_ylabel(col.title(), fontsize=10)
                    axes[idx].grid(True, alpha=0.3)
                    axes[idx].tick_params(axis='x', rotation=45)
                    
                    if len(df) <= 60:  # small datasets
                        for x, y in zip(df['date'], df[col]):
                            axes[idx].text(x, y, f"{y:.1f}", fontsize=8, rotation=45)
                
                plt.tight_layout()
                st.pyplot(fig)



        elif viz_option == "Distribution Plots":
            st.subheader("📊 Distribution of Weather Variables")
            numeric_cols = st.session_state.analyzer.df.select_dtypes(include=[np.number]).columns
            
            selected_var = st.selectbox("Select variable:", numeric_cols)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.hist(
                    st.session_state.analyzer.df[selected_var], 
                    bins=30, 
                    color='skyblue', 
                    edgecolor='navy',
                    alpha=0.7
                )
                ax.set_xlabel(selected_var.title())
                ax.set_ylabel('Frequency')
                ax.set_title(f'Distribution of {selected_var.title()}')
                ax.grid(axis='y', alpha=0.3)
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.boxplot(st.session_state.analyzer.df[selected_var])
                ax.set_ylabel(selected_var.title())
                ax.set_title(f'Box Plot of {selected_var.title()}')
                ax.grid(axis='y', alpha=0.3)
                st.pyplot(fig)
    
    # Tab 3: Extremes
    with tab3:
        st.header("🌡️ Extreme Weather Days")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'temperature' in st.session_state.analyzer.df.columns:
                st.subheader("🔥 Temperature Extremes")
                hottest = st.session_state.analyzer.df.loc[
                    st.session_state.analyzer.df['temperature'].idxmax()
                ]
                coldest = st.session_state.analyzer.df.loc[
                    st.session_state.analyzer.df['temperature'].idxmin()
                ]
                
                st.markdown(f"""
                <div class="stat-card">
                    <h3>Hottest Day</h3>
                    <p><strong>Date:</strong> {hottest['date']}</p>
                    <p><strong>Temperature:</strong> {hottest['temperature']:.2f}°C</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="stat-card">
                    <h3>Coldest Day</h3>
                    <p><strong>Date:</strong> {coldest['date']}</p>
                    <p><strong>Temperature:</strong> {coldest['temperature']:.2f}°C</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if 'precipitation' in st.session_state.analyzer.df.columns:
                st.subheader("💧 Precipitation Extremes")
                wettest = st.session_state.analyzer.df.loc[
                    st.session_state.analyzer.df['precipitation'].idxmax()
                ]
                
                st.markdown(f"""
                <div class="stat-card">
                    <h3>Wettest Day</h3>
                    <p><strong>Date:</strong> {wettest['date']}</p>
                    <p><strong>Precipitation:</strong> {wettest['precipitation']:.2f} mm</p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'wind_speed' in st.session_state.analyzer.df.columns:
                windiest = st.session_state.analyzer.df.loc[
                    st.session_state.analyzer.df['wind_speed'].idxmax()
                ]
                
                st.markdown(f"""
                <div class="stat-card">
                    <h3>Windiest Day</h3>
                    <p><strong>Date:</strong> {windiest['date']}</p>
                    <p><strong>Wind Speed:</strong> {windiest['wind_speed']:.2f} km/h</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 4: Data View
    with tab4:
        st.header("📋 Raw Data View")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            num_rows = st.slider("Number of rows to display", 5, 100, 10)
        with col2:
            sort_by = st.selectbox("Sort by", st.session_state.analyzer.df.columns)
        
        st.dataframe(
            st.session_state.analyzer.df.sort_values(by=sort_by, ascending=False).head(num_rows),
            use_container_width=True
        )
        
        # Download button
        csv = st.session_state.analyzer.df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"weather_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Tab 5: Insights
    with tab5:
        st.header("🔍 Quick Insights")
        
        if 'temperature' in st.session_state.analyzer.df.columns:
            avg_temp = st.session_state.analyzer.df['temperature'].mean()
            temp_trend = "warming" if st.session_state.analyzer.df['temperature'].iloc[-30:].mean() > avg_temp else "cooling"
            
            st.info(f"📊 The average temperature is **{avg_temp:.2f}°C** and the recent trend shows {temp_trend}.")
        
        # if 'precipitation' in st.session_state.analyzer.df.columns:
        #     rainy_days = len(st.session_state.analyzer.df[st.session_state.analyzer.df['precipitation'] > 0])
        #     rainy_percentage = (rainy_days / len(st.session_state.analyzer.df)) * 100
            
        #     st.info(f"💧 There were **{rainy_days}** rainy days (**{rainy_percentage:.1f}%** of total days).")
        
        
        # Seasonal analysis
        if 'date' in st.session_state.analyzer.df.columns and 'temperature' in st.session_state.analyzer.df.columns:
            st.subheader("🍂 Seasonal Temperature Analysis")
            
            df_seasonal = st.session_state.analyzer.df.copy()
            df_seasonal['month'] = pd.to_datetime(df_seasonal['date']).dt.month
            df_seasonal['season'] = df_seasonal['month'].apply(
                lambda x: 'Winter' if x in [12, 1, 2] else
                         'Spring' if x in [3, 4, 5] else
                         'Summer' if x in [6, 7, 8] else 'Fall'
            )
            
            seasonal_avg = df_seasonal.groupby('season')['temperature'].mean().sort_values(ascending=False)
            
            col1, col2, col3, col4 = st.columns(4)
            
            for idx, (season, temp) in enumerate(seasonal_avg.items()):
                with [col1, col2, col3, col4][idx]:
                    st.metric(season, f"{temp:.1f}°C")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Weather Data Analyzer | Built with Streamlit 🌤️</p>",
    unsafe_allow_html=True
)