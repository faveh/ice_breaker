from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parser import person_intel_parser, PersonIntel
from third_parties.linkedin import (
    scrape_linkedin_profile,
    scrape_linkedin_profile_from_gist,
)
from third_parties.twitter import scrape_user_tweets


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    # Using agent to get search online for the name and fetch the linkedin profile url of the name
    linkedin_profile_url = linkedin_lookup_agent(name=name)

    # scraping the linkedin profile page
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    print(linkedin_data)

    # scraping the twitter page
    twitter_username = twitter_lookup_agent(name=name)
    print(twitter_username)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)

    # A templates of what we want the llm to do, given an information: scraped data from the linkedin profile
    summary_template = """
             given the Linkedin information {linkedin_information} and twitter {twitter_information} about a person from I want you to create:
             1. a short summary
             2. two interesting facts about them
             3. A topic that may interest them
             4. 2 creative Ice breakers to open a conversation with them
            \n{format_instructions}
         """

    prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # chaining the llm and the prompt templates
    chain = LLMChain(llm=llm, prompt=prompt_template)

    result_ = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)
    print(result_)
    print(linkedin_data.get("profile_pic_url"))
    return person_intel_parser.parse(result_), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello LangBaba")
    result = ice_break(name="Harrison Chase")
    print(result)
