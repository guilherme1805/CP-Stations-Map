from requests_html import HTMLSession
import json
import datetime

root_url = 'https://www.cp.pt'
index_url = root_url + '/passageiros/pt/consultar-horarios/estacoes'

session = HTMLSession()

stations = {'stations' : []}

def get_stations_url():
    page = session.get(index_url)
    station_url_table = page.html.find('tbody tr a')

    for station_url in station_url_table:
        station = dict()
        station['url'] = root_url + station_url.attrs['href']
        stations['stations'].append(station)


def get_stations_info(url, index):
    page = session.get(url)

    station_data = page.html.find('div.station-data')[0]

    stations['stations'][index]['name'] = station_data.find('h1', first = True).text
    print(stations['stations'][index]['name'])

    station_main_data = station_data.find('ul li')

    #Address
    try:
        stations['stations'][index]['address'] = station_main_data[0].text.split(':')[1].strip()
    except:
        print('Error: Address not setted.')

    #Location
    try:
        coord = station_main_data[1].text.split(':')[1].split('|')
        location = []
        location.append(float(coord[0].replace(',', '')))
        location.append(float(coord[1].replace(',', '')))
        stations['stations'][index]['location'] = location
    except:
        print('Error: Location not setted.')

    #CP Services
    try:
        for index2, service in enumerate(station_main_data[2].text.split(':')[1].split('|')):
            if index2 == 0:
                        stations['stations'][index]['cp_services'] = []
            stations['stations'][index]['cp_services'].append(service.strip())
    except:
        print('Error: CP Services not setted.')

    #Lines
    try:
        for index2, line in enumerate(station_main_data[3].text.split(':')[1].split('|')):
            if index2 == 0:
                        stations['stations'][index]['lines'] = []
            stations['stations'][index]['lines'].append(line.strip())
    except:
        print('Error: Line(s) not setted.')

    #Services
    try :
        station_services = page.html.find('div.tab-content', first=True)

        if station_services.find('ul'):
            stations['stations'][index]['services'] = dict()

        cp_services, access_connections, facilities, complementary_services = False, False, False, False
        for services in station_services.find('ul'):

            #CP Services
            if cp_services == False:
                if page.html.find('ul li', containing='Serviços CP') :
                    stations['stations'][index]['services']['cp_services'] = []
                    for service in services.find('li'):
                        stations['stations'][index]['services']['cp_services'].append(service.text)
                    cp_services = True
                    continue

            #Access/Connections
            if access_connections == False:
                if page.html.find('ul li', containing='Acessos e Ligações') :
                    stations['stations'][index]['services']['access_connections'] = []
                    for service in services.find('li'):
                        stations['stations'][index]['services']['access_connections'].append(service.text)
                    access_connections = True
                    continue


            #Facilities
            if facilities == False:
                if page.html.find('ul li', containing='Mobilidade Condicionada') :
                    stations['stations'][index]['services']['facilities'] = []
                    for service in services.find('li'):
                        stations['stations'][index]['services']['facilities'].append(service.text)
                    facilities = True
                    continue

            #Complementary Services
            if complementary_services == False:
                if page.html.find('ul li', containing='Serviços Complementares') :
                    stations['stations'][index]['services']['complementary_services'] = []
                    for service in services.find('li'):
                        stations['stations'][index]['services']['complementary_services'].append(service.text)
                    complementary_services = True
                    continue

    except:
        print('Error: Services not setted')

def parse_station_to_file(dict, filename):
    with open(filename, 'w') as file:
        json.dump(dict, file, indent = 4, ensure_ascii = False)


get_stations_url()

for index, station in enumerate(stations['stations']):
    get_stations_info(station['url'], index)
    print(str(index+1) + '/' + str(len(stations['stations'])))

parse_station_to_file(stations, 'data.json')
