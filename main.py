import json
import graphviz
import re
import sys
import os

def clean_node_name(name):
    """Remove special characters from node name."""
    return re.sub(r"[^a-zA-Z0-9_]+", "_", name)

def add_node(dot, node_name, shape='box', color='#81C784', fontcolor='#1A4876'):
    """Add a node with specified attributes to the graph."""
    dot.node(node_name, shape=shape, style='filled', color=color, fontcolor=fontcolor, height='0.6')

def add_edge(dot, source, target, color='#4CAF50'):
    """Add an edge with specified attributes to the graph."""
    dot.edge(source, target, color=color, style='dashed', penwidth='1.2')

def visualize_iam_policy(iam_policy, output_file='iam_policy_graph'):
    try:
        iam_policy = json.loads(iam_policy)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return

    dot = graphviz.Digraph(comment='IAM Policy Graph', format='png', graph_attr={'bgcolor': '#F2F2F2', 'rankdir': 'LR'})

    for binding in iam_policy.get('bindings', []):
        role = binding.get('role', 'unknown_role')
        for member in binding.get('members', []):
            member_node = clean_node_name(member)

            if member.startswith('serviceAccount:'):
                add_node(dot, member_node, shape='box', color='#64B5F6')
            elif member.startswith('user:'):
                add_node(dot, member_node, shape='ellipse', color='#FFD54F')
            else:
                add_node(dot, member_node, color='#81C784')

            add_edge(dot, member_node, clean_node_name(role))

        add_node(dot, clean_node_name(role))

    output_path = os.path.join(os.path.dirname(__file__), f"{output_file}")
    dot.render(output_path, cleanup=True)

    print(f"IAM Policy visualization saved as {output_path}.png")

def main(file_path):
    try:
        with open(file_path, 'r') as file:
            iam_policy_json = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    visualize_iam_policy(iam_policy_json, output_file='iam_policy_graph')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 code.py /path/to/iam.json")
    else:
        main(sys.argv[1])
