import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import folium
from streamlit_folium import folium_static
import re
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

class GarageSearchEngine:
    def __init__(self, csv_path: str):
        """Initialize the search engine with data preparation"""
        self.df = pd.read_csv(csv_path)
        self.prepare_data()
        
    def prepare_data(self):
        """Prepare data for searching"""
        # Create combined text field
        self.df['search_text'] = self.df.apply(
            lambda x: f"{x['Garage Name']} {x['Location']} {x['City']} {x['Postcode']}", 
            axis=1
        ).str.lower()
        
        # Initialize TF-IDF
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['search_text'])
        
        # Extract postcode areas
        self.df['postcode_area'] = self.df['Postcode'].str.extract(
            r'([A-Z]{1,2}\d{1,2})', 
            flags=re.IGNORECASE
        )

    def search(self, query: str, search_type: str, threshold: float = 0.1):
        """Unified search method"""
        if search_type == 'name':
            return self._search_by_name(query, threshold)
        elif search_type == 'location':
            return self._search_by_location(query)
        elif search_type == 'nearby':
            return self._search_nearby(query)
        else:
            return self._comprehensive_search(query)

    def _search_by_name(self, name: str, threshold: float):
        """Search by garage name"""
        query_vector = self.tfidf.transform([name.lower()])
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        results_df = self.df.copy()
        results_df['similarity_score'] = similarity_scores
        
        return results_df[
            (results_df['similarity_score'] >= threshold) |
            (results_df['Garage Name'].str.lower().str.contains(name.lower(), na=False))
        ].sort_values('similarity_score', ascending=False)

    def _search_by_location(self, location: str):
        """Search by location"""
        query_vector = self.tfidf.transform([location.lower()])
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        results_df = self.df.copy()
        results_df['similarity_score'] = similarity_scores
        return results_df[results_df['similarity_score'] >= 0.1].sort_values('similarity_score', ascending=False)

    def _search_nearby(self, postcode: str):
        """Find nearby garages"""
        area_match = re.search(r'([A-Z]{1,2}\d{1,2})', postcode.upper())
        if not area_match:
            return pd.DataFrame()
            
        area_prefix = area_match.group(1)[:2]
        return self.df[self.df['Postcode'].str.contains(f"^{area_prefix}", case=False, na=False)]

    def _comprehensive_search(self, query: str):
        """Search across all fields"""
        name_results = self._search_by_name(query, 0.1)
        location_results = self._search_by_location(query)
        nearby_results = self._search_nearby(query)
        
        all_results = pd.concat([name_results, location_results, nearby_results])
        return all_results.drop_duplicates(subset=['Garage Name', 'Postcode'])

def get_coordinates(address):
    """Get coordinates for an address using Nominatim"""
    try:
        geolocator = Nominatim(user_agent="garage_search")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        return None

def create_map(df, center_lat=51.5074, center_lon=-0.1278):
    """Create a folium map with garage markers"""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    
    for idx, row in df.iterrows():
        address = f"{row['Location']}, {row['City']}, {row['Postcode']}, UK"
        coords = get_coordinates(address)
        if coords:
            folium.Marker(
                coords,
                popup=f"""
                <b>{row['Garage Name']}</b><br>
                {row['Location']}<br>
                {row['City']}, {row['Postcode']}<br>
                Phone: {row['Phone']}<br>
                Email: {row['Email']}
                """,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
    return m

def main():
    st.set_page_config(page_title="UK Garage Finder", layout="wide")
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .garage-card {
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🚗 UK Garage Finder")
    st.markdown("---")
    
    # Initialize search engine
    try:
        search_engine = GarageSearchEngine('Garage in UK  Sheet1.csv')
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("Search Options")
        search_type = st.selectbox(
            "Search Type",
            ["Comprehensive", "By Name", "By Location", "Find Nearby"],
            key="search_type"
        )
        
        search_query = st.text_input(
            "Search Query",
            placeholder="Enter garage name, location, or postcode..."
        )
        
        if search_type == "By Name":
            threshold = st.slider(
                "Similarity Threshold",
                0.0, 1.0, 0.1, 0.05,
                help="Adjust how closely results should match your search"
            )
        
        search_button = st.button("🔍 Search")
        
        st.markdown("---")
        st.markdown("### Tips")
        st.markdown("""
        - For name search: Enter full or partial garage name
        - For location: Enter city, area, or postcode
        - For nearby: Enter a postcode to find garages in the area
        """)
    
    # Main content
    if search_button and search_query:
        with st.spinner("Searching..."):
            # Convert search type to backend format
            search_type_map = {
                "Comprehensive": "all",
                "By Name": "name",
                "By Location": "location",
                "Find Nearby": "nearby"
            }
            
            # Perform search
            results = search_engine.search(
                search_query,
                search_type_map[search_type],
                threshold if search_type == "By Name" else 0.1
            )
            
            if len(results) > 0:
                # Create two columns
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f"Found {len(results)} matching garages")
                    
                    # Display results in cards
                    for _, garage in results.iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div class="garage-card">
                                <h3>{garage['Garage Name']}</h3>
                                <p>📍 {garage['Location']}, {garage['City']}, {garage['Postcode']}</p>
                                <p>📞 {garage['Phone']}</p>
                                <p>📧 {garage['Email']}</p>
                                {"<p>🌐 " + f"<a href='{garage['Website']}' target='_blank'>{garage['Website']}</a></p>" if garage['Website'] != 'No Website' else ""}
                            </div>
                            """, unsafe_allow_html=True)
                
                with col2:
                    st.subheader("📍 Map View")
                    # Create and display map
                    if len(results) > 0:
                        sample_address = f"{results.iloc[0]['City']}, UK"
                        coords = get_coordinates(sample_address)
                        if coords:
                            m = create_map(results[:10], coords[0], coords[1])
                            folium_static(m)
                
                # Analytics
                st.markdown("---")
                st.subheader("📊 Analytics")
                
                # City distribution
                city_dist = results['City'].value_counts()
                fig = px.pie(
                    values=city_dist.values,
                    names=city_dist.index,
                    title="Distribution by City"
                )
                st.plotly_chart(fig)
                
            else:
                st.warning("No garages found matching your search criteria.")

if __name__ == "__main__":
    main()
