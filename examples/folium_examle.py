from flask import Flask
import folium

app = Flask(__name__)


@app.route('/')
def index():
    start_coords = (49.817545, 24.023932)
    folium_map = folium.Map(location=start_coords, zoom_start=17)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run("0.0.0.0", port=80, debug=False)
