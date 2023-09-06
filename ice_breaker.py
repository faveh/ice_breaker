from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello LangBaba")

    # Using agent to get search online for the name and fetch the linkedin profile url of the name
    linkedin_profile_url = linkedin_lookup_agent(name="Adejuwon Ayodimeji")

    # A template of what we want the llm to do, given an information: scraped data from the linkedin profile
    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # chaining the llm and the prompt template
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # scraping the linkedin profile page
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    print(chain.run(information=linkedin_data))
