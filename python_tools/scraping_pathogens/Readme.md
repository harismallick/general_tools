## Scraping government documentation to identity pathogens that need to be screened prior to DNA synthesis.

### Links
1. [UK Gov link 1](https://www.legislation.gov.uk/ukpga/2001/24/schedule/5#commentary-c19544061)
2. [UK Gov link 2](https://www.legislation.gov.uk/uksi/2008/944/schedule/1/made)

### How to do this?
1. Scrape the websites for the list of pathogens mentioned.
2. Fuzzy match the new list to the existing RPD to find the differences.
3. Those that don't exist in the RPD are new entries. Search for their taxID in the NCBI db.

