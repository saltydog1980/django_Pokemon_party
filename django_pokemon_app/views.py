from django.shortcuts import render
import requests as HTTP_Client
import pprint
import random
#setting up pprint
pp = pprint.PrettyPrinter(indent=2, depth=3)

#serving up the main landing page
def index(request):
    return render(request, 'pages/index.html')

#Pulled this out and set in it's own function to reduce repetition
#all my call outs to the API
def get_poke(endpoint):
    API_response = HTTP_Client.get(endpoint)
    responseJSON = API_response.json()
    return responseJSON

#view to serve up ultimate page
def detail(request):
    #creating a name list so we do not repeat
    name_list = []
    #building the poke party dict out
    poke_party = {}
    # Set our endpoint with the starting pokemon
    selected_choice = request.POST['choice']
    #checking to see if input is blank
    #if it is, generating random to start with
    if selected_choice != "":
        poke_id = selected_choice
    else:
        poke_id = random.randrange(1, 906)
    #setting endpoint to send to get poke
    endpoint = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    #sending out and getting response from API for initial poke
    responseJSON = get_poke(endpoint)
    
    #adding first poke and all attributes
    poke_party[0] = {}
    name_list.append(responseJSON['name'])
    poke_party[0]['name'] = responseJSON['name']
    poke_party[0]['img'] = responseJSON['sprites']['front_default']
    poke_party[0]['type_name'] = responseJSON['types'][0]['type']['name']
    poke_party[0]['type_url'] = responseJSON['types'][0]['type']['url']
    
    #setting endpoint to grab the list of pokes of said type of poke 0
    endpoint2 = f"{responseJSON['types'][0]['type']['url']}"
    
    #sending to get the list
    response2JSON = get_poke(endpoint2)

    #list of poke of type
    poke_type_list = response2JSON['pokemon']

    #count of poke in list
    poke_count = len(poke_type_list)

    #while loop to populate the poke party
    while len(name_list)<6:
        #pulling random poke out of list
        new_poke = poke_type_list[random.randrange(0, poke_count)]
        #if new poke already in list restarting loop with continue
        if new_poke['pokemon']['name'] in name_list:
            continue
        #if not in list setting new endpoint
        new_endpoint = new_poke['pokemon']['url']
        
        #calling get poke to get new poke
        response3JSON = get_poke(new_endpoint)
        #if the poke has no picture restarting the loop
        if response3JSON['sprites']['front_default'] == None:
            continue
        
        #if not in party adding new poke and their attributes to name list and dict
        name_list.append(response3JSON['name'])
        poke_party[len(name_list)-1] = {}
        poke_party[len(name_list)-1]['name'] = response3JSON['name']
        poke_party[len(name_list)-1]['img'] = response3JSON['sprites']['front_default']

    #now creating data to pass to my detail page
    data = {'poke_party': poke_party}


    return render(request, 'pages/detail.html', data)