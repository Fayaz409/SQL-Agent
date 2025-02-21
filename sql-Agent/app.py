import streamlit as st
from agent import SQLiteAgent
from tools import list_tables, get_table, sql_query
import json

st.set_page_config(page_title="SQLite Data Talk Agent", layout="wide")
st.title("SQLite Data Talk Agent")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Initialize the SQLite agent with our tools
agent = SQLiteAgent(tools=[list_tables, get_table, sql_query])

# User input
query = st.text_input("Enter your query about the database:")

if query:
    with st.spinner("Processing..."):
        try:
            response = agent.invoke(query)
            st.success("Response:")
            st.write(response)
            # Update chat history
            st.session_state["chat_history"].append({"user": query, "agent": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display conversation history
if st.session_state["chat_history"]:
    st.subheader("Conversation History")
    for chat in st.session_state["chat_history"]:
        st.markdown(f"**User:** {chat['user']}")
        st.markdown(f"**Agent:** {chat['agent']}")
        st.markdown("---")

# Optionally, you could add buttons to save/load history, etc.
