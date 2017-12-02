#! /usr/bin/env python3

# Grab osm data and convert geojson



import requests
import json
import sys
from pprint import pprint
import subprocess
import overpass
import psycopg2
from psycopg2.extensions import adapt

URL_PARKS = "https://parks.api.codefornrv.org/parks"
URL_DB = "http://localhost:3000/fuk"
URL_OVERPASS = "http://overpass-api.de/api/interpreter?data="

class Parks(object):
    """ Handled talking to park.api.codefornrv"""



    def __init__(self):
        self.nulled_parks_count = 0
        self.nulled_parks = []
        self.total_parks_count = 0
        self.all_parks_data = None
        self.osm_info_list = []


    def _get_nulled_park_count(self):
        count = len(self.nulled_parks)
        return count

    def _print_nulled_park_ids(self):
        id_array = []
        for item in self.nulled_parks:
            id_array.append(item["id"])
        return id_array

    def _return_park_total_count():
        return self.nulled_parks_count

    def _get_overpass_string(self, target):
        target_string = "[out:json];" + target + ";out body; >; out skel qt;"
        return target_string

    def _get_overpass_string_amenities(self, target):
        target_string = "[out:json];" + target + ";map_to_area -> .a;way(area.a)[leisure];(._;>;);out;node(area.a)[leisure];out;"
        return target_string
    def _call_overpass(self, target, amenities):
        try:

            """Feb 2, 2017 Changing to using overpass python wrapper verison

            """
            if(amenities==False):
                r = requests.post(URL_OVERPASS, self._get_overpass_string(target))
                print(self._get_overpass_string(target))
            if(amenities==True):
                r = requests.post(URL_OVERPASS,self._get_overpass_string_amenities(target))
                print(self._get_overpass_string_amenities(target))
            print("\n%%%%%\n\n" + r.text + "\n$$$$\n")
            tmp = open('tmp.json', 'w+')
            tmp.write(r.text)
            tmp.close()


            print(subprocess.getoutput("osmtogeojson tmp.json > retmp.json"))

            data = open('retmp.json').read()


        except:
            print("Failed to call overpass")
            print(target)

        return data


    def get_park_total_count(self):
        try:
            r = requests.get(URL_PARKS)
            print("%%%%%%%%%%% getting parks")
            pprint(r.text)

            data = json.loads(r.text)
            print(len(data))
            self.total_parks_count = len(data)
            self.all_parks_data = data
            pprint(self.all_parks_data)
        except Exception as e:
            print("Unable to get total count of the parks/n")
            print(e)

    def list_osm_info(self):

        pprint(self.all_parks_data)

        print("before the for loop list")
        for item in self.all_parks_data:
            print(item)
            print("loop")
            try:
                print(item['osm_info'][0])
               # input("Pause 106 ")
                for index,osm in enumerate(item['osm_info'], start=0):

                    print(index, osm['id'], osm['type'])
                    osm_result = "%s(%s)" % (osm['type'], osm['id'])
                    print("osm_result : %s " % osm_result)
                #    input("Pause....")
                    self.osm_info_list.append(osm['type']+ '(' + osm['id']+')')
               # print("After for loop ln115")
            except:
                continue

        return(self.osm_info_list)

    def get_osm_info(self, id):
        for item in self.nulled_parks:
            pprint(item)
           # #input("Press enter to continue")
            if(item["id"] == id):
                #for info in ["osm_info"]:
                print("")
                print(item["osm_info"])
               # #input("At get_osm_info:  Press enter to continue...." )
                if(item["osm_info"]["osm_info"] == 'None'):
                    print("No osm_info entered. Returning 404")
                    return 404
                else:
                    return item["osm_info"]["osm_info"]


    def get_list_of_null_parks(self):
        _endpoint = URL_PARKS + "?geom=is.null"
        try:
            r = requests.get(_endpoint)
        except Exception as e:
            print("Failed Getting Nulled parks...")
        if (r.status_code == 200):
            print("Get Successful")
            print("")
            self.nulled_parks = json.loads(r.text)
            pprint(self.nulled_parks)
            self.nulled_parks_count = self._get_nulled_park_count()
            #print(self._print_nulled_park_ids())
            print("\n\nNumber of Parks with no geometeries: %s" % self.nulled_parks_count)

        elif (r.status_code !=200):
            print("Failure, Status Code: %s" % r.status_code)
            print(_endpoint)

    def get_nulled_geometeries(self):

        db = DB()

        if (len(self.nulled_parks) == 0):
            print("Checking parks.api for Parks with no geometery data.... ")
            try:
                self.get_list_of_null_parks()

            except:
                print("Failed checking for parks.api....")
        else:
            for items in self.nulled_parks:
                pprint(self.nulled_parks)
                print("osm_info  >>>>  %s " % ( items["osm_info"]))
                try:
                    arr = self.get_osm_info(items["id"])
                except:
                    print("Error has occured getting osm_info. Moving on to next Park..")
                    continue
                target = ("%s(%s)" % (arr[0]["type"], arr[0]["id"] ))
                print("calling: " + self._get_overpass_string(target))
                pprint(self._call_overpass(target))
                print(items["id"])
                #input("Press enter to continue")

                items["geom"] = self._call_overpass(target)

                print(items["geom"])
#                r = requests.patch(
#                     ("%s%s%d" % (URL_DB,"?id=eq.",items["id"])),
#                    {"geom" : items["geom"]}
#                )

                db.add_data(items["id"] , items["geom"])

      #      db.fill_point_location()

                #print(r.text)






    #def set_nulled_parks()
        #for item in
class DB(object):

    def __init__(self):
        self.conn = psycopg2.connect(database="",
                                     user="",
                                     password="",
                                     host="")
        self.cur  = self.conn.cursor()

    def add_data(self, id, data):
        print("++++++++++++")
        var_geojson = adapt(data)
        print(var_geojson)
        input("Press enter to continue")
        execute_string = """ SELECT parks.update_geojson(%s, %s )""" % (id , var_geojson)

#        excute_string = """UPDATE parks.parks SET geom = ST_Multi(ST_GeomFromGeoJSON
#        ('{
#                "type":"Polygon",
#                "coordinates":
#                    [
#                       [
#                            [1,1]
#                        ]
#                   ],
#                "crs": {"type":"name","properties":{"name":"EPSG:4326"}}
#        }')) """
#
#        excute_string = """UPDATE parks.parks SET geom = ST_Multi(ST_GeomFromGeoJSON
#
#            ('{
#
#            }')) """
#
        self.cur.execute(execute_string)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def fill_point_location(self):
        execute_string = """UPDATE parks.parks SET point_location = ST_Centroid(geom) WHERE geom IS NOT NULL;"""
        self.cur.execute(execute_string)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

#print("Init of Parks class... \n*\n*\n*\n*  ")
#
#foo = Parks()
#
#print("\n\n\nMaking a list of parks with empty geom rows...... \n>\n>\n>\n>")
#foo.get_list_of_null_parks()
#print("""\n\n\nAttempting to grad geom data.... foo.get_nulled_geometeries() \n*\n*\n*\n*\n*""")
#
#
#foo.get_nulled_geometeries()
#
#foo.nulled_parks
#

foo = Parks()

#print(foo._get_nulled_park_count())

foo.get_park_total_count()
#print(40*'%%%%%')
foo.list_osm_info()
pprint(foo.osm_info_list )
