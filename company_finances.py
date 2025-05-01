"""Converts company finance data into a historical model"""
import pandas as pd
import numpy as np

# TODO: Need to better modulize
def create_company_finances(bus_path: str, con_path: str, company_dim: pd.DataFrame) -> pd.DataFrame:
    """Creates the finance metrics table for companies

    Args:
        bus_path (str): Path to the business vertical
        con_path (str): Path to the consumer retail/health vertical
        company_dim (pd.DataFrame): Company dimention table

    Returns:
        pd.DataFrame: Company finances per year
    """

    # Reads in the business companies
    b_companies_df = pd.read_excel(bus_path, skiprows=5)
    b_companies_df = pd.merge(b_companies_df, company_dim, on  = "Company Name", how="left")
    
    # Desired columns for this table
    columns = ["Company ID", "2014A EBITDA", "2015A EBITDA", "2016A EBITDA", "2017A/E EBITDA", "2018E EBITDA"]
    b_companies_df = b_companies_df[columns]

    # Unpivots
    unpivot_df = b_companies_df.melt(
                id_vars=["Company ID"],
                value_vars=["2014A EBITDA", "2015A EBITDA", "2016A EBITDA", "2017A/E EBITDA", "2018E EBITDA"],
                var_name="Year",
                value_name="EBITDA"
    )
    unpivot_df["Year"] = unpivot_df["Year"].str.rstrip("EBITDA")

    # Cleaning data
    unpivot_df["EBITDA Type"] = unpivot_df["Year"].str[4:]
    unpivot_df["Year"] = unpivot_df["Year"].str[:4]
    unpivot_df = unpivot_df.dropna()
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].astype(str)
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].apply(lambda row: row.replace("C$", "CAD "))
    # Removed mm - Is all the data in millions?
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].str.replace("mm pre-tax income", "(pre-tax income)")

    # TODO This estimate column can be handled better
    unpivot_df[["EBITDA", "Estimate"]] = unpivot_df["EBITDA"].str.split("(", expand = True)
    unpivot_df["Estimate"] = unpivot_df["Estimate"].str.replace(")", "")
    unpivot_df["Estimate"] = unpivot_df["Estimate"].str.strip()
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].str.replace("$", "")
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].str.strip()

    # Deals with estimates
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].apply(lambda row: str(int(row[0]) + int(row[4:6]) / 2) if "-" in row else row)

    # Gets the currency
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].apply(lambda row: str(f" {row}") if "CAD" not in row else row)
    unpivot_df[["Currency", "EBITDA"]] = unpivot_df["EBITDA"].str.split(" ", expand = True)
    unpivot_df["Currency"] = unpivot_df["Currency"].apply(lambda row: "US" if not row else row)

    unpivot_df["Revenue"] = np.nan # Creates for merge with con table
    unpivot_df["EBITDA"] = unpivot_df["EBITDA"].astype(float) # Converts back to decimal

    # Reads in consumer/health vertical
    columns = ["Company ID", "Date Added", "LTM EBITDA", "LTM Revenue"]
    c_companies_df = pd.read_excel(con_path, skiprows=8, skipfooter=3) # Foot note in this file
    c_companies_df = c_companies_df.dropna(subset=["Company Name"]) # Drop null company to remove extra rows
    c_companies_df = pd.merge(c_companies_df, company_dim, on  = "Company Name", how="left")
    c_companies_df = c_companies_df[columns]

    # Conform to bus vertical
    c_companies_df["Year"] = c_companies_df["Date Added"].dt.year
    c_companies_df["EBITDA Type"] = np.nan
    c_companies_df["Currency"] = "US"
    c_companies_df["Estimate"] = "LTM,Revenue" # Again should be handled different with a better data model
    c_companies_df.rename(columns={"LTM EBITDA": "EBITDA", "LTM Revenue": "Revenue"}, inplace=True)
    
    # Unions them together
    company_finances = pd.concat([unpivot_df,c_companies_df])

    # Calculates enterprise value and estimate equity investment
    # Default right now but need varification on this
    # If the calculation requires transaction types will need to bring that col over temporarily
    # Or I can leave the data as is
    company_finances["Enterprise Value"] = (company_finances["EBITDA"]) * 10
    company_finances["Equity Investment Est."] = (company_finances["Enterprise Value"]) / 2

    company_finances.reset_index()
    company_finances["Finance ID"] = company_finances.index +1
    company_finances = company_finances[["Finance ID", "Company ID", "Year", "Revenue", "EBITDA","Enterprise Value",
                       "Equity Investment Est.", "Currency", "EBITDA Type", "Estimate"]]
    return company_finances