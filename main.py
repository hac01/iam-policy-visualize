import json
import graphviz
import re
import sys

#removes special chars from node name
def clean_node_name(name):
    return re.sub(r"[^a-zA-Z0-9_]+", "_", name)


def visualize_iam_policy(json_data, output_file='iam_policy_graph'):
    try:
        iam_policy = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return

    dot = graphviz.Digraph(comment='IAM Policy Graph', format='png', graph_attr={'bgcolor': '#212121', 'rankdir': 'LR', 'fontcolor': 'white'})
# Adds nodes and edges for each binding in IAM policy

    for binding in iam_policy.get('bindings', []):
        role = binding.get('role', 'unknown_role')
        for member in binding.get('members', []):
            if member.startswith('serviceAccount:'):
                member_node = clean_node_name(member)
                dot.node(member_node, shape='box', style='filled', color='#1565C0', fontcolor='white', height='0.6')
                dot.edge(member_node, role, color='#4CAF50', style='dashed', penwidth='1.2')
            elif member.startswith('user:'):
                member_node = clean_node_name(member)
                dot.node(member_node, shape='ellipse', style='filled', color='#FFD54F', fontcolor='#212121', height='0.6')
                dot.edge(member_node, role, color='#4CAF50', style='dashed', penwidth='1.2')
            else:
                member_node = clean_node_name(member)
                dot.node(member_node, shape='box', style='filled', color='#2E7D32', fontcolor='white', height='0.6')
                dot.edge(member_node, role, color='#4CAF50', style='dashed', penwidth='1.2')

        role_node = clean_node_name(role)
        dot.node(role_node, shape='box', style='filled', color='#2E7D32', fontcolor='white', height='0.6')

    dot.render(output_file, cleanup=True)

    print(f"IAM Policy visualization saved as {output_file}.png")

#takes json file as input
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
