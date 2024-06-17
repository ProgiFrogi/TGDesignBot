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
        lst = []
        self.__search__(self.root, parent, lst)
        if len(lst) == 0:
            raise Exception("Target node does not exist")
        lst[0].children.append(self.Node(data))

    # Delete the node and it's children by name.
    def delete_node(self, name: str):
        lst = []
        self.__get_parent__(self.root, name, lst)
        if len(lst) == 0:
            return
        delete_node = [x for x in lst[0].children if x.name == name]
        lst[0].children.remove(delete_node[0])

    # Checking is node is leaf of tree.
    def is_leaf(self, name: str) -> bool:
        return len(self.get_children(name)) == 0

    # Get a list of children's names
    def get_children(self, name: str) -> list:
        children_list = []
        lst = []
        self.__search__(self.root, name, lst)
        for node in lst[0].children:
            children_list.append(node.name)
        return children_list

    # Return name of parent of target node.
    def get_parent(self, name: str) -> str:
        lst = []
        self.__get_parent__(self.root, name, lst)
        if len(lst) == 0:
            raise Exception("No such node")
        else:
            return lst[0].name

    def exist(self, name: str) -> bool:
        lst = []
        self.__search__(self.root, name, lst)
        return len(lst) != 0

    # Searching target Node in tree. If node doesn't exist return fake node with name = 'None'
    def __search__(self, node: Node, target: str, lst: list):
        if target == 'root':
            lst.append(self.root)
            return
        for children in node.children:
            if children.name == target:
                lst.append(children)
                return
            else:
                self.__search__(children, target, lst)

    def __get_parent__(self, node: Node, target: str, lst: list):
        for children in node.children:
            if children.name == target:
                lst.append(node)
            else:
                self.__get_parent__(children, target, lst)