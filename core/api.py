import requests

# Get API connection.
url = "https://interactiveellieapi.herokuapp.com/live/ppl_count"
r = requests.get(url)    
# If there is a positive callback for the connection, put the starting value of 0.
if r.status_code == 200:
    r2 = requests.put(url, json = {'value':0})

# Last amount that the API received.
past_api_amount = [0]

# Array for the detected amounts to only put a new detected value if it has been consistent for a number of frames.
past_amounts_list = [0,0,0,0,0,0,0,0,0]

# Function to check if all items in an array are the same. Return True ifso.
def check_array_items_equal(array):
    print(array)
    for i in range(len(array)):
        if i != (len(array) -1):
            if array[i] != array[i + 1]:
                return False
    return True

# Function to check if putting the new value should be allowed by checking if it has been consistent for a number of frames.
def check_put_allowed(array):
    if check_array_items_equal(array) == False:
        return False
    return True


def put_people_amount(amount):

    # Adds latest detected amount to array and moves al previous values one place to the left.
    for i in range(len(past_amounts_list)):
        if i == (len(past_amounts_list) -1):            
            past_amounts_list[len(past_amounts_list) -1] = amount
        else: 
            past_amounts_list[i] = past_amounts_list[i + 1]  

    # prev_ppl = r.json()['value']
    # # An if to prevent unnecessary API puts when the new value is the same as the one already in the API.
    # if amount != prev_ppl:
    
    # If new detected value is not the same as the one already put to the API.
    # Added to prevent unnecessary API events and unnecessary frame drops as a result. (FPS goes back to around 10 instead of constantly at around 1.)
    if past_api_amount[0] != amount:

        # If persmission is granted for putting the new detected value.
        if check_put_allowed(past_amounts_list) == True:
            r = requests.get(url)
            # If there is a positive callback for the connection, put the amount to the api.
            if r.status_code == 200:
                print("The API receives " + str(amount))
                # Put the current amount to the API
                r2 = requests.put(url, json = {'value':amount})
                past_api_amount[0] = amount