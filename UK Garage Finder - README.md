# UK Garage Finder 🚗

A sophisticated search application built with Streamlit for finding garages across the UK. The system uses advanced text similarity matching and provides an interactive interface with mapping capabilities.

## Features 🌟

- **Multiple Search Options**
  - Comprehensive search across all fields
  - Search by garage name
  - Search by location/address
  - Find nearby garages using postcode
  - Adjustable similarity threshold for precise matching

- **Interactive Map View**
  - Visual representation of garage locations
  - Interactive markers with garage details
  - Automatic centering based on search results

- **Analytics Dashboard**
  - Distribution of garages by city
  - Interactive charts and visualizations
  - Search result analytics

- **User-Friendly Interface**
  - Clean, modern design
  - Responsive layout
  - Easy-to-use search filters
  - Detailed garage information cards

## Installation Requirements 🔧

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Required Packages
```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
streamlit==1.24.0
pandas==1.5.3
numpy==1.24.3
scikit-learn==1.2.2
folium==0.14.0
streamlit-folium==0.11.0
geopy==2.3.0
plotly==5.13.1
```

## Project Structure 📁

```
uk-garage-finder/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Package dependencies
├── data/
│   └── Garage in UK  Sheet1.csv    # Garage database
├── src/
│   ├── search_engine.py   # Search functionality
│   └── utils.py           # Utility functions
└── README.md              # Project documentation
```

## Setup Instructions 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/uk-garage-finder.git
cd uk-garage-finder
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage Guide 📖

1. **Starting the Application**
   - Run the application using `streamlit run app.py`
   - The web interface will open automatically in your default browser

2. **Search Options**
   - Select search type from the sidebar
   - Enter search query (garage name, location, or postcode)
   - Adjust similarity threshold if needed
   - Click the search button

3. **Viewing Results**
   - Results are displayed as cards with garage details
   - Interactive map shows garage locations
   - Analytics section shows distribution of results

## Features in Detail 🔍

### Search Engine
- TF-IDF vectorization for text matching
- Cosine similarity for relevance ranking
- Postcode area matching for nearby searches
- Comprehensive search combining multiple methods

### User Interface
- Sidebar for search options
- Main content area with results
- Interactive map view
- Analytics visualizations

### Data Visualization
- Folium maps for location display
- Plotly charts for analytics
- Interactive markers and popups

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## System Requirements 💻

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Python**: Version 3.8 or higher
- **Browser**: Modern web browser (Chrome, Firefox, Safari)

## Performance Notes 📊

- Initial load time may vary based on data size
- Map rendering depends on internet connection
- Geocoding requests are rate-limited
- Search performance scales with database size

## Future Enhancements 🚀

- [ ] Advanced filtering options
- [ ] User reviews and ratings
- [ ] Appointment booking system
- [ ] Service type categorization
- [ ] Mobile app version
- [ ] API integration
- [ ] Real-time availability
- [ ] Service price comparison

## License 📝

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments 🙏

- Streamlit team for the amazing framework
- OpenStreetMap for map data
- All contributors and testers

## Contact 📧

Your Name - [@yourusername](https://twitter.com/yourusername)
Project Link: [https://github.com/yourusername/uk-garage-finder](https://github.com/yourusername/uk-garage-finder)
