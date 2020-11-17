import requests #used to interact wiht API
from IPython.display import IFrame
from urllib.parse import urlencode, urlparse, parse_qsl
class GoogleMapsAPI(object):
    lat = None
    lng = None
    data_type = 'json'
    location_query = None 
    api_key =  None
    place_id = None
    
    def __init__(self, api_key = None, address_or_postal_code = None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if api_key == None:
            raise Exception("Needs APi") 
        self.api_key = api_key 
        self.location_query = address_or_postal_code
        if self.location_query != None:
            self.extract_lat_lng()
    
    def extract_lat_lng(self, location = None):
        loc_query = self.location_query
        if location != None:
            loc_query = location
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}" #<use of endpoint 
        params = {"address": loc_query, "key": self.api_key}#< dictionary for params contains address and key
        url_params = urlencode(params)#< encodes input or address into a url acceptable param
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200,299):#<-- This is so if there are no searches found
            return {}
        else:
            lat_lng = {}
        try:
            lat_lng = r.json()['results'][0]['geometry']['location'] #<-- saves the lat and long into dic from request dict
        except:#<-- error controle
            pass
        self.lat = lat_lng.get('lat')
        self.lng = lat_lng.get('lng') #<-- Shows tha lat in long
        return self.lat, self.lng
    
    def search(self, keyword = None, radius = 5000, location = None):
        lat, lng = self.lat, self.lng
        if location != None:
             lat,lng = self.extract_lat_lng(location = location)
        endpoint= f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}" #< NEAR BY EXAMPLE
        params = {
            "key": self.api_key,
            "location":f"{lat},{lng}",
            "radius": radius,
            "keyword": keyword   
        }
        encoded_params = urlencode(params)
        places_url = f'{endpoint}?{encoded_params}'
        r = requests.get(places_url)
        if r.status_code not in range(200,299):
            return {}
        else:
            return r.json()['results']
        
    def place_detail(self, place_id = None):
        detail_base_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
        detail_params = {
        "key" : self.api_key,
        "place_id": f"{place_id}",
        "fields" : "name,rating,formatted_phone_number,opening_hours,price_level" 
        }
        detail_encode = urlencode(detail_params)
        url_place_detail = f'{detail_base_endpoint}?{detail_encode}'
        r = requests.get(url_place_detail)
        if r.status_code not in range(200,299):
            return []
        else:
            return r.json()['result']
        
    def map_results(self, query = None, location = None):
        map_url = 'https://www.google.com/maps/embed/v1/'
        mode = 'search'
        params = {
            'key':self.api_key,
            'q':f'{query} around {location}',
            'center':f'{self.lat},{self.lng}',
            'zoom' : '10'
        }
        params_encode = urlencode(params)
        map_url = f'{map_url}{mode}?{params_encode}'
        return map_url 
