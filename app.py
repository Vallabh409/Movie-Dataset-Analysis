import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="TMDB Movie Dataset Analysis",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 TMDB Movie Dataset Analysis")
st.markdown("""
    Explore and analyze The Movie Database (TMDB) dataset to discover insights about movies, 
    genres, budgets, revenues, and more!
""")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('tmdb-movies.csv')
        return df
    except FileNotFoundError:
        st.error("Data file 'tmdb-movies.csv' not found. Please ensure it's in the repository.")
        return None

df = load_data()

if df is not None:
    # Sidebar for filters
    st.sidebar.header("🏛️ Filters & Options")
    
    # Show raw data option
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("📊 Raw Dataset")
        st.dataframe(df.head(100))
    
    # Data overview
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Movies", len(df))
    with col2:
        if 'release_year' in df.columns:
            st.metric("Year Range", f"{int(df['release_year'].min())} - {int(df['release_year'].max())}")
    with col3:
        if 'revenue_adj' in df.columns:
            total_revenue = df['revenue_adj'].sum() / 1e9
            st.metric("Total Revenue", f"${total_revenue:.2f}B")
    with col4:
        if 'budget_adj' in df.columns:
            total_budget = df['budget_adj'].sum() / 1e9
            st.metric("Total Budget", f"${total_budget:.2f}B")
    
    # Data cleaning info
    with st.expander("🧹 Data Quality Information"):
        st.write("**Missing Values:**")
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Count': df.isnull().sum().values,
            'Missing Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        st.dataframe(missing_data[missing_data['Missing Count'] > 0])
    
    # Year-based analysis
    if 'release_year' in df.columns:
        st.subheader("📅 Movies Released Over Time")
        
        # Filter by year range
        year_range = st.slider(
            "Select Year Range",
            min_value=int(df['release_year'].min()),
            max_value=int(df['release_year'].max()),
            value=(int(df['release_year'].min()), int(df['release_year'].max()))
        )
        
        df_filtered = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]
        
        # Movies per year
        movies_per_year = df_filtered.groupby('release_year').size().reset_index(name='count')
        fig_year = px.line(
            movies_per_year,
            x='release_year',
            y='count',
            title='Number of Movies Released Per Year',
            labels={'release_year': 'Year', 'count': 'Number of Movies'}
        )
        st.plotly_chart(fig_year, use_container_width=True)
    
    # Budget and Revenue Analysis
    if 'budget_adj' in df.columns and 'revenue_adj' in df.columns:
        st.subheader("💰 Budget vs Revenue Analysis")
        
        # Filter out zero values for better visualization
        df_budget_revenue = df[(df['budget_adj'] > 0) & (df['revenue_adj'] > 0)].copy()
        
        if len(df_budget_revenue) > 0:
            # Calculate ROI
            df_budget_revenue['roi'] = ((df_budget_revenue['revenue_adj'] - df_budget_revenue['budget_adj']) / df_budget_revenue['budget_adj']) * 100
            
            # Scatter plot
            fig_scatter = px.scatter(
                df_budget_revenue.sample(min(1000, len(df_budget_revenue))),
                x='budget_adj',
                y='revenue_adj',
                hover_data=['original_title', 'release_year'],
                title='Budget vs Revenue (Sample of Movies)',
                labels={'budget_adj': 'Budget ($)', 'revenue_adj': 'Revenue ($)'},
                color='roi',
                color_continuous_scale='RdYlGn'
            )
            fig_scatter.add_trace(
                go.Scatter(
                    x=[0, df_budget_revenue['budget_adj'].max()],
                    y=[0, df_budget_revenue['budget_adj'].max()],
                    mode='lines',
                    name='Break-even line',
                    line=dict(dash='dash', color='red')
                )
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Top profitable movies
            st.subheader("🏆 Top 10 Most Profitable Movies")
            df_budget_revenue['profit'] = df_budget_revenue['revenue_adj'] - df_budget_revenue['budget_adj']
            top_profitable = df_budget_revenue.nlargest(10, 'profit')[['original_title', 'release_year', 'budget_adj', 'revenue_adj', 'profit', 'roi']]
            top_profitable['budget_adj'] = top_profitable['budget_adj'].apply(lambda x: f"${x/1e6:.2f}M")
            top_profitable['revenue_adj'] = top_profitable['revenue_adj'].apply(lambda x: f"${x/1e6:.2f}M")
            top_profitable['profit'] = top_profitable['profit'].apply(lambda x: f"${x/1e6:.2f}M")
            top_profitable['roi'] = top_profitable['roi'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(top_profitable, use_container_width=True)
    
    # Genre Analysis
    if 'genres' in df.columns:
        st.subheader("🎭 Genre Analysis")
        
        # Extract all genres
        all_genres = []
        for genres in df['genres'].dropna():
            all_genres.extend([g.strip() for g in str(genres).split('|')])
        
        genre_counts = pd.Series(all_genres).value_counts().head(15)
        
        fig_genres = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            title='Top 15 Most Common Genres',
            labels={'x': 'Number of Movies', 'y': 'Genre'}
        )
        st.plotly_chart(fig_genres, use_container_width=True)
    
    # Rating Analysis
    if 'vote_average' in df.columns:
        st.subheader("⭐ Rating Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            fig_rating = px.histogram(
                df[df['vote_average'] > 0],
                x='vote_average',
                nbins=30,
                title='Distribution of Movie Ratings',
                labels={'vote_average': 'Average Rating'}
            )
            st.plotly_chart(fig_rating, use_container_width=True)
        
        with col2:
            # Top rated movies
            if 'vote_count' in df.columns:
                # Filter movies with at least 100 votes for reliability
                df_top_rated = df[df['vote_count'] >= 100].nlargest(10, 'vote_average')[['original_title', 'release_year', 'vote_average', 'vote_count']]
                st.write("**Top 10 Highest Rated Movies (min 100 votes)**")
                st.dataframe(df_top_rated, use_container_width=True)
    
    # Runtime Analysis
    if 'runtime' in df.columns:
        st.subheader("⏱️ Runtime Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_runtime = df['runtime'].mean()
            st.metric("Average Runtime", f"{avg_runtime:.0f} minutes")
        
        with col2:
            # Runtime distribution
            fig_runtime = px.histogram(
                df[df['runtime'] > 0],
                x='runtime',
                nbins=40,
                title='Distribution of Movie Runtimes',
                labels={'runtime': 'Runtime (minutes)'}
            )
            st.plotly_chart(fig_runtime, use_container_width=True)
    
    # Search functionality
    st.subheader("🔍 Search Movies")
    search_term = st.text_input("Search for a movie:", "")
    
    if search_term:
        search_results = df[df['original_title'].str.contains(search_term, case=False, na=False)]
        if len(search_results) > 0:
            st.write(f"Found {len(search_results)} movies:")
            display_cols = [col for col in ['original_title', 'release_year', 'genres', 'runtime', 'vote_average', 'budget_adj', 'revenue_adj'] if col in df.columns]
            st.dataframe(search_results[display_cols].head(20), use_container_width=True)
        else:
            st.warning("No movies found matching your search.")
    
    # Download filtered data
    st.subheader("💾 Download Data")
    csv = df_filtered.to_csv(index=False) if 'df_filtered' in locals() else df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="tmdb_movies_filtered.csv",
        mime="text/csv"
    )

else:
    st.error("🚨 Unable to load data. Please ensure 'tmdb-movies.csv' exists in the repository.")

# Footer
st.markdown("---")
st.markdown("### 🚀 Ready to Deploy on Streamlit Cloud")
st.markdown("""
    **Deployment Instructions:**
    1. Ensure 'tmdb-movies.csv' is in the repository
    2. Create a `requirements.txt` with: streamlit, pandas, numpy, plotly
    3. Deploy directly from GitHub via Streamlit Cloud
""")
