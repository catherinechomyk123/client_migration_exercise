"""Creates the firm dimention table"""
import pandas as pd



def create_firm_dim_table(bank_firms_path: str, pe_firms_path: str) -> pd.DataFrame:
    """Creates the firm dim table

    Args:
        bank_firms_path (str): Path to the content table
        pe_firms_path (str): Path to the PE table

    Returns:
        pd.DataFrame: Consolidated firm dim table
    """

    # Reads in the banking tier 1 firms
    finance_firms_t1 = pd.read_excel(bank_firms_path, sheet_name="Tier 1's")
    finance_firms_t1 = finance_firms_t1[["Firm"]]
    finance_firms_t1["Firm Type"] = "Investment Bank" # Sets the type to banking

    # Reads in the banking tier 2 firms
    finance_firms_t2 = pd.read_excel(bank_firms_path, sheet_name="Tier 2's")
    finance_firms_t2 = finance_firms_t2[["Firm"]]
    finance_firms_t2["Firm Type"] = "Investment Bank" # Sets the type to banking

    # Reads in the pe firms
    full_pe_firms = pd.read_excel(pe_firms_path, skiprows=2) # Headers at 2 data at 4 (not date enineering stats)
    full_pe_firms = full_pe_firms.drop(index=0) # Is this the standard? - Extra row
    pe_firms = full_pe_firms[["Company Name"]].rename(columns={"Company Name": "Firm"})
    pe_firms["Firm Type"] = "Private Equity" # Sets the type to PE

    # Joines the tables and gets the uniue firm naems
    all_firms = pd.concat([finance_firms_t1, finance_firms_t2, pe_firms])
    unique_firms = all_firms.drop_duplicates()

    # Enriches The data with AUM and website
    enrichment_df = pd.merge(unique_firms, full_pe_firms, left_on="Firm", right_on="Company Name", how="left")
    enrichment_df.reset_index()
    enrichment_df["Firm ID"] = enrichment_df.index + 1 # Creates the PK
    enrichment_df = enrichment_df[["Firm ID", "Firm", "Firm Type", "AUM\n(Bns)", "Website"]]
    enrichment_df.rename(columns={"AUM\n(Bns)" : "AUM (Bns)"}, inplace=True)

    return enrichment_df
