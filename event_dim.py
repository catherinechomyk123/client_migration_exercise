"""Generates the event dim table"""
import datetime
import pandas as pd


def create_event_dim_table(excel_path: str) -> pd.DataFrame:
    """Creates the event dim table from the metadata of the events file

    Args:
        excel_path (str): Path to the events file

    Returns:
        pd.DataFrame: An event dim table
    """
    # Initializes the data structure
    event_dim_data = {
        "Event ID": [],
        "Event Name": [],
        "Year": []
        }

    excel = pd.ExcelFile(excel_path)

    # Iterates through the sheet names to get all events
    for idx, sheet in enumerate(excel.sheet_names):
        event_dim_data["Event ID"].append(idx+1)
        try:
            event_dim_data["Year"].append(int(sheet[:4]))
            event_dim_data["Event Name"].append(sheet[4:])
        except ValueError: # If the year is not at the start of the sheet
            # Sets year to the current year
            event_dim_data["Year"].append(datetime.date.today().year)
            # Collects the event name as is
            event_dim_data["Event Name"].append(sheet)

    # Creates the df
    event_dim_df = pd.DataFrame(event_dim_data)
    return event_dim_df