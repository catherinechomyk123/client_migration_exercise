"""Creates the deal table"""
import pandas as pd
import numpy as np


def create_deal_table(bus_path:str, con_path:str, firm_dim_df: pd.DataFrame,
                       contacts_df: pd.DataFrame, company_df: pd.DataFrame) -> pd.DataFrame:
    """Creates the deals table across both verticals

    Args:
        bus_path (str): Path to the business vertical
        con_path (str): Path to the consumer retail/health vertical
        firm_dim_df (pd.DataFrame): Firm dimentions table
        contacts_df (pd.DataFrame): Contacts table
        company_df (pd.DataFrame): Company dimentions table

    Returns:
        pd.DataFrame: All the deals for both verticalls
    """

    # Reads in the bus vertical
    b_companies_df = pd.read_excel(bus_path, skiprows=5)
    columns = ["Company Name", "Project Name", "Date Added", "Invest. Bank", "Banker",
        "Sourcing", "Transaction Type", "Status"]
    b_companies_df = b_companies_df[columns]

    # Prepping data for transformation
    b_companies_df["Date Added"] = b_companies_df["Date Added"].astype(str)
    b_companies_df["Date Added"] = b_companies_df["Date Added"].apply(lambda row: row.split(" ")[0])

    month_mapping = {
        "Apr": "04",
        "Dec": "12",
        "Mar": "03",
        "Nov": "11",
        "Feb": "02",
        "Jan": "01",
        "Oct": "10",
        "Sep": "07",
        "May": "05",
        "Jul": "06",
        "null":"00"
    }
    # Split year month and day
    b_companies_df["Date Added"] = b_companies_df["Date Added"] .apply(lambda row: fr"-{row}" if len(row) == 6 else row )
    b_companies_df[["Year", "Month", "Day"]] = b_companies_df["Date Added"].str.split("-", expand=True)
    b_companies_df["Month"] = b_companies_df["Month"].apply(lambda row: month_mapping.get(row[:3].title(), row.zfill(2)) if pd.notnull(row) and len(row) ==3 else row) # There is a null date

    # Adds columns for the con vertical
    b_companies_df["Active Stage"] = np.nan
    b_companies_df["Passed Rationale"] = np.nan

    # Reads in consumer/health vertical
    c_companies_df = pd.read_excel(con_path, skiprows=8, skipfooter=3) # Foot note in this file
    c_companies_df = c_companies_df.dropna(subset=["Company Name"]) # Drop null company to remove extra rows

    # Split year month and day
    c_companies_df["Year"] = c_companies_df["Date Added"].dt.year
    c_companies_df["Month"] = c_companies_df["Date Added"].dt.month
    c_companies_df["Day"] = c_companies_df["Date Added"].dt.day

    # Selects the final columns
    columns = ["Company Name", "Project Name", "Year", "Month", "Day", "Invest. Bank", "Banker",
        "Sourcing", "Transaction Type", "Status", "Active Stage", "Passed Rationale"]
    c_companies_df = c_companies_df[columns]

    # Unions the verticals
    deals_df = pd.concat([b_companies_df, c_companies_df])
    deals_df[["Invest. Bank 1", "Invest. Bank 2"]] = deals_df["Invest. Bank"].str.split(",", expand = True)

    # Substitutes the FK
    deals_df = pd.merge(deals_df, firm_dim_df, left_on="Invest. Bank 1", right_on="Firm", how="left")
    del deals_df["Invest. Bank 1"]
    deals_df = deals_df.rename(columns={"Firm ID": "Invest. Bank 1"})
    deals_df = pd.merge(deals_df, firm_dim_df, left_on="Invest. Bank 2", right_on="Firm", how="left")
    del deals_df["Invest. Bank 2"]
    deals_df = deals_df.rename(columns={"Firm ID": "Invest. Bank 2"})
    deals_df = pd.merge(deals_df, contacts_df, left_on="Banker", right_on= "Name", how="left")
    del deals_df["Banker"]
    deals_df = deals_df.rename(columns={"Contact ID": "Banker"})
    deals_df = pd.merge(deals_df, company_df, left_on="Company Name", right_on= "Company Name", how="left")


    # Creates the PK
    deals_df.reset_index()
    deals_df["Deal ID"] = deals_df.index + 1
    # Selects the final columns
    columns = ["Deal ID", "Company ID", "Project Name", "Year", "Month", "Day", "Invest. Bank 1", "Invest. Bank 2", "Banker",
        "Sourcing", "Transaction Type", "Status", "Active Stage", "Passed Rationale"]
    deals_df = deals_df[columns]
    return deals_df