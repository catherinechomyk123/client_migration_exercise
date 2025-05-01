"""Consolidates and cleans up all contacts into the contacts table

Key assumptions:
    If there is no commas in the City column, it is a country outside of the US
"""
import pandas as pd
import numpy as np


def create_contact_table(excel_path: str, firm_df: pd.DataFrame, con_path: str) -> pd.DataFrame:
    """Consolidates and cleans the contact table

    Args:
        excel_path (str): Path to the contact table
        firm_df (pd.DataFrame): Firm dimention table

    Returns:
        pd.DataFrame: PE and Banking contacts
        # TODO: Need to enrich the data with PE firms and banks found in the consumer vertical
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

    all_contacts = map_firm_id(all_contacts, firm_df)

    return all_contacts

def map_firm_id(contacts_df: pd.DataFrame, firm_df: pd.DataFrame) -> pd.DataFrame:
    """Maps the firms id to the table

    Args:
        contacts_df (pd.DataFrame): The contacts data
        firm_df (pd.DataFrame): The firm dimention table

    Returns:
        pd.DataFrame: _description_
    """
    contacts_firm_id = pd.merge(contacts_df,firm_df, on="Firm", how="left")
    columns = ["Contact ID", "Firm ID", "Name", "Title", "Group", "Sub-Vertical", "E-mail", "Phone",
                "Secondary Phone", "Country", "State", "City", "Birthday", "Coverage Person",
                "Preferred Contact Method"]
    contacts_df = contacts_firm_id[columns]
    return contacts_df



def enrich_contacts(contacts_df: pd.DataFrame, con_path:str) -> pd.DataFrame:
    # Reads in consumer/health vertical
    c_companies_df = pd.read_excel(con_path, skiprows=8, skipfooter=3) # Foot note in this file
    c_companies_df = c_companies_df.dropna(subset=["Company Name"]) # Drop null company to remove extra rows
    columns = ['Invest. Bank', 'Banker', 'Banker Email', 'Banker Phone Number']
    c_companies_df = c_companies_df[columns]
    c_companies_df = c_companies_df.dropna(subset=["Invest. Bank"])
    c_companies_df["Invest. Bank"] = c_companies_df["Invest. Bank"].str.replace(";", "")
    c_companies_df[["Invest. Bank 1", "Invest. Bank 2"]] = c_companies_df["Invest. Bank"].str.split(",", expand = True)
    print(c_companies_df)