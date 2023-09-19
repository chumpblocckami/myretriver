import os

import streamlit as st

from src.db import Embedder
from src.llm import LLM


@st.cache_resource
def get_llm(args):
    return LLM(args)


if "cards" not in os.listdir("./"):
    with st.spinner("Loading cards..."):
        embedder = Embedder()
        embedder.generate_dataset()

llm = get_llm({})
st.markdown("""# 🔍 MyRetriver 🔍
            Query Magic: the Gathering cards according to a specific prompts
            """)
st.image(image="images/icon.jpeg", caption="source: Reddit", use_column_width=True)

example = "A creature that returns an artifact when it dies"

with st.form("input_form"):
    query = st.text_input(label="Describe the card", value=example)
    with st.expander("More options"):
        k = st.slider(label="Number of results", min_value=1, max_value=5, value=1)
        if k:
            llm = get_llm({"k": k})
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.spinner("retrieving"):
            results = [d for d in llm.retriever.get_relevant_documents(query, search_kwargs={"k": k})]
            for d in results:
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(image=d.metadata["img"],
                                 caption=d.metadata['name'])
                    with col2:
                        st.write(d.metadata)
