"""Consolidates and cleans up all contacts into the contacts table

Key assumptions:
    If there is no commas in the City column, it is a country outside of the US
"""
import pandas as pd


def create_contact_table(excel_path: str) -> pd.DataFrame:
    """Consolidates and cleans the contact table

    Args:
        excel_path (str): Path to the contact table

    Returns:
        pd.DataFrame: PE and Banking contacts
        # TODO: Need to enrich the data with PE firms
        # TODO: Need to replace the firm with a firm id
    """
    # Grabs tier 1 contacts and add the tier flag
    t1_df = pd.read_excel(excel_path, sheet_name="Tier 1's")
    t1_df["Tier"] = 1

    # Grabs tier 2 contacts and add the tier flag
    t2_df = pd.read_excel(excel_path, sheet_name="Tier 2's")
    t2_df["Tier"] = 2

    # Unions the data
    all_contacts = pd.concat([t1_df, t2_df])
    # Cretaes the unique id
    all_contacts.reset_index(inplace=True)
    all_contacts["Contact ID"] =  all_contacts.index+1
    # Cleans the name # TODO check if extention is already in title before dropping
    all_contacts[["Name", "Title Extendend"]] = all_contacts["Name"].str.split('(', expand=True)
    # Renames the column to country for processing
    all_contacts.rename(columns={"City": "Country"}, inplace=True)
    # Splits the columns and if there is only one value (e.g. UK) that is the country, otherwise US
    all_contacts[["City", "State"]] = all_contacts["Country"].str.split(",", expand = True)
    all_contacts["Country"] = all_contacts["Country"].apply(lambda row: "US" if "," in row else row)

    return all_contacts