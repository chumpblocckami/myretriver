import os

from dotenv import load_dotenv
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.vectorstores.chroma import Chroma

from .utils import hf_embedding_functions

load_dotenv()


class LLM():
    def __init__(self, kwargs={"k":5}):
        ## TODO: GENERATE THIS INFO USING LLM (prompt ex.: we are talking about magic the gathering cards: describe {attribute} as you were an experience player")
        self.fields = [
            AttributeInfo(
                name="name",
                description="The name of the card",
                type="string",
            ),
            AttributeInfo(
                name="cmc",
                description="The converted mana cost (cmc) of the card",
                type="integer",
            ),
            AttributeInfo(
                name="price",
                description="The price in euro of the card",
                type="float",
            )

        ]
        self.description = "Collection of Magic:the Gathering cards"

        self.llm = OpenAI(temperature=1,
                          openai_api_key=os.environ["OPENAI_API_KEY"])
        self.vectorstore = Chroma(persist_directory="./cards",
                                  collection_name="cards",
                                  embedding_function=hf_embedding_functions)

        self.retriever = SelfQueryRetriever.from_llm(
            self.llm,
            self.vectorstore,
            self.description,
            self.fields,
            verbose=True,
            enable_limit=True,
            search_kwargs=kwargs
        )
