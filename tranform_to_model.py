"""Transforms all data files into the new data model"""
from event_dim import create_event_dim_table
from contacts import create_contact_table
from marketing_participants import create_market_participant_table


EVENT_PATH = "data\Events.xlsx"
CONTACT_PATH = "data\Contacts.xlsx"

if __name__ == "__main__":

    # Creates the event dim table
    event_dim_df = create_event_dim_table(EVENT_PATH)

    # Creates the contact table
    contacts_df = create_contact_table(CONTACT_PATH) #TODO: Will be updated later for enrichment

    # Creates the marketing and participant table
    marketing_df = create_market_participant_table(EVENT_PATH, contacts_df)

    #TODO: Other tables will go here

    # Outputs the tables to an excel sheet
    event_dim_df.to_excel("new data model\event_dim.xlsx", index=False)
    contacts_df.to_excel("new data model\contacts.xlsx", index=False)
    marketing_df.to_excel("new data model\marketing_participants.xlsx", index=False)