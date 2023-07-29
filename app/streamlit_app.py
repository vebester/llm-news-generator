from typing import Dict, List, Optional, Tuple, Union, Any
from dotenv import dotenv_values
import streamlit as st
from streamlit_chat import message
from langchain.docstore.document import Document
from langchain import PromptTemplate
from llm_langchain.llm_langchain import LLMLangChain
from llm_langchain.llm_langchain_chat import LLMLangChainChat
from llm_langchain.prompt_builder.prompt_builder import PromptBuilder
from llm_langchain.docs_store import DocsStore
from llm_langchain.chroma_docs_store import ChromaDocsStore
import json
import logging

# from llm_langchain.utils import pull_from_website

_logger = logging.getLogger(__name__)

# setup streamlit page
st.set_page_config(
    page_title="ChatGPT",
    page_icon="🤖"
)

# from app.core.config import config
config: Dict[str, Any] = dotenv_values(".env")
if not config:
    # config = {k: = v for k, v in st.secrets.items()}
    config["DEBUG"] = st.secrets["DEBUG"]
    # config["ENV_MODE"] = st.secrets["ENV_MODE"]
    config["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
# st.write(config)

debug: bool = bool(config["DEBUG"])
# env_mode: str = config["ENV_MODE"]

MODEL_NAMES = ("gpt-3.5-turbo", "gpt-4")

config["model_name"] = MODEL_NAMES[0]

llm_langchain = LLMLangChainChat(config)

docs_store = ChromaDocsStore(config)

# llm_langchain.splitter = docs_store.splitter

llm_langchain.docs_store = docs_store

pb = PromptBuilder()

# Вы являетесь опытным комментатором тем для обсуждения в Twitter, Instagram или любых других сообществах.
# system_template = "You are an experienced editor and article writer."
# pb.system_template = system_template

# initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("ChatGPT")
# st.subheader("AI Tutor:")

SENTIMENT = {
    "negative",
    "positive"
    #   "neutral"
}

CATEGORIES = (
    "Select",
    "Gun Control",
    "Abortion",
    "Religious Freedom",
    "Animal Rights",
    "Vaccines",
    "Privacy Rights",
    "Free-Market Capitalism",
    "Global Climate Change",
    "Evolution",
    "Marijuana Legalization",
    "Capital Punishment",
    "Marriage Equality",
    #    "vector",
    "Immigration Reform",
    "Trump Presidency",
    "Opioid Crisis",
    "Transgender Rights",
    "Federal Livable Wage",
    "White Supremacy",
    "Electoral College",
    "Black Lives Matter",
    "Cancel culture",
    "Student Debt Crisis",
    "Israeli-Palestinian Conflict",
    "Universal healthcare",
    "Consensual sex",
    "Gene Editing",
    "Age of marriage",
    "Uniform Civil Code",
    "Fiat or Crypto",
    "Cattle slaughter",
    "Rastra Basha",
    "Sabarimala issue",
    "News Ethics",
    "Beauty pageants",
    "Driverless cars",
    "Rohingya refugees",
    "Mass migration",
    "Whistleblowing",
    "Bullet for bullet",
    "Suicide legislation",
    "Gambling Regulation",
    "Parenting style",
    "Alcohol Ban",
    "Technological unemployment",
    "Online Piracy",
    "Boycott of Chinese goods",
    "Homeschooling",
    "School uniform",
    "Gender equality",
    "Media censorship",
    "Modern Slavery",
    "Conscription",
    "Organ Donation",
    "Caste Reservations",
    "Ban of Bandhs",
    "Russo-Ukrainian War",
    "Syrian civil war",
    "Energy War"
)

text_category: str = ""
output_language: str = "English"

OPENAI_COMPLETION_OPTIONS = {
    "temperature": 0,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

st.header("Text Summarizer 🤖")

# sidebar with user input
with st.sidebar:
    model_name = st.selectbox(
        "Select a model",
        MODEL_NAMES
    )

    if model_name:
        config["model_name"] = model_name
        llm_langchain = LLMLangChainChat(config)

    max_sentences = st.selectbox(
        "Max num of sentences in summary:", ('1', '2', '3', '4', '5'), index=4)

    max_chars = st.number_input(
        "Max num of summary chars:", min_value=1, max_value=300, value=300)

    max_categories = st.selectbox(
        "Max num of categories:", ('1', '2', '3', '4', '5'), index=4)

    output_language = st.selectbox(
        "Output Language:", ('English', 'Russian'))

    # def _send_data():
    #    st.session_state.counter += 1

    # form = st.form(key="my_form")
    # n_negative = form.slider("Num negative comments", 0, 10)
    # n_positive = form.slider("Num positive comments", 0, 10)
    # submit_button_click = st.form_submit_button(
    #    label="Rerun",
    #    on_click=_send_data
    # )
    # if submit_button_click:

input_data: str = ""

url = st.text_input(
    "Web Page Url: ", placeholder="https://", key="user_input_url")

if st.button("Get from url"):
    if url:
        # st.write("Getting webpage...")
        docs: List[Document] = DocsStore.load_urls([url])
        if len(docs) != 0:
            input_data = docs[0].page_content

user_input = st.text_area(
    "Text: ", value=input_data, key="user_input")

# user_summary_input = st.text_area(
#    "Summary: ", value="", key="user_summary_input")


# text_category = st.selectbox(
#    "Text category: ", CATEGORIES, index=0, key="user_category_list")

if st.button("Summarize"):
    # handle user input
    user_input.strip()
    if user_input or text_category != "Select":
        if text_category == "Select":
            text_category = ""

        llm = llm_langchain.chat_open_ai(temperature=0)

        num_tokens = llm.get_num_tokens(user_input)
        print(f"Text has {num_tokens} tokens")

        pb.set_vars(
            text=user_input, text_category=text_category,
            max_sentences=int(max_sentences), max_chars=max_chars,
            output_language=output_language)
        # input_language="Russian", output_language="Russian")

        st.session_state.messages = ["Summarize"]

        category_tag: str = ""

        with st.spinner("Thinking..."):

            human_template = pb.get_human_template()

            if debug:
                st.write(human_template)

            human_prompt = PromptTemplate(
                template=human_template, input_variables=["text"])
            # "max_sentences",
            # "max_chars"])

            # human_prompt = llm_langchain.prompt_from_template(
            #    template=human_template,
            #    input_variables=["text", "max_sentences", "max_chars"])

            # if debug:
            #    st.write(human_prompt)

            # num_human_tokens = llm.get_num_tokens(human_prompt)
            # print(f"human prompt has {num_human_tokens} tokens")

            # st.session_state.messages.append(llm_langchain.human_message(content=user_input))

            # human_message_prompt = llm_langchain.human_message(human_template)

            # texts = llm_langchain.docs_store.splitter.split_text(user_input)
            # docs = [Document(page_content=t) for t in texts[:3]]

            # Create Document objects for the user_input
            docs = docs_store.splitter.create_documents([user_input])

            num_documents = len(docs)
            print(f"Docs split up into {num_documents} documents")

            # summary_prompt = human_prompt.format(
            #    text=user_input,
            # text_category=text_category,
            #    max_sentences=int(max_sentences), max_chars=max_chars
            # )

            chain = llm_langchain.load_summarize_chain(prompt=human_prompt)

            # chain = llm.chain(prompt=chat_prompt)
            output = chain.run(docs)

            # output = chain.run(docs,
            #                   text=user_input, text_category=text_category,
            #                   max_sentences=int(max_sentences), max_chars=max_chars,
            #                   output_language=output_language)
            # input_language="Russian", output_language=output_language)

            st.write(output)
            # st.write(type(output))

            if type(output) == str:
                print(output)
            # user_summary_input = output.strip()

            st.session_state.messages.append(output)

            # for i in range(1, n_comments + 1):
            #    st.session_state.messages.append(
            #        str(i))

    else:
        st.write('Enter the text.')

if st.button("Classify"):
    # handle user input
    user_input.strip()
    if user_input or text_category != "Select":
        if text_category == "Select":
            text_category = ""

        llm = llm_langchain.chat_open_ai(temperature=0)

        # num_tokens = llm.get_num_tokens(user_input)
        # print(f"Text has {num_tokens} tokens")

        pb.set_vars(
            text=user_input, text_category=text_category,
            max_sentences=int(max_sentences), max_chars=max_chars,
            max_categories=int(max_categories),
            categories=list(CATEGORIES[1:]),
            output_language=output_language)
        # input_language="Russian", output_language="Russian")

        st.session_state.messages = ["Classify"]

        category_tag: str = ""

        with st.spinner("Thinking..."):

            system_message_prompt = llm_langchain.system_message_prompt_templay(
                pb.get_system_classification_template())

            human_template = pb.get_human_classification_template()

            if debug:
                st.write(human_template)

            human_message_prompt = llm_langchain.human_message_prompt_templay(
                human_template)

            chat_prompt = llm_langchain.chat_prompt_templay(
                system_message_prompt, human_message_prompt)

            # texts = llm_langchain.docs_store.splitter.split_text(user_input)
            # docs = [Document(page_content=t) for t in texts[:3]]

            # Create Document objects for the user_input
            # docs = docs_store.splitter.create_documents([user_input])

            # num_documents = len(docs)
            # print(f"Docs split up into {num_documents} documents")

            chain = llm_langchain.chain(prompt=chat_prompt)

            output = chain.run(
                text=user_input, text_category=text_category,
                max_categories=max_categories,
                categories=list(CATEGORIES[1:]),
                max_sentences=int(max_sentences), max_chars=max_chars,
                output_language=output_language)

            st.write(output)
            # st.write(type(output))

            if type(output) == str:
                print(output)

            output = output.strip()

            format_json = False

            categories: list = []

            if type(output) == list:
                categories = output
            elif type(output) == str and output[0] != "{":
                categories = output.strip("[]").split(",")
                # print("categories=", format_json, categories, type(categories))
            else:
                format_json = True
                response: Any = json.loads(output)
                print(response, type(response))
                if "categories" in response:
                    categories = response["categories"]
                    # print("categories=", format_json, categories, type(categories))
                else:
                    print(response, type(response))

                # if type(response) == dict:
                #    categories = response.labels()
                # elif type(response) == list:
                #    categories = response
                # else:
                #    print(response, type(response))

            # print(comments, type(comments), type(response))
            out: str = ""
            for i, category in enumerate(categories):
                if not format_json:
                    category = category.strip()[1:-1]
                if i == 0:
                    category_tag = f"#{category}"
                else:
                    category_tag = f", #{category}"
                out += category_tag

            st.session_state.messages.append(out)

    else:
        st.write('Enter the text.')

# handle user input
# if user_input:
#   st.session_state.messages.append(llm.human_message(content=user_input))
#   with st.spinner("Generating..."):
#       response = llm.chat_open_ai(st.session_state.messages)
#   st.session_state.messages.append(
#       llm.ai_message(content=response.content))

# display message history
messages = st.session_state.get('messages', [])

for i, msg in enumerate(messages):
    if i == 0:
        message(msg, is_user=True, key=str(i) + '_user')
    else:
        message(msg, is_user=False, key=str(i) + '_ai')

    # for i, msg in enumerate(messages[1:]):
    # if i % 2 == 0:
    #     message(msg.content, is_user=True, key=str(i) + '_user')
    # else:
#     message(msg.content, is_user=False, key=str(i) + '_ai')
