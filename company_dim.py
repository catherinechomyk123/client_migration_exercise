"""Consolidates and cleans the companies for the company_dim table"""
import pandas as pd


def create_company_dim_table(bus_path: str, con_path: str) -> pd.DataFrame:
    """Creats the company dim table

    Args:
        bus_path (str): Path to the business vertical
        con_path (str): Path to the consumer/health vertical

    Returns:
        pd.DataFrame: Company dimentions table
    """

    # Desired columns for this table
    columns = ["Company Name", "Vertical", "Sub Vertical", "Current Owner", "Business Description"]

    # Reads in business vertical
    b_companies_df = pd.read_excel(bus_path, skiprows=5)
    b_companies_df = b_companies_df[columns]

    # Reads in consumer/health vertical
    c_companies_df = pd.read_excel(con_path, skiprows=8, skipfooter=3) # Foot note in this file
    c_companies_df = c_companies_df.dropna(subset=["Company Name"]) # Drop null company to remove extra rows
    c_companies_df = c_companies_df[columns]

    # Combines the data
    all_companies_df = pd.concat([b_companies_df, c_companies_df])

    # Creares the PK
    all_companies_df.reset_index(inplace=True)
    all_companies_df["Company ID"] = all_companies_df.index + 1

    # Final schema
    columns = ["Company ID", "Company Name", "Vertical", "Sub Vertical", "Business Description", "Current Owner"]
    all_companies_df = all_companies_df[columns]
    return all_companies_df
