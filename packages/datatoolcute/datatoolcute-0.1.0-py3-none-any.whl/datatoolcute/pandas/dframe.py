import pandas as pd
import Levenshtein

def set_header(
    data: pd.DataFrame,
    header_columns: list[str | int]
):
    
    # check whether the header is already set
    if set(header_columns) == set(data.columns):
        return data

    # find where the header columns is first found as a row on the datafrane
    header_index = data[data.isin(header_columns).sum(axis=1) == len(header_columns)].index[0]
    # set this row as the header
    data.columns = data.loc[header_index]
    # drop the rows before the header and then reset index
    return data.loc[header_index + 1:].reset_index(drop=True)

def levenshtein_on_list(words_list: list[str], template: str, cutoff: float = 0.7):
    return sorted(list(words_list), key=lambda column: Levenshtein.ratio(column, template, score_cutoff=cutoff))

def reduce_synonyms(
    data: pd.DataFrame,
    base_column: str,
    synonyms: list[str],
    cutoff: float = 0.7
) -> pd.DataFrame:
    
    # Check if the base column already exists in the DataFrame
    if base_column in data.columns:
        return data

    # Find the closest match from the synonyms list to the columns in the DataFrame
    close_match = levenshtein_on_list(data.columns, base_column)[-1]
    
    # If a close match is found, rename the closest column to the base_column
    if close_match:
        data = data.rename(columns={close_match[0]: base_column})
    else:
        # If no exact or close match is found in the column names, search through synonyms
        for synonym in synonyms:
            close_match = levenshtein_on_list(data.columns, synonym)[-1]
            if close_match:
                data = data.rename(columns={close_match[0]: base_column})
                break

    return data

def drop_all_columns_with_repeated_names(df: pd.DataFrame) -> pd.DataFrame:
    
    # Get a count of all column names
    column_counts = df.columns.value_counts()
    
    # Identify columns that appear more than once
    duplicate_columns = column_counts[column_counts > 1].index
    
    # Drop all columns that are duplicates
    df = df.drop(columns=duplicate_columns)
    
    return df

if __name__ == '__main__':
    import pandas as pd

    # Create the initial DataFrames
    df_1 = pd.DataFrame({
        'Key': [1, 2, 3, 4, 5],
        'School': ['A', 'B', 'B', 'C', 'D'],
        'Motive': ['Laziness', 'Laziness', 'Laziness', 'Laziness', 'Laziness']
    })
    df_1['Date'] = '30.09.2023'

    df_2 = pd.DataFrame({
        'Key': [1, 2, 3, 4],
        'School': ['A', 'B', 'B', 'C'],
        'Motive': ['Weakness', 'Laziness', 'Weakness', 'Laziness']
    })
    df_2['Date'] = '30.10.2023'

    df_3 = pd.DataFrame({
        'Key': [3, 4],
        'School': ['B', 'C'],
        'Motive': ['Weakness', 'Weakness']
    })
    df_3['Date'] = '30.11.2023'

    # Combine the DataFrames into a single DataFrame with Date column
    combined_df = pd.concat([df_1, df_2, df_3])

    # Pivot the combined DataFrame to get the desired structure
    result = combined_df.pivot_table(
        index=['Key', 'School'],
        columns='Date',
        values='Motive',
        aggfunc='first'  # Use 'first' to handle duplicate values if any
    ).reset_index()

    # Sort columns for better readability (optional)
    result = result.sort_index(axis=1)

    print(result)