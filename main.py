# This is a sample Python script.
import getopt
import math
import re
import sys


def split_on_camel_case(camel_case_string):
    split_string = camel_case_string
    if len(split_string) > 12:
        type_tokens = re.split('(?=[A-Z])', split_string)
        pivot = math.ceil(len(type_tokens) / 2)
        split_string = "".join(type_tokens[:pivot]) + "\n" + "".join(type_tokens[pivot:])
    return split_string


def print_nodes(nodes, ofile):

    node_defs = []
    connections = []

    for node_name in nodes:
        # Define the node
        node = nodes[node_name]

        node_type = node['node_type']
        if len(node_type) > 16:
            node_type = split_on_camel_case(node_type)

        bvar = node['bvar_name']
        if bvar:
            if "_" in bvar:
                bvar = bvar[bvar.index("_") + 1:]

            bvar = split_on_camel_case(bvar)
            node_defs.append("%s [label=\"%s\n\n%s\"];" % (node_name, node_type, bvar))
        else:
            node_defs.append("%s [label=\"%s\"];" % (node_name,  node_type))

        # Now walk any children
        for child_node_name in node['children']:
            connections.append("%s -> %s" % (node_name, child_node_name))

    diag_file = open("%s.diag" % ofile, "w")
    diag_file.write("blockdiag {\n")
    diag_file.write("orientation = portrait;\n")
    diag_file.write("default_fontsize = 10;\n")
    diag_file.write("node_height = 80;\n")

    for bn_def in node_defs:
        diag_file.write("%s\n" % bn_def)
    diag_file.write("\n\n")

    for connection in connections:
        diag_file.write("%s\n" % connection)
    diag_file.write("}\n")
    diag_file.close()


def parse_lines(infile):
    nodes = {}
    with open(infile) as fp:
        lines = fp.read().splitlines()

        for line in lines:
            if " new " in line:
                #  node constructor
                tokens = line.split()
                type_tokens = tokens[4].split("(")
                node_name = tokens[1]
                node_type = type_tokens[0]
                node_label = type_tokens[1][1:-2]
                bvar_name = ''
                if "BehaviorVariableName." in line:
                    bvar_name = line[line.index("BehaviorVariableName.") + 21:-2]

                nodes[node_name] = {'node_type': node_type, 'node_label': node_label, 'bvar_name': bvar_name,
                                    'children': set()}
                print("node name: %s  type: %s  label: %s" % (node_name, node_type, node_label))

            elif "AddChild(" in line:
                # Adding a connection
                parent_node = line[0:line.index(".")]
                child_node = line[line.index("(") + 1:-2]
                print("parent_node: %s  child_node: %s" % (parent_node, child_node))
                nodes[parent_node]['children'].add(child_node)

    return nodes


def parse_opts(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "i:o:h", [])
    except getopt.GetoptError:
        print('btgbtreegrapher.py -h -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('btgbtreegrapher.py -h -i <inputfile> -o <outputfile>')
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg

    if not outputfile:
        outputfile = inputfile

    return inputfile, outputfile


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ifile, ofile = parse_opts(sys.argv[1:])
    nodes = parse_lines(ifile)
    # reversed_nodes = dict(reversed(list(nodes.items())))
    nodes = print_nodes(nodes, ofile)
