from Repo.TGDesignBot.main.DBHandler.select_scripts import \
    get_templates_from_child_directories as get_templates_from_child_directories
from Repo.TGDesignBot.main.DBHandler.delete_scripts import delete_template as delete_template


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
        remove_lst = self.get_templates_from_child_directories(lst[0].name)
        for remove_template in remove_lst:
            self.delete_template(remove_template[0])

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

    # Take a name of directory and checking if this directory exists in tree.
    def exist(self, name: str) -> bool:
        lst = []
        self.__search__(self.root, name, lst)
        return len(lst) != 0

    # Searching target Node in tree. If node doesn't exist returns empty list.
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

    # Utility function to searching parent of target Node in tree.
    # Takes current Node, children name (target) and list there need to save answer.
    def __get_parent__(self, node: Node, target: str, lst: list):
        for children in node.children:
            if children.name == target:
                lst.append(node)
            else:
                self.__get_parent__(children, target, lst)
