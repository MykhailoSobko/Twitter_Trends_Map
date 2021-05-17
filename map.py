import werkzeug.wsgi
from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter
import folium


def get_coordinates():
    avaliable_countries = ['United Arab Emirates', 'Algeria', 'Argentina', 'Australia', 'Austria', 'Bahrain', 'Belgium',
                           'Belarus', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Denmark', 'Dominican Republic',
                           'Ecuador',
                           'Egypt', 'Ireland', 'France', 'Ghana', 'Germany', 'Greece', 'Guatemala', 'Indonesia',
                           'India',
                           'Israel', 'Italy', 'Japan', 'Jordan', 'Kenya', 'Korea', 'Kuwait', 'Lebanon', 'Latvia',
                           'Oman',
                           'Mexico', 'Malaysia', 'Nigeria', 'Netherlands', 'Norway', 'New Zealand', 'Peru', 'Pakistan',
                           'Poland', 'Panama', 'Portugal', 'Qatar', 'Philippines', 'Puerto Rico', 'Russia',
                           'Saudi Arabia',
                           'South Africa', 'Singapore', 'Spain', 'Sweden', 'Switzerland', 'Thailand', 'Turkey',
                           'United Kingdom',
                           'Ukraine', 'United States', 'Venezuela', 'Vietnam']

    coordinates = []
    for country in avaliable_countries:
        geolocator = Nominatim(user_agent="location_find")
        # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=1)
        location = geolocator.geocode(country)
        coordinates.append([country, (location.latitude, location.longitude)])
    return coordinates


def create_map():
    countries = get_coordinates()
    countries_map = folium.Map()

    for country in countries:
        location = country[1]
        html = f"""
            <a href='http://127.0.0.1:5000/trendslist/{country[0]}' name='{country[0]}'>{country[0]}</a>
            """
        iframe = folium.Html(html, script=True)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=location, popup=popup).add_to(countries_map)
    return countries_map.save("choose_country.html")


create_map()
