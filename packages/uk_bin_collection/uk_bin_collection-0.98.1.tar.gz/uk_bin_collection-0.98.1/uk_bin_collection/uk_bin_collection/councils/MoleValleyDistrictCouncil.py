import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from uk_bin_collection.uk_bin_collection.common import *
from uk_bin_collection.uk_bin_collection.get_bin_data import AbstractGetBinDataClass


# import the wonderful Beautiful Soup and the URL grabber
class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def parse_data(self, page: str, **kwargs) -> dict:

        user_postcode = kwargs.get("postcode")
        check_postcode(user_postcode)

        root_url = "https://myproperty.molevalley.gov.uk/molevalley/api/live_addresses/{}?format=json".format(
            user_postcode
        )
        requests.packages.urllib3.disable_warnings()
        response = requests.get(root_url, verify=False)

        if not response.ok:
            raise ValueError("Invalid server response code retreiving data.")

        jsonData = response.json()

        if len(jsonData["results"]["features"]) == 0:
            raise ValueError("No collection data found for postcode provided.")

        properties_found = jsonData["results"]["features"]

        # If UPRN is provided, we can check a specific address.
        html_data = None
        uprn = kwargs.get("uprn")
        if uprn:
            check_uprn(uprn)
            for item in properties_found:
                if uprn == str(int(item["properties"]["blpu_uprn"])):
                    html_data = item["properties"]["three_column_layout_html"]
                    break
            if html_data is None:
                raise ValueError("No collection data found for UPRN provided.")
        else:
            # If UPRN not provided, just use the first result
            html_data = properties_found[0]["properties"]["three_column_layout_html"]

        soup = BeautifulSoup(html_data, features="html.parser")
        soup.prettify()

        data = {"bins": []}
        all_collection_dates = []
        regex_date = re.compile(r".* ([\d]+\/[\d]+\/[\d]+)")
        regex_additional_collection = re.compile(r"We also collect (.*) on (.*) -")

        # Search for the 'Bins and Recycling' panel
        for panel in soup.select('div[class*="panel"]'):
            if panel.h2.text.strip() == "Bins and Recycling":

                # Gather the bin types and dates
                for collection in panel.select("div > strong"):
                    bin_type = collection.text.strip()
                    collection_string = collection.find_next("p").text.strip()
                    m = regex_date.match(collection_string)
                    if m:
                        collection_date = datetime.strptime(
                            m.group(1), "%d/%m/%Y"
                        ).date()
                        data["bins"].append(
                            {
                                "type": bin_type,
                                "collectionDate": collection_date.strftime("%d/%m/%Y"),
                            }
                        )
                        all_collection_dates.append(collection_date)

                # Search for additional collections
                for p in panel.select("p"):
                    m2 = regex_additional_collection.match(p.text.strip())
                    if m2:
                        bin_type = m2.group(1)
                        if "each collection day" in m2.group(2):
                            collection_date = min(all_collection_dates)
                            data["bins"].append(
                                {
                                    "type": bin_type,
                                    "collectionDate": collection_date.strftime(
                                        "%d/%m/%Y"
                                    ),
                                }
                            )
                break

        return data
