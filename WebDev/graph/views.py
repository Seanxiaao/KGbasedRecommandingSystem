from django.shortcuts import render
from django.views import View
from WebDev.settings import driver
import json
from django.http import HttpResponse

# Create your views here.
# A drafted version, will later make separation for front/backend

# Group information
group = {
    'MUSIC': 1,
    'PERSON': 2,
    'DBPEDIA_SUBJECT': 3,
    'DBPEDIA_TYPE': 4,
    'TAG': 5,
    'WORD': 6,
    'WORDNET_WORD': 7,
}


def get_property_name(property):
    return property.get('label')


class GraphView(View):
    TEMPLATE = 'graph.html'

    # node example {'id': 'Mlle.Baptistine', 'group': 1}
    # link example {'source': 'Claquesous', 'target': 'Valjean', 'value': 1},

    def get(self, request):
        # get the id and name relationship
        id_name_dic = {}
        # first get the dbdata
        data_dic = {
            'nodes': [],
            'links': []
        }

        with driver.session() as session:
            # seperate match then

            result = session.run("MATCH (n)-[r]->(m) RETURN "
                                 "properties(n) as n_properties, labels(n) as n_labels, "
                                 "id(n) as n_id, r, "
                                 "properties(m) as m_properties, labels(m) as m_labels, "
                                 "id(m) as m_id LIMIT 1000")

            # make component of json
            for record in list(result):
                # check if n in the graph
                if not record['n_id'] in id_name_dic.keys():
                    temp_dic = {}
                    curr_property, curr_label = record['n_properties'], record['n_labels']
                    name = get_property_name(curr_property)
                    temp_dic.update({'id': name})
                    key = curr_label[0].upper()
                    temp_dic.update({'group': group[key]})
                    id_name_dic.setdefault(record['n_id'], name)
                    temp_dic.update({'_id': record['n_id']})
                    # append node
                    data_dic['nodes'].append(temp_dic)
                # check if m in the graph
                if not record['m_id'] in id_name_dic.keys():
                    temp_dic = {}
                    curr_property, curr_label = record['m_properties'], record['m_labels']
                    name = get_property_name(curr_property)
                    temp_dic.update({'id': name})
                    key = curr_label[0].upper()
                    temp_dic.update({'group': group[key]})
                    id_name_dic.setdefault(record['m_id'], name)
                    temp_dic.update({'_id': record['m_id']})
                    data_dic['nodes'].append(temp_dic)
                if record['r'] is not None:
                    nodes = record['r'].nodes
                    source, target, rel = nodes[0], nodes[1], record['r'].type
                    temp_dic = {}
                    try:
                        temp_dic.setdefault('source', id_name_dic[source.id])
                        temp_dic.setdefault('target', id_name_dic[target.id])
                        temp_dic.setdefault('relation', rel)
                        temp_dic.setdefault('value', 1)
                    except KeyError:
                        raise Exception("key not found")
                    # append relationship
                    data_dic['links'].append(temp_dic)
        return render(request, self.TEMPLATE, {'data': json.dumps(data_dic)})


class NodeDetailView(View):
    TEMPLATE = 'graph.html'

    # a bug need to fix tommorow
    def get(self, request, node_id):

        id_name_dic = {}
        visited_path = set()
        data_dic = {
            'nodes': [],
            'links': []
        }

        with driver.session() as session:
            # 2 - hop
            match_query = "MATCH (n) WHERE id(n) = $node_id CALL apoc.path.expandConfig(n, " \
                          "{minLevel:1, maxLevel:2}) YIELD path WITH n, RELATIONSHIPS(path) as relation, " \
                          "LAST(NODES(path)) as m RETURN " \
                          "properties(n) as n_properties, labels(n) as n_labels, id(n) as n_id, " \
                          "relation, " \
                          "properties(m) as m_properties, labels(m) as m_labels, id(m) as m_id;" \
            # bfs
            # have bug with nodes like 90765
            # match_query = "MATCH (n) WHERE id(n) = $node_id CALL apoc.path.expandConfig(n, " \
            #               "{relationshipFilter: '>', minLevel:1}) " \
            #               "YIELD path WITH n, RELATIONSHIPS(path) as relation, " \
            #               "LAST(NODES(path)) as m RETURN " \
            #               "properties(n) as n_properties, labels(n) as n_labels, id(n) as n_id, " \
            #               "relation, " \
            #               "properties(m) as m_properties, labels(m) as m_labels, id(m) as m_id;" \

            result = session.run(match_query, node_id=node_id)

            for record in list(result):
                # check if n in the graph
                if not record['n_id'] in id_name_dic.keys():
                    temp_dic = {}
                    curr_property, curr_label = record['n_properties'], record['n_labels']
                    name = get_property_name(curr_property)
                    temp_dic.update({'id': name})
                    key = curr_label[0].upper()
                    temp_dic.update({'group': group[key]})
                    id_name_dic.setdefault(record['n_id'], name)
                    temp_dic.update({'_id': record['n_id']})
                    # append node
                    data_dic['nodes'].append(temp_dic)
                # check if m in the graph

                if not record['m_id'] in id_name_dic.keys():
                    temp_dic = {}
                    curr_property, curr_label = record['m_properties'], record['m_labels']
                    name = get_property_name(curr_property)
                    temp_dic.update({'id': name})
                    key = curr_label[0].upper()
                    temp_dic.update({'group': group[key]})
                    id_name_dic.setdefault(record['m_id'], name)
                    temp_dic.update({'_id': record['m_id']})
                    data_dic['nodes'].append(temp_dic)
                for r in record['relation']:
                    nodes = r.nodes
                    source, target, rel = nodes[0], nodes[1], r.type
                    if not (source.id, target.id) in visited_path and not (target.id, source.id) in visited_path:
                        temp_dic = {}
                        try:
                            temp_dic.setdefault('source', id_name_dic[source.id])
                            temp_dic.setdefault('target', id_name_dic[target.id])
                            temp_dic.setdefault('relation', rel)
                            temp_dic.setdefault('value', 1)
                        except KeyError:
                            raise Exception("key not found")
                        data_dic['links'].append(temp_dic)
                    visited_path.add((source.id, target.id))

        # return HttpResponse(json.dumps(data_dic), content_type="application/json")
        return render(request, self.TEMPLATE, {'data': json.dumps(data_dic)})

    def post(self, request):
        pass
