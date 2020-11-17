'''
-Get a search bar going
- learn how to use debugger and test 
- get in line errors 
'''
import Google_Maps_Class as GM
GOOGLE_API_KEY = "--NEEDS KEY--"

def Find_Place(results, query, location):
    print('Locations that provide', query,'in', location)
    count = 1
    search_results_id = []
    for item in results:
        print("===== Location",count,"======")
        print('Place:',item['name'],'\nAddress: ', item['vicinity'], '\nRating: ', item['rating'],"\n")
        search_results_id.append(item['place_id'])
        count += 1
    return search_results_id

def get_location_detail(user, place_id):
    results = user.place_detail(place_id)
    #Fprint(results)
    try:
        print('Location Name: ',results['name'],'\nPhone Number: ',results['formatted_phone_number'],'\nLocation Hours: ',results['opening_hours']['weekday_text'])
    except:
        print(results)
    #for item in results['opening_hours']:
        #print(item)

def main():
    print("What are you looking for? (Examples vegan Food, Substaibale Super markets)")
    query = input('Enter Here: ')
    print('What the location?')
    location = input("Enter General area or address?")
    user = GM.GoogleMapsAPI(GOOGLE_API_KEY, address_or_postal_code = location)
    user.extract_lat_lng(location)
    search_results_id = Find_Place(user.search( keyword = query, radius = 5000, location = location), query, location)
    print("Which location would you like to view in detail?\n")
    query = int(input("Enter Location Number: "))-1
    get_location_detail(user,search_results_id[query])
    #IFrame(user.map_results(query, location), width=700, height=350)


if __name__ == '__main__':
    main() 
