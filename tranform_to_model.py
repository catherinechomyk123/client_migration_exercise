"""Transforms all data files into the new data model"""
from event_dim import create_event_dim_table



EVENT_PATH = "data\Events.xlsx"


if __name__ == "__main__":

    # Creates the event dim table
    event_dim_df = create_event_dim_table(EVENT_PATH)

    #TODO: Other tables will go here

    # Outputs the table to an excel sheet
    event_dim_df.to_excel("new data model\event_dim.xlsx", index=False)