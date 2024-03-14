import csv
from bs4 import BeautifulSoup


def load_graphml_nodes(file_path):
    """Load nodes from a GraphML file."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        soup = BeautifulSoup(file, "xml")  # Using "xml" parser for handling XML files

    nodes = soup.find_all("node")
    dict_nodes = {}
    for node in nodes:
        data_element = node.find("data", key="d4")
        if data_element:
            label_text = data_element.find("y:Label").find("y:Label.Text").text.strip()
            label_soup = BeautifulSoup(label_text, "html.parser")
            node_name = label_soup.get_text().strip().replace("\n", "")
            node_name = node_name.replace("\ufeff", "").replace("\ufeff", "").replace("\u200b", "")    
            dict_nodes[node["id"]] = node_name

    return dict_nodes


def load_graphml_edges(file_path):
    """Load edges from a GraphML file."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        soup = BeautifulSoup(file, "xml")  

    edges = soup.find_all("edge")
    dict_edges = {}
    for edge in edges:
        data_element = edge.find("data", key="d11")
        if data_element:
            label_text = data_element.find("y:Label").find("y:Label.Text").text.strip()
            label_soup = BeautifulSoup(label_text, "html.parser")
            edge_name = label_soup.get_text().strip().replace("\n", "")
            edge_name = edge_name.replace("\ufeff", "").replace("\ufeff", "").replace("\u200b", "")      
            dict_edges[edge["id"]] = edge_name

    return dict_edges


def load_mapping_csv(file_path):
    """Load a mapping table from a CSV file."""
    abstraction_nodes = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            abstraction_node = row.get('Abstraction Node', '').strip() 
            if abstraction_node:  
                abstraction_nodes.append(abstraction_node)
    return abstraction_nodes


def combine_abstraction_nodes(csv_files):
    """Combine abstraction nodes from multiple CSV files into a single list."""
    combined_nodes = []
    for file_path in csv_files:
        abstraction_nodes = load_mapping_csv(file_path)
        combined_nodes.extend(abstraction_nodes)
    return combined_nodes

def load_mapping_csv_edges(file_path):
    """Load a mapping table from a CSV file."""
    abstraction_edges = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            abstraction_edge = row.get('Abstraction Edge', '').strip()  
            if abstraction_edge:  
                abstraction_edges.append(abstraction_edge)
    return abstraction_edges


def combine_abstraction_edges(csv_files):
    """Combine abstraction edges from multiple CSV files into a single list."""
    combined_edges = []
    for file_path in csv_files:
        abstraction_edges = load_mapping_csv_edges(file_path)
        combined_edges.extend(abstraction_edges)
    return combined_edges


def verify_mapping(platform, dict_nodes, dict_edges, all_abstraction_nodes, all_abstraction_edges):
    """Verify the mapping of nodes and edges."""
    print('\n')
    print(platform)
    print("Nodes from Graphml")
    print(dict_nodes)
    print("Edges from Graphml")
    print(dict_edges)
    print("Nodes from the tables")
    print(all_abstraction_nodes)
    print("Edges from the tables")
    print(all_abstraction_edges)
    flag_nodes_found = 0
    for node_name in dict_nodes.values():
        if node_name in all_abstraction_nodes:
            flag_nodes_found += 1
        else:
            print(f"Node name '{node_name}' not found in the list of all abstraction nodes.")

    if flag_nodes_found == len(dict_nodes):
        print("All Nodes are Verified.",platform)

    flag_edges_found = 0
    for edge_name in dict_edges.values():
        if edge_name in all_abstraction_edges:
            flag_edges_found += 1
        else:
            print(f"Edge name '{edge_name}' not found in the list of all abstraction edges.")
    
    if flag_edges_found == len(dict_edges):
        print("All Edges are Verified.",platform)


# AWS
aws_csv_files_nodes = ["AWS/aws_1to1_mapping.csv", "AWS/aws_non_1to1_mapping.csv", "AWS/aws_renamed_nodes.csv"]
aws_csv_files_edges = ["AWS/aws_non_1to1_mapping_edges.csv", "AWS/aws_renamed_edges.csv"]
aws_graphml_file = "AWS/AWS.graphml"


all_aws_abstraction_nodes = combine_abstraction_nodes(aws_csv_files_nodes)
all_aws_abstraction_edges = combine_abstraction_edges(aws_csv_files_edges)


aws_dict_nodes = load_graphml_nodes(aws_graphml_file)
aws_dict_edges = load_graphml_edges(aws_graphml_file)


verify_mapping("AWS", aws_dict_nodes, aws_dict_edges, all_aws_abstraction_nodes, all_aws_abstraction_edges)


# Azure
azure_csv_files_nodes = ["Azure/azure_1to1_mapping.csv", "Azure/azure_non_1to1_mapping.csv", "Azure/azure_renamed_nodes.csv"]
azure_csv_files_edges = ["Azure/azure_1to1_mapping_edges.csv", "Azure/azure_non_1to1_mapping_edges.csv", "Azure/azure_renamed_edges.csv"]
azure_graphml_file = "Azure/Azure.graphml"


all_azure_abstraction_nodes = combine_abstraction_nodes(azure_csv_files_nodes)
all_azure_abstraction_edges = combine_abstraction_edges(azure_csv_files_edges)


azure_dict_nodes = load_graphml_nodes(azure_graphml_file)
azure_dict_edges = load_graphml_edges(azure_graphml_file)


verify_mapping("Azure", azure_dict_nodes, azure_dict_edges, all_azure_abstraction_nodes, all_azure_abstraction_edges)


# Google
google_csv_files_nodes = ["Google/google_1to1_mapping.csv", "Google/google_non_1to1_mapping.csv", "Google/google_renamed_nodes.csv"]
google_csv_files_edges = ["Google/google_1to1_mapping_edges.csv", "Google/google_non_1to1_mapping_edges.csv", "Google/google_renamed_edges.csv"]
google_graphml_file = "Google/Google.graphml"


all_google_abstraction_nodes = combine_abstraction_nodes(google_csv_files_nodes)
all_google_abstraction_edges = combine_abstraction_edges(google_csv_files_edges)


google_dict_nodes = load_graphml_nodes(google_graphml_file)
google_dict_edges = load_graphml_edges(google_graphml_file)


verify_mapping("Google", google_dict_nodes, google_dict_edges, all_google_abstraction_nodes, all_google_abstraction_edges)