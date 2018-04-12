#! /usr/bin/python3

import script
import json
from pprint import pprint

test = script.Parks()



#test.get_osm_info()
#id = input("Enter osm id:")
test.get_park_total_count()
print("call test.list_osm_info()")
input("Press Enter to Continue")
test.list_osm_info()
pprint(test.osm_info_list)

results = []
count = 0
for item in test.osm_info_list:
    print( "count: %d" % count)

    count +=1
    resultj = json.loads(test._call_overpass(item,True))
    results.append(resultj)
    print("leisure count: " , len(resultj["features"]))
    input("Press Enter to Continue")

#results = test._call_overpass(id,True)


#resultsJson = json.loads(results)

#print(type(resultsJson))


#pprint.pprint(resultsJson)



