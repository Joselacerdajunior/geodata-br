import json
from geopy.distance import great_circle

# Coordenadas de Campinas (latitude, longitude)
# campinas_coords = (-22.907104, -47.063240)
json_name = 'geojs-35-mun.json'
new_file_name = 'geojs-35-200km-Campinas-mun.json'
distance_km = 200
campinas_coords = (-22.9103015,-47.0595007)

def is_within_radius(feature, center, radius_km):
    # Supondo que a 'feature' é um ponto, obtenha suas coordenadas
    # Ajuste este código caso as 'features' sejam polígonos ou outras formas
    feature_coords = feature['geometry']['coordinates'][0][0]  # Ajuste conforme necessário
    feature_coords = tuple(reversed(feature_coords))  # Inverte para (latitude, longitude)

    # Calcula a distância
    distance = great_circle(center, feature_coords).kilometers
    return distance <= radius_km

# Ler o arquivo GeoJSON
with open(json_name, 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)

# Filtrar as 'features' que estão dentro do raio de 250 km
filtered_features = [feature for feature in geojson_data['features'] if is_within_radius(feature, campinas_coords, distance_km)]

# Criar um novo GeoJSON com as 'features' filtradas
filtered_geojson = {
    'type': 'FeatureCollection',
    'features': filtered_features
}

# Salvar o novo GeoJSON filtrado em um arquivo
with open(new_file_name, 'w', encoding='utf-8') as file:
    json.dump(filtered_geojson, file, ensure_ascii=False, indent=4)