from flask import Flask, render_template
from flask import request
import requests
import json
from geopy.geocoders import Nominatim

# inisialisasi flask App
App = Flask(__name__, template_folder='Web')

# connect to an API
url_volcano = "https://indonesia-public-static-api.vercel.app/api/volcanoes"
response_API = requests.get(url_volcano)

# parse data into JSON format 
data = response_API.text
parse_json = json.loads(data)

# DATA VOLCANO NI BOS SENGGOL DONG

# {
#     "nama":"Weh",
#     "bentuk":"stratovulkan",
#     "tinggi_meter":"617 meter",
#     "estimasi_letusan_terakhir":"Pleistosen",
#     "geolokasi":"5.82°N 95.28°E"
# }

# Make an variable from data in parse_json
nama_gunung = list(map(lambda x: x['nama'], parse_json))
bentuk_gunung = list(map(lambda x: x['bentuk'], parse_json))
tinggi_gunung = list(map(lambda x: x['tinggi_meter'], parse_json))
estimasi_letusan_gunung = list(map(lambda x: x['estimasi_letusan_terakhir'], parse_json))
geolokasi_gunung = list(map(lambda x: x['geolokasi'], parse_json))

# for i,gunung in enumerate(parse_json):
#     print(f"Gunung {i+1}: {gunung['nama']}")
#     # 150 gunung pada parse_json

# Geolocator translate 
geolocator = Nominatim(user_agent='geoapiGunung')

# dataGunung tampil di home
dataGunung = []
for i in range(10):
    gunung = dict()
    gunung['nama'] = nama_gunung[i]
    location = geolocator.geocode(geolokasi_gunung[i])
    gunung['geolokasi.latitude'] = location.latitude
    gunung['geolokasi.longitude'] = location.longitude
    dataGunung.append(gunung)

# print(dataGunung)

# Detail data gunung pada masing-masing gunung (linked)
detailGunung = []
# gmaps = googlemaps.Client(key='AIzaSyDTRNCCEFPzk2u9nz-ZJiml1s7zDw-jQms')

for i in range(10):
    gunung = dict()
    gunung['nama'] = nama_gunung[i]
    gunung['bentuk'] = bentuk_gunung[i]
    gunung['tinggi'] = tinggi_gunung[i]
    gunung['estimasi_letusan_terakhir'] = estimasi_letusan_gunung[i]
    location = geolocator.geocode(geolokasi_gunung[i])
    gunung['geolokasi.latitude'] = location.latitude
    gunung['geolokasi.longitude'] = location.longitude

    detailGunung.append(gunung)

# print(detailGunung)

@App.route('/')
def home():
    return render_template('index.html', volcano = dataGunung)

def get_volcano_data(volcano_list,name):
    return [v for v in volcano_list if v['nama'] == name]

@App.route('/detail-gunung')
def detail_gunung():
    nama = request.args.get('nama')
    # nama = detail_gunung[0]['nama']
    volcano_data = get_volcano_data(detailGunung, nama)
    print(volcano_data)
    return render_template('detailGunung.html', volcano = volcano_data)

@App.route('/about')
def about():
    dataKelompok = {
        'gambar':'https://drive.google.com/uc?export=view&id=1nGM0tvQ6BV3oyzPIFue2aiTZN3oBnSUk',
        'anggota':[
            {
                'nim': '21102056',
                'nama': 'Bintang Rizqi Pasha'
            },
            {
                'nim': '21102057',
                'nama': 'Sani Akhzam Prakistiyanto'
            },
            {
                'nim': '21102059',
                'nama': 'Farhan Aryo Pangestu'
            }
        ],
        'kelas': 'IF-09-M'
    }

    return render_template('about.html', data_kelompok = dataKelompok)

App.run(debug=True)
