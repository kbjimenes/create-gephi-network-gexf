###########################################################################################
# Date: 18/04/2019
# Script to create a network graph with Gephi
# Author: kbjimenes
###########################################################################################

#Libraries
import pandas as pd 
import xml.etree.ElementTree as ET

#Files
EDGE_LIST_FILE = "edge_list.csv"
NODE_ATTRIBUTES = "node_attributes.csv"
RESULT_XML_FILE="test.gexf"

file_creator = "kbjimenes"
file_description="Network graph"

# @Read file as a data frame
# Attributes
# @file_name : csv file
# @sep_tab : separator
def read_file_as_dataframe(file_name, sep_tab): 
    df = pd.read_csv(file_name, sep=sep_tab)
    return df

# @Generate node attributes
# Attributes
# @graph : xml object
# @node_attributes_dt : node attributes file dataframe
def generate_node_attributes(graph, node_attributes_dt):
	columns = list(node_attributes_dt.columns)
	node_attributes = ET.SubElement(graph, 'attributes')
	node_attributes.set('class', 'node')
	k=0
	for i in range(2, len(columns)):
		node_attribute = ET.SubElement(node_attributes, 'attribute')
		node_attribute.set('id', str(k))
		node_attribute.set('title', columns[i])
		node_attribute.set('type', "string")
		k=k+1
	return graph

# @Generate nodes
# Attributes
# @graph : xml object
# @node_attributes_dt : node attributes file dataframe
def generate_nodes(graph, node_attributes_dt):
	columns = list(node_attributes_dt.columns)
	nodes = ET.SubElement(graph, 'nodes')
	for index, row in node_attributes_dt.iterrows():
		node = ET.SubElement(nodes, 'node')
		node.set('id', str(row['N']))
		node.set('label', str(row['NAME']))	
		attvalues = ET.SubElement(node, 'attvalues')
		k=0
		for i in range(2, len(columns)):
			attvalue = ET.SubElement(attvalues, 'attvalue')
			attvalue.set("for", str(k))
			attvalue.set("value", str(row['CATEGORY']))
			k=k+1
	return graph

# @Generate edges
# Attributes
# @graph : xml object
# @edge_list_dt : edge list file dataframe
def generate_edges(graph, edge_list_dt):
	print(edge_list_dt.head())
	edges = ET.SubElement(graph, 'edges')
	for index, row in edge_list_dt.iterrows():
		edge = ET.SubElement(edges, 'edge')
		edge.set('id', str(index))
		edge.set('source', str(row['N1']))
		edge.set('target', str(row['N2']))
		edge.set('weight', str(row['weight']))
	return graph

# create a new XML file with the results
# Attributes
# @graph : xml object
def save_graph_file(gexf):
	str_gexf = ET.tostring(gexf, encoding='utf8', method='xml').decode()
	myfile = open(RESULT_XML_FILE, "w")
	myfile.write(str_gexf)


# @Generate GEXF file
# Attributes
# @node_attributes_dt : node attributes file dataframe
# @edge_list_dt : edge list file dataframe
def generate_file(node_attributes_dt, edge_list_dt):
	# create the file structure
	gexf = ET.Element('gexf')
	gexf.set('xmlns', 'http://www.gexf.net/1.2draft')
	gexf.set('version', '1.2')
	#meta
	meta = ET.SubElement(gexf, 'meta')
	creator=ET.SubElement(meta, 'creator')
	creator.text=file_creator
	description=ET.SubElement(meta, 'description')
	description.text=file_description

	graph = ET.SubElement(gexf, 'graph')
	graph.set('mode', 'static')
	graph.set('defaultedgetype', 'directed')

	graph = generate_node_attributes(graph, node_attributes_dt)
	graph = generate_nodes(graph, node_attributes_dt)

	graph = generate_edges(graph, edge_list_dt)

	save_graph_file(gexf)

if __name__ == "__main__":

	edge_list_dt = read_file_as_dataframe(EDGE_LIST_FILE, ",")
	node_attributes_dt = read_file_as_dataframe(NODE_ATTRIBUTES, ",")
	generate_file(node_attributes_dt, edge_list_dt)