"""Transforms all data files into the new data model"""
from event_dim import create_event_dim_table
from contacts import create_contact_table
from marketing_participants import create_market_participant_table
from company_dim import create_company_dim_table
from firm_dim import create_firm_dim_table
from company_finances import create_company_finances
from deals import create_deal_table

EVENT_PATH = "data\Events.xlsx"
CONTACT_PATH = "data\Contacts.xlsx"
BUSINESS_VERTICAL_PATH = "data\Business Services Pipeline.xlsx"
CONSUMER_HEALTH_VERTICAL_PATH = "data\Consumer Retail and Healthcare Pipeline.xlsx"
PE_PATH = "data\PE Comps.xlsx"

if __name__ == "__main__":

    # Creates the company dim table
    company_dim_df = create_company_dim_table(BUSINESS_VERTICAL_PATH, CONSUMER_HEALTH_VERTICAL_PATH)

    # Creates the event dim table
    event_dim_df = create_event_dim_table(EVENT_PATH)

    # Create the firm dim table
    firm_dim_df = create_firm_dim_table(CONTACT_PATH, PE_PATH)

    # Creates the contact table
    contacts_df = create_contact_table(CONTACT_PATH, firm_dim_df, CONSUMER_HEALTH_VERTICAL_PATH)

    # Creates the marketing and participant table
    marketing_df = create_market_participant_table(EVENT_PATH, contacts_df)

    # Creates the finance table
    finance_df = create_company_finances(BUSINESS_VERTICAL_PATH, CONSUMER_HEALTH_VERTICAL_PATH, company_dim_df)

    # Creates the deals table
    deal_df = create_deal_table(BUSINESS_VERTICAL_PATH, CONSUMER_HEALTH_VERTICAL_PATH, firm_dim_df, contacts_df, company_dim_df)

    # Outputs the tables to an excel sheet
    company_dim_df.to_excel(r"new data model\company_dim.xlsx", index=False)
    event_dim_df.to_excel(r"new data model\event_dim.xlsx", index=False)
    contacts_df.to_excel(r"new data model\contacts.xlsx", index=False)
    marketing_df.to_excel(r"new data model\marketing_participants.xlsx", index=False)
    firm_dim_df.to_excel(r"new data model\firm_dim.xlsx", index=False)
    finance_df.to_excel(r"new data model\company_finances.xlsx", index=False)
    deal_df.to_excel(r"new data model\deals.xlsx", index=False)