#! /usr/bin/python3

import script
import pprint
import json


def print_amenities(park):

    amenities_length=len(park["features"])
    print(amenities_length)

    #pprint.pprint(park["features"])
    print(4*'\n')
    for  index, item in enumerate(park["features"]):
        print( "%d : %s" % (index, item["properties"]))
        print("\n")


def get_amenities(park):
    results = test._call_overpass(park,True)
    results_json = json.loads(results)
    try:
        print_amenities(results_json)
    except:
        pass



amenities_array[]

test = script.Parks()
test.get_park_total_count()
print(40*'%%%%%')
test.list_osm_info()
#pprint(foo.osm_info_list )



#target = "way(32515094)"
#results = test._call_overpass(target,True)

#results_json = json.loads(results)

#print_amenities(results_json)


#print (results)

print("osm_info_list")
pprint.pprint(test.osm_info_list)

for item in test.osm_info_list:
    get_amenities(item)



