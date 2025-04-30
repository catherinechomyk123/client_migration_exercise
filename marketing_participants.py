"""Transforms the event table to the marketig participants table"""
import pandas as pd


def create_market_participant_table(excel_path:str, contact_df: pd.DataFrame) -> pd.DataFrame:
    """Creates the marketing participant table

    Args:
        excel_path (str): Path to the events table
        contact_df (pd.DataFrame): The contact table

    Returns:
        pd.DataFrame: The marketing participant table
    """
    # TODO: Do not hard code - for scalability

    #  Gets the first event data
    dinner_df = pd.read_excel(excel_path, sheet_name="Leaders and Partners Dinner")
    dinner_df["Event ID"] = 1 # Sets the FK

    #  Gets the second event data
    recap_df = pd.read_excel(excel_path, sheet_name="2019 Market Re-Cap")
    recap_df["Event ID"] = 2 # Sets the FK

    # Combined the two events
    combined_df = pd.concat([dinner_df, recap_df])
    # Creates the PK
    combined_df.reset_index(inplace=True)
    combined_df["Participant ID"] = combined_df.index + 1
    
    # Adds in the contact id (FK)
    add_contact_id = combined_df.merge(contact_df, on="E-mail", how="left")
    clean_df = add_contact_id[["Participant ID", "Event ID", "Contact ID", "Attendee Status"]]
    return clean_df
