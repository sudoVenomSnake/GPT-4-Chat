import streamlit as st
import openai
from langchain.agents import AgentType, initialize_agent, load_tools, get_all_tool_names
from langchain.chat_models import ChatOpenAI
import redirect as rd


openai.api_key = st.secrets['OPENAI_API_KEY']

if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": f"Enter paragraph by paragraph."})
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm = ChatOpenAI(temperature = 0.0, model = "gpt-4")

tools = load_tools(
    ["arxiv"],
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose = True,
)

BASE_PROMPT = "Re-write the following in the style of a research paper format, with relevant citations. Write in plain and professional English. Only rewrite what I give you, keeping it the same length. Write queries in ArXiV to get relevant papers. Give citations after rewriting the text in the proper citation format. Only cite when absolutely sure, else it is not compulsory (you will be graded on quality of cites). The format is - <some text []...> [] Citation [] Citation..."

prompt = st.chat_input()
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with rd.stdout as out:
             full_response = agent_chain.run(BASE_PROMPT + "\n" + prompt)
        # report = []
        # for resp in client.chat.completions.create(
        #     model = "gpt-4",
        #     messages=[
        #             {"role": "system", "content": "You are a Professor of Automata, who explains questions of Automata really well and step by step."},
        #             {"role": "user", "content": prompt},
        #         ],
        #     stream = True):
        #     if resp.choices[0].finish_reason == "stop":
        #         break
        #     # result = resp.choices[0].delta.content
        #     full_response += resp.choices[0].delta.content
        #     report.append(resp.choices[0].delta.content)
        #     result = "".join(report).strip()
        #     # result = result.replace("\n", "")    
        #     message_placeholder.markdown(f'{result}' + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
