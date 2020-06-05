import xml.etree.ElementTree as ET 

tree = ET.parse('planet.osm')
db = tree.getroot()

def main():
    print('No longer valid')

def getHighways():
    highways = []
    for child in db.iter('way'):
        way = child
        print("\n id =", way.attrib['id'])
        vals = {'refs': []}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        for element in way.iter('nd'):
            vals['refs'].append(element.attrib['ref'])
        highways.append(vals)
    return highways



def getNodeByRef(ref):
    ref = str(ref)
    node = {}
    for child in db.iter('node'):
        if child.attrib['id'] == ref:
            node = child
            break
    res = {
        'id' : ref, 
        'lat' : node.attrib['lat'],
        'lon' : node.attrib['lon']
    }
    for child in node:
        res[child.attrib['k']] = child.attrib['v']
    return res

def getNodesCoords():
    res = {}
    for child in db.iter('node'):
        res[child.attrib['id']] = (child.attrib['lat'], child.attrib['lon'])
    return res

def getBuildingsNodes():
    buildings = []
    for child in db.iter('way'):
        way = child
        vals = {'node': ''}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        if not 'building' in vals:
            continue
        buildings.append(next(way.iter('nd')).attrib['ref'])
    return buildings


def getHospitalsNodes():
    hospitals = []
    for child in db.iter('way'):
        way = child
        vals = {'node': ''}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        if not 'amenity' in vals:
            continue
        elif not vals['amenity'] == 'hospital':
            continue 
        hospitals.append(next(way.iter('nd')).attrib['ref'])
    return hospitals

def getRelations():
    res = []
    for child in db.iter('relation'):
        vals = {'members': []}
        for member in child.iter('member'):
            vals['members'].append(member.attrib)
        for tag in child.iter('tag'):
            vals[tag.attrib['k']] = tag.attrib['v']
        res.append(vals)
    return res


def getBuildings(type = ''):
    buildings = []
    for child in db.iter('way'):
        way = child
        vals = {'node': ''}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        if not 'building' in vals:
            continue
        # print("\n id =", way.attrib['id'])
        for element in way.iter('nd'):
            vals['node'] = element.attrib['ref']
            break
        buildings.append(vals)
    return buildings

def getItemsByAmenity(type = ''):
    items = []
    for child in db.iter('way'):
        way = child
        vals = {'node': ''}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        if not 'amenity' in vals:
            continue
        elif not vals['amenity'] == type:
            continue 
        print("\n id =", way.attrib['id'])
        for element in way.iter('nd'):
            vals['node'] = element.attrib['ref']
            break
        items.append(vals)
        # print(vals)
    # print(type)
    return items

def getStreets():
    streets = []
    for child in db.iter('way'):
        way = child
        vals = {'refs': []}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        if not 'highway' in vals:
            continue
        #print("\n id =", way.attrib['id'])
        for element in way.iter('nd'):
            vals['refs'].append(element.attrib['ref'])
        streets.append(vals)
    return streets


def getRoads():
    streets = []
    not_roads = ['pedestrian', 'footway', 'bridleway','steps','sidewalk','cycleway','construction']
    for child in db.iter('way'):
        way = child
        vals = {'refs': []}
        for element in way.iter('tag'):
            vals[element.attrib['k']] = element.attrib['v']
        if not 'highway' in vals:
            continue
        if (vals['highway'] in not_roads):
            continue
        #print("\n id =", way.attrib['id'])
        for element in way.iter('nd'):
            vals['refs'].append(element.attrib['ref'])
        streets.append(vals)
    # print(streets)
    return streets

# if __name__ == "__main__":
    # print(getItemsByAmenity('hospital'))
    # streets = getStreets()
    # print(type([streets]))
    # for street in streets:
    #     if 'name' in street:
    #         if street['name'] == 'улица Смирнова':    
    #             for ref in street['refs']:
    #                 getNodeByRef(ref)
    #             print('')

