from typing import List, Tuple

def columns_set_overview(my_lists: List[List[str]]) -> Tuple[List[str], List[str], List[List[str]]]:

    # Convert each list of column names to a set for set operations
    sets = [set(lst) for lst in my_lists]

    # Find common columns (intersection across all sets)
    common_columns = list(set.intersection(*sets))

    # Find all columns (union across all sets)
    all_columns = list(set.union(*sets))

    # Find exclusive columns for each list
    exclusive_columns = [
        list(set(all_columns) - s) for s in sets
    ]

    return common_columns, all_columns, exclusive_columns