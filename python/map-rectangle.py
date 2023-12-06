import json
from geopy.distance import great_circle, distance

def calculate_bounds(center, west_km, east_km, north_km, south_km):
    # Calcular os pontos de limite
    west = distance(kilometers=west_km).destination(center, bearing=270)  # Oeste
    east = distance(kilometers=east_km).destination(center, bearing=90)   # Leste
    north = distance(kilometers=north_km).destination(center, bearing=0)   # Norte
    south = distance(kilometers=south_km).destination(center, bearing=180) # Sul

    # Retorna latitude e longitude dos limites (lat_norte, lat_sul, lon_oeste, lon_leste)
    return (north.latitude, south.latitude, west.longitude, east.longitude)

def is_within_bounds(feature, bounds):
    # Obter as coordenadas da 'feature'
    feature_coords = feature['geometry']['coordinates'][0][0]
    feature_coords = tuple(reversed(feature_coords))

    lat, lon = feature_coords
    north_lat, south_lat, west_lon, east_lon = bounds

    # Verificar se a feature está dentro dos limites do retângulo
    return south_lat <= lat <= north_lat and west_lon <= lon <= east_lon

# Coordenadas de Campinas e dimensões do retângulo
json_name = 'geojs-35-mun.json'
new_file_name = 'geojs-35-[200-70-70-70]km-Campinas-mun.json'
campinas_coords = (-22.9103015,-47.0595007)
bounds = calculate_bounds(campinas_coords, 200, 70, 70, 70)

# Ler o arquivo GeoJSON
with open(json_name, 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)

# Filtrar as 'features'
filtered_features = [feature for feature in geojson_data['features'] if is_within_bounds(feature, bounds)]

# Criar e salvar o novo GeoJSON
filtered_geojson = {'type': 'FeatureCollection', 'features': filtered_features}
with open(new_file_name, 'w', encoding='utf-8') as file:
    json.dump(filtered_geojson, file, ensure_ascii=False, indent=4)
