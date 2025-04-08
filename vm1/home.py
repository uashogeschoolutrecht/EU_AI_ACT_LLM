"""
This script is designed for VM1 and implements a Streamlit web application that allows users to ask questions about the EU AI Act.

The main functionalities include:
1. Displaying the home page where users can input their questions.
2. Connecting to a MySQL database to store user prompts.
3. Sending user prompts to a chatbot server and retrieving responses.

Main Components:
- `home_page` function: Displays the main interface for user interaction.
- `connect_db` function: Establishes a connection to the MySQL database.
- `insert_prompt` function: Inserts user prompts into the database.
- `message_chatbot` function: Sends prompts to the chatbot server and retrieves responses.
- `perform_prompt` function: Handles the process of inserting prompts and updating the interface with chatbot responses.
- Entry point: Configures logging, sets up the Streamlit page, and loads custom styles.
"""

from pathlib import Path
import streamlit as st
import mysql.connector
import asyncio
import logging
import httpx
import mysql

def home_page():
    """
    Displays the home page of the website.
    """
    st.title("Stel je vraag over de EU AI ACT....")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "current_response" not in st.session_state:
        st.session_state["current_response"] = ""

    # Display previous messages
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Input for new messages
    if prompt := st.chat_input("Wat is uw vraag?"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state["current_response"] = ""
        st.session_state['messages'].append({"role": "assistant", "content": "..."})
        asyncio.run(perform_prompt(prompt))

async def connect_db():
    """
    Connects to the MySQL database and returns the connection object.

    Returns:
        connection (mysql.connector.connection.MySQLConnection): The connection object to the MySQL database.

    Raises:
        ConnectionError: If the connection to the MySQL database fails.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='vragen_db',
            user='feedbackuserai',
            password='OnsWWvanhetprojectai123!'
        )
        if not connection.is_connected():
            raise ConnectionError("MySql is not connected.")
        return connection

    except BaseException as e:
        logging.error(f"Error connecting to MySQL: {e}")
        st.error("Er is een fout opgetreden met het verbinden van de server.")

async def insert_prompt(prompt: str):
    """
    Inserts a prompt into the 'vragen' table in the database.

    Args:
        prompt (str): The prompt to be inserted.

    Raises:
        BaseException: If there is an error executing the MySQL query.
    """
    try:
        if connection := await connect_db():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO vragen (vraag) VALUES (%s)", (prompt,))
            connection.commit()
            cursor.close()
            connection.close()
    except BaseException as e:
        logging.error(f"Error executing on MySQL: {e}")
        st.error("Er is een fout opgetreden bij het opslaan van uw vraag.")

async def message_chatbot(prompt: str) -> str:
    """
    Sends a message to the chatbot server and returns the response.

    Args:
        prompt (str): The message to send to the chatbot.

    Returns:
        str: The response from the chatbot server.

    Raises:
        httpx.RequestError: If there is an error connecting to the chatbot server.
    """
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, read=60.0)) as client:
            response = await client.post("http://10.10.10.72:5000/chat", json={"message": prompt})
            response.raise_for_status()
            return response
    except httpx.RequestError as e:
        logging.error(f"Failed to connect to chatbot server: {e}")
        return None

async def perform_prompt(prompt: str):
    """
    Performs a prompt by inserting it into the chatbot, retrieving the response,
    and updating the session state with the answer.

    Args:
        prompt (str): The prompt to be sent to the chatbot.
    """
    with st.spinner("Wacht even..."):
        await insert_prompt(prompt)
        response = await message_chatbot(prompt)

        if response:
            try:
                answer = response.json()["message"].replace(prompt, "").strip()
                st.session_state['messages'][-1]['content'] = answer
                st.experimental_rerun()
            except ValueError as e:
                logging.error(f"JSON decode error: {e}")
                st.session_state['messages'][-1]['content'] = "Error processing response from server."
                st.experimental_rerun()

if __name__ == "__main__":
    """
    Entry point for running the Streamlit application.

    This block ensures that the Streamlit application runs only if the script is executed directly.
    It will not run if the script is imported as a module in another script.

    Configures logging, sets up the Streamlit page configuration, and loads custom styles.
    """
    logging.basicConfig(level=logging.DEBUG)
    st.set_page_config(
        page_title="Bot Fabio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    folder = Path(__file__).parent.as_posix()
    with open(f"{folder}/style.css", 'r') as f:
        css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    home_page()
