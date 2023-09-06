import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profile
    Manually scrape the information from the LinkedIn Profile
    """
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}

    response = requests.get(
        api_endpoint,
        params={"linkedin_profile_url": linkedin_profile_url},
        headers=header_dic,
    )

    return manipulate_data_response(response.json())


def scrape_linkedin_profile_from_gist():
    response = requests.get(
        "https://gist.githubusercontent.com/faveh/a63922ab37ece1d5c2841344a6ec785f/raw/d6d97a151ba26bb207f7c3748b65ff90ab9edf99/eden-linkedin.json"
    )
    return manipulate_data_response(response.json())


def manipulate_data_response(data):
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certification"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
