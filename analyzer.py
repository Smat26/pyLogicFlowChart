import ast
import astunparse
from graphviz import Digraph
import argparse


class Analyzer(ast.NodeVisitor):

    def __init__(self):
        self.root = None
        self.graph = Digraph('conditional_logic_flow', filename='flowchart.gv', strict=True)
        self.graph.attr('node', shape='box', style='rounded', ratio='compress', size='900,900')
        self.graph.node('start')
        self.variable_of_interest = None
        self.action = None

    def if_handler(self, node, parent_node):
        if parent_node.body[0] == node:
            condition = 'Yes'
        else:
            condition = 'No'
        return "if {}".format(astunparse.unparse(parent_node.test)[:-1]), condition

    def for_handler(self, node):
        target_var = astunparse.unparse(node.target)[:-1]
        iterant = astunparse.unparse(node.iter)[:-1]
        return 'for {} in {}:'.format(target_var, iterant)

    def node_printer(self, node, parent_node):
        if isinstance(parent_node, ast.FunctionDef):
            return 'function {}'.format(parent_node.name), ''
        elif isinstance(parent_node, ast.If):
            return self.if_handler(node, parent_node)
        elif isinstance(parent_node, ast.For):
            return self.for_handler(parent_node)
        elif isinstance(parent_node, ast.Expr):
            return ast.dump(parent_node), ''
        elif isinstance(parent_node, ast.Module):
            return 'Module', ''
        else:
            return str(parent_node), ''

    def link_parent(self, tree):
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

    def visit_Call(self, node):
        if 'append()' in self.action:
            if args.has_self:
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Attribute) and node.func.attr == 'append':
                        if node.func.value.value.id == 'self' and node.func.value.attr == target:
                            list_value = astunparse.unparse(node.args[0])
                            self.save_up(node.parent, list_value)
                            return
            else:
                if isinstance(node.func.value, ast.Name) and node.func.attr == 'append':
                    if node.func.value.id == target:
                        list_value = astunparse.unparse(node.args[0])
                        self.save_up(node.parent, list_value)

    def visit_Subscript(self, node):
        if '[]' in self.action:
            if isinstance(node.value, ast.Name) and node.value.id == 'd':
                d_value = astunparse.unparse(node.parent)
                self.save_up(node.parent, d_value)

    def save_up(self, node, leaf_node_val):
        line = [node]
        indent = '\t'
        last_node_value = leaf_node_val
        while hasattr(node, 'parent'):
            if isinstance(node.parent, ast.ClassDef):
                break
            if hasattr(node.parent, 'childern'):
                node.parent.childern.add(node)
            else:
                node.parent.childern = {node}
            line.append(node.parent)
            node_value, node_edge = self.node_printer(node, node.parent)
            self.graph.edge(node_value, last_node_value, label=node_edge)
            node = node.parent
            last_node_value = node_value
            indent += '\t'
        self.graph.edge('start', last_node_value)

    def report(self):
        self.graph.view()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Params for CodeLogicFlow')
    parser.add_argument('-s', '--source', type=str,
                        help="Path of the target python file to visualize")
    parser.add_argument('-v', '--variable-of-interest', type=str,
                        help='variable of interest in the given target file')
    parser.add_argument('-a', '--action-of-interest', choices=['dict-add', 'list-append'],
                        help='The action of interest that the variable does')
    parser.add_argument('-c', '--has-self', action='store_true',
                        help='Specifies variable of interest is a class variable')

    args = parser.parse_args()
    target = args.variable_of_interest
    if args.has_self:
        target = 'self' + target
    if args.action_of_interest == 'dict-add':
        action = '[]'
    elif args.action_of_interest == 'list-append':
        action = 'append()'

    with open(args.source, "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.variable_of_interest = target
    analyzer.action = action
    analyzer.link_parent(tree)
    analyzer.visit(tree)
    analyzer.report()
