import http.client
import json
import time
import timeit
import sys
import collections
from pygexf.gexf import *

#
# implement your data retrieval code here
#
key = str(sys.argv[1])
print(key)
connection = http.client.HTTPSConnection("www.rebrickable.com")
url = "https://rebrickable.com/api/v3/lego/sets/?key=" + key + "&page_size=280&ordering=-num_parts"
connection.request("GET", url)
response = connection.getresponse()
start = timeit.default_timer()
a = json.loads(response.read())
# List of dictionary of sets. keys: set_num, name, year, theme_id, num_parts, set_img_url, set_url, last_modified_dt
sets = a["results"]
def sortQ(val):
    return val["quantity"]

part = {}
count = 0
for i in sets:
    set_num = i["set_num"]
    count = count + 1

    end = timeit.default_timer()
    if end - start < 1:
        time.sleep(1.01 - (end - start))
    url = "https://rebrickable.com/api/v3/lego/sets/" + str(set_num) + "/parts/?key=" + key + "&page_size=1000"
    connection.request("GET", url)
    response = connection.getresponse()
    start = timeit.default_timer()

    a = json.loads(response.read())
    res = a["results"]
    parti = []
    next = a["next"]
    while next:
        connection.request("GET", next)
        response = connection.getresponse()
        a = json.loads(response.read())
        res.extend(a["results"])
        next = a["next"]

    for j in res:
        parti.append({"color" : j["color"]["rgb"], "quantity" : j["quantity"], "name" : j["part"]["name"], "number" : j["part"]["part_num"] + "_" + j["color"]["rgb"]})
    parti.sort(key=sortQ, reverse=True)
    parti = parti[0:20]
    # dictionary, key is set_num, value is list of 20 dictionaries of parts
    part[set_num] = parti

# complete auto grader functions for Q1.1.b,d
def min_parts():
    """
    Returns an integer value
    """
    # you must replace this with your own value
    return 1140

def lego_sets():
    """
    return a list of lego sets.
    this may be a list of any type of values
    but each value should represent one set

    e.g.,
    biggest_lego_sets = lego_sets()
    print(len(biggest_lego_sets))
    > 280
    e.g., len(my_sets)
    """
    res = []
    for i in sets:
        res.append({"set_num" : i["set_num"], "name" : i["name"]})
    return res

def gexf_graph():
    """
    return the completed Gexf graph object
    """
    # you must replace these lines and supply your own graph
    gexf = Gexf("Jiahua Song", "Visualization of Sets and Parts")
    graph = gexf.addGraph("undirected", "static", "graph")
    graph.addNodeAttribute(title='Type', type='string')
    for i in sets:
        set_node = graph.addNode(i["set_num"], i["name"], r='0', g='0', b='0')
        set_node.addAttribute('0', "set")
        part_list = part[i["set_num"]]
        for j in part_list:
            if graph.nodeExists(j["number"]):
                graph.addEdge(id=i["set_num"] + j["number"], source=i["set_num"], target=j["number"], weight=j['quantity'])
                continue
            part_node = graph.addNode(j["number"], j["name"], r=str(int(j["color"][0:2], 16)), g=str(int(j["color"][2:4], 16)), b=str(int(j["color"][4:6], 16)))
            part_node.addAttribute('0', 'part')
            graph.addEdge(id=i["set_num"] + j["number"], source=i["set_num"], target=j["number"], weight=j['quantity'])
    file = open('bricks_graph.gexf', 'wb')
    gexf.write(file)
    return gexf.graphs[0]

def avg_node_degree():
    """
    hardcode and return the average node degree
    (run the function called “Average Degree”) within Gephi
    """
    # you must replace this value with the avg node degree
    return 5.409

def graph_diameter():
    """
    hardcode and return the diameter of the graph
    (run the function called “Network Diameter”) within Gephi
    """
    # you must replace this value with the graph diameter
    return 8

def avg_path_length():
    """
    hardcode and return the average path length
    (run the function called “Avg. Path Length”) within Gephi
    :return:
    """
    # you must replace this value with the avg path length
    return 4.416
