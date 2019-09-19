import requests,time,sys

ver=sys.version_info[0]


t=time.time()

#Intialising server request!
print("Requesting Server.....")
r=requests.get('http://vtslive.in/nist/getMobilityData.php?L=smartgreencampus@nist&P=smart@nist')
res = r.json()



index_list=[0]*len(res['busDetails'])
for i in range(len(res['busDetails'])):
    index_list[i]=res['busDetails'][i]['busNum']


#General Instructions and Information Displayed!
print("\n \n \n Welcome !! This is a command-line application! You can request Bus Tracking Information as many times as you want. \n Request to server is sent every 20 seconds \n\n \n\nInstructions: \n 1. The Bus live GPS information will be provided if you enter the correct bus number [Valid Bus numbers lie between 1 and 40] \n 2. To exit the application, type 0 and press ENTER. \n \n\n\n ")


#For Place approximation, I used 10,000 latitude and longitude points spread over a square region of area 100km^2 with it's centre as (19.197504,84.747889) which is the centre of NIST Behrampur:
# I got only three major reverse geolocations ['Ichchapuram', 'Brahmapur', 'Chikitigarh'] So, I will be mapping coordinates to these three places based on my coordinate learnings!

def get_place(l):
    lat=float(l[0])
    lng=float(l[1])
    lat=round(lat,2)
    lng=round(lng,2)
    if(lat<19.19):
        return 'Ichchapuram'
    if(lat==19.19):
        if(lng<84.77):
            return 'Ichchapuram'
        else:
            return 'Brahmapur'
    if(lat==19.20):
        if(lng<84.75):
            if(lng<=84.70):
                return 'Chikitgarh'
            else:
                return 'Ichchapuram'    
        else:
            return 'Brahmapur'
    if(lat==19.23 and lng >=84.71):
        return 'Brahmapur'
    if(lat==19.23 and lng <84.71):
        return 'Chikitgarh'
    if(lat==19.22 and lng >=84.72):
        return 'Brahmapur'
    else:
        return 'Chikitgarh'
    if(lat==19.21 and lng >=84.73):
        return 'Brahmapur'
    else:
        return 'Chikitgarh'



f=0
while(f==0):
    #New Input arrives!
    if(ver==3):
        N=input("Enter Bus Number: ")
    elif(ver==2):
        N=raw_input("Enter Bus Number: ")
    
    #Checking for Exit condition
    if(N=='0'):
        print("\n\n\nExiting command-line application! Good Bye :)\n\n\n")
        f==1
        break
    
    #Checking for Invalid Bus Index
    if(N not in index_list):
        print("\n\nBus Number Invalid!\n\n")
        continue

    #Checking time elapsed since last server request. Server Request refreshed at every 20 seconds
    if(time.time()-t>20):
        print("\n\nRequesting Server.....\n\n")
        t=time.time()
        r=requests.get('http://vtslive.in/nist/getMobilityData.php?L=smartgreencampus@nist&P=smart@nist')
        res = r.json()

    index_list=[0]*len(res['busDetails'])
    for i in range(len(res['busDetails'])):
        index_list[i]=res['busDetails'][i]['busNum']

    #Extracting details from JSON Object
    details = res['busDetails'][index_list.index(N)]
    is_moving = False
    no=details['busNum']
    gps=details['gps']

    #Checking if BUS DATA IS AVAILABLE OR NOT
    if(gps is None ):
        print("\n\nBus Tracking information not available for this bus!\n\n")
        continue
    velocity=gps.split('Velocity : </b>')[1].split('km/h')[0]

    lat=details['lat']
    lng=details['lng']

    #Extracting Place information using learned places from get_place() function.
    place=get_place([lat,lng])


    #Printing the results
    print("\n\nBus Tracking information available for this bus!\n\n")
    print('Bus Number: '+str(no))
    print('Geolocation:- Latitude- '+str(lat)+' Longitude- '+str(lng))
    print('Place of bus: '+place)

    #Checking if bus is moving or not using velocity 
    if(velocity!=0):
        is_moving=True
        print('Bus is moving! with a velocity '+str(velocity)+' km/h\n\n\n')
    else:
        print('Bus is not moving!\n\n\n')

