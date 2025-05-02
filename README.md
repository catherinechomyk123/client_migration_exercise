# Client Migration Exercise

## How to Use

- Install dependencies from poetry
- run the script transform_to_model

## Data model

![Data Model](EDA/data_model.png)

## Additional Enhancements

- Create the PE Prortfolio table
- Enrich the contact table with the contacts from PE and the Consumer Vertical
    - Deals is missing data do to lack of contacts
- Refine Data model
    - Make it more normalized
    - AUM in the finance table
    - Combine firm dim and company dim
    - Finance metrics can be at a day/month level
- Make sure all data types are accurate
- Business Description work
    - Analyze and create a list that encompasses all business descriptions
    - Confirm the list
    - Sub out the string with the list
