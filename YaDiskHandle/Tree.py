class Tree:
    # Inner class Node. Have 2 fields: name and an array of children.
    class Node:
        def __init__(self, data: str):
            self.name = data
            self.children = []

        def __del__(self):
            for child in self.children:
                self.children.remove(child)

    def __init__(self):
        self.root = self.Node('root')

    # Insert new node to tree. Takes the name of parent node and value - name of child.
    def insert(self, parent: str, data: str):
        target_node = self.__search__(self.root, parent)
        if target_node.name == 'None':
            raise Exception("Target node does not exist")
        target_node.children.append(self.Node(data))

    # Delete the node and it's children by name.
    def delete_node(self, name: str):
        parent = self.__get_parent__(self.root, name)
        if parent.name == 'None':
            return
        delete_node = [x for x in parent.children if x.name == name]
        parent.children.remove(delete_node[0])

    # Get a list of children's names
    def get_children(self, name: str) -> list:
        children_list = []
        for node in self.__search__(self.root, name).children:
            children_list.append(node.name)
        return children_list

    # Return name of parent of target node.
    def get_parent(self, name: str) -> str:
        target = self.__get_parent__(self.root, name).name
        if target == 'None':
            raise Exception("No such node")
        else:
            return target

    def exist(self, name: str) -> bool:
        return self.__search__(self.root, name).name != 'None'

    # Searching target Node in tree. If node doesn't exist return fake node with name = 'None'
    def __search__(self, node: Node, target: str) -> Node:
        if target == 'root':
            return self.root
        for children in node.children:
            if children.name == target:
                return children
            else:
                return self.__search__(children, target)
        else:
            return self.Node('None')

    def __get_parent__(self, node: Node, target: str) -> Node:
        for children in node.children:
            if children.name == target:
                return node
            else:
                return self.__get_parent__(children, target)
        else:
            return self.Node('None')
