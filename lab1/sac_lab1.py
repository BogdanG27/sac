from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItem, AddItemProperty, SetItemValues, ListItems
from recombee_api_client.exceptions import APIException
import pandas as pd

client = RecombeeClient(
  'upb-bogdan-dev', 
  'RG145oZPeIsquQMafD1T1rZ53dyXpWBWzYPcSKk3RJQwUDLXbbJqEnKg9fPTCunO', 
  region=Region.EU_WEST
)

df = pd.read_csv('top100cities.csv', usecols=["city", "state", "population_2020", "land_area_sqmi"])

def addItemProperties():
    client.send(AddItemProperty('city', 'string'))
    client.send(AddItemProperty('state', 'string'))
    client.send(AddItemProperty('population_2020', 'int'))
    client.send(AddItemProperty('land_area_sqmi', 'double'))


def addItems():
    # add items
    for index, row in df.iterrows():
        cityId = str(index)  # You can use a unique identifier as the item ID

        try:
            # Send the item data to Recombee
            client.send(AddItem(cityId))
            print(f"Added city with ID {cityId} to Recombee")
        except APIException as e:
            print(f"Error adding city with ID {cityId} to Recombee: {e}")

    addItemProperties()

    for index, row in df.iterrows():
        city = row['city']
        state = row['state']
        population_2020 = row['population_2020']
        land_area_sqmi = row['land_area_sqmi']

        # Define the item data
        item_data = {
            'city': city,
            'state': state,
            'population_2020': population_2020,
            'land_area_sqmi': land_area_sqmi,
        }
        client.send(SetItemValues(str(index), item_data))
        print(f"Added data for city with ID {index} to Recombee")
        

def printItems():
    result = client.send(ListItems(return_properties=True))
    print(result)

addItems()
printItems()