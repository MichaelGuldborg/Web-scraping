import requests
import smtplib

url = "http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/DK/dkk/en-US/cph/anywhere/anytime/anytime?apikey=prtl6749387986743898559646983194"
response = requests.get(url)

data = response.json()

id_to_place = {}
places = data['Places']
for place in places:
    id_to_place[place['PlaceId']] = place['Name']

routes = []
routes.extend(data['Routes'])

for route in routes:
    try:
        route['Price']
    except:
        route['Price'] = 0

sorted_routes = sorted(routes, key=lambda x: x['Price'], reverse=False)
for route in sorted_routes:
    if route['Price'] != 0:
        origin = id_to_place[route['OriginId']]
        destination = id_to_place[route['DestinationId']]
        price = route['Price']
        print("from: {}, to: {}, price: {} dkk".format(origin, destination, price))
