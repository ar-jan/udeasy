import yaml


def export_q(data, dest):
    with open(dest, 'w') as file:
        yaml.safe_dump(data, file)


def import_q(path):
    with open(path) as file:
        data = yaml.safe_load(file)
    if valid_imported(data):
        return data


def valid_imported(data) -> bool:
    # checking if the loaded query is a dict
    if not isinstance(data, dict):
        return False
    # checking if 'features' is present as a key of the query dict
    if 'features' not in data:
        return False
    features = data['features']
    # checking the features and getting the list of nodes
    nodes = valid_features(features)
    if not nodes:
        return False
    if 'relations' not in data or 'positions' not in data:
        return False
    if not valid_relations(data['relations'], nodes):
        return False
    if not valid_positions(data['positions'], nodes):
        print(data['positions'])
        return False
    for k in ['show_conllu', 'show_sent', 'show_trees']:
        if k not in data:
            return False
        if not isinstance(data[k], bool):
            return False
    return True


def valid_features(features) -> list:
    """
    This function checks the features dict imported from the yaml file and
    returns the list of nodes names if it is well formed, otherwise it
    returns an empty list

    Arguments:
    features: the features dict

    Returns:
    list: the list of nodes if features is a well formed dict, an empty list
    otherwise
    """
    # checking if features is a dict
    if not isinstance(features, dict):
        return []
    # checking if features is empty
    if not features:
        return []
    nodes = []
    # loop through nodes
    for n in features:
        # check if the node key is a string and if it has a dict as value
        if not isinstance(n, str) or not isinstance(features[n], dict):
            return []
        nodes.append(n)
        # check if the optional key is in the node dict
        if 'optional' not in features[n]:
            return []
    # return the list of nodes
    return nodes


def valid_relations(relations, nodes) -> bool:
    """
    This function checks whether the relation list contains valid dicts in
    which the values are the ones contained in the nodes list

    Arguments:
    relations: the relations list
    nodes: the list containing the name of the nodes

    Returns:
    bool: whether is a valid list or not
    """
    if '' not in nodes:
        nodes.append('')
    # return false if relations is not a list
    if not isinstance(relations, list):
        return False
    for element in relations:
        # return false if an element in the relation list is not a dict
        if not isinstance(element, dict):
            return False
        # otherwise, check what's inside the dict
        try:
            n1 = element['node1']
            n2 = element['node2']
            rel = element['rel']
            # return false if the nodes are not in the nodes list
            if n1 not in nodes or n2 not in nodes:
                return False
            # return false if the value of rel is not a str
            if not isinstance(rel, str):
                return False
        # return false if the dict does not contain these keys
        except KeyError:
            return False
    return True


def valid_positions(positions, nodes) -> bool:
    """
    This function checks whether the position list contains valid dicts in
    which the values are the ones contained in the nodes list

    Arguments:
    positions: the positions list
    nodes: the list containing the name of the nodes

    Returns:
    bool: whether is a valid list or not
    """
    if '' not in nodes:
        nodes.append('')
    # return false if positions is not a list
    if not isinstance(positions, list):
        return False
    for element in positions:
        # return false if an element in the positions list is not a dict
        if not isinstance(element, dict):
            return False
        # otherwise, check what's inside the dict
        try:
            n1 = element['node1']
            n2 = element['node2']
            element['rel']
            element['by']
            element['dist']
            # return false if the nodes are not in the nodes list
            if n1 not in nodes or n2 not in nodes:
                return False
        # return false if the dict does not contain these keys
        except KeyError:
            return False
    return True


if __name__ == '__main__':
    print(import_q('/home/luca/udeasy/test_query.yaml'))
