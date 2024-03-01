def recursion(folder_dict, path_list, function):
    head, *tail = path_list
    if 1 < len(path_list):
        if head not in folder_dict:
            folder_dict[head] = recursion({}, tail, function)
        else:
            folder_dict[head].update(recursion(folder_dict[head], tail, function))
    else:
        return {head: function}
