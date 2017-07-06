
def group_list(my_list, chunk_size):
    return [my_list[i:i + chunk_size] for i in range(0, len(my_list), chunk_size)]