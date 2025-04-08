"""
This script is designed for VM1 and implements a Streamlit page that allows users to provide feedback on the responses they receive from the AI chatbot named Fabio.

The main functionalities include:
1. Displaying the feedback page: Allows users to rate response speed and answer quality, and provide textual feedback.
2. Connecting to a MySQL database to store user feedback.
3. Sending the collected feedback to the database.

Main Components:
- `feedback_page` function: Displays the main interface for user feedback.
- `connect_db` function: Establishes a connection to the MySQL database.
- `send_feedback` function: Inserts user feedback into the database.
- Entry point: Ensures the feedback page is displayed when the script is executed directly.
"""

import streamlit as st
import asyncio
import logging
import mysql.connector

def feedback_page():
    """
    Displays the feedback page of the website.

    The feedback page allows users to rate the response speed and answer quality of the AI chatbot,
    as well as provide additional textual feedback. The collected feedback is sent to the database.
    """
    st.title("Feedback")
    st.markdown("### Wat vond je van de reactiesnelheid van Fabio? (Hoger = Beter/Sneller)")
    response_time = st.slider("Reactiesnelheid:", 1, 10, 1)
    st.markdown("### Wat vond je van het antwoord van Fabio? (Hoger = Beter)")
    answer_quality = st.slider("Antwoord:", 1, 10, 1)
    feedback_text = st.text_area("Laat uw feedback achter:")

    if st.button("Verzenden"):
        if response_time and answer_quality and feedback_text:
            asyncio.run(send_feedback(response_time, answer_quality, feedback_text))
        else:
            st.error("Vul alstublieft alle velden in.")

async def connect_db() -> mysql.connector.connection.MySQLConnection:
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
            database='feedback_db',
            user='feedbackuserai',
            password='OnsWWvanhetprojectai123!'
        )
        if not connection.is_connected():
            raise ConnectionError("MySql is not connected.")
        return connection

    except BaseException as e:
        logging.error(f"Error connecting to MySQL: {e}")
        st.error("Er is een fout opgetreden met het verbinden van de server.")

async def send_feedback(response_time: int, answer_quality: int, feedback_text: str):
    """
    Sends feedback to the database.

    Args:
        response_time (int): The rating for response speed (1-10).
        answer_quality (int): The rating for answer quality (1-10).
        feedback_text (str): The text of the feedback.

    This function inserts the provided feedback into the MySQL database and displays a success
    message upon successful insertion or an error message if the insertion fails.
    """
    with st.spinner("Wacht even..."):
        try:
            if connection := await connect_db():
                cursor = connection.cursor()
                cursor.execute("INSERT INTO feedback (response_time, answer_quality, feedback) VALUES (%s, %s, %s)",
                               (response_time, answer_quality, feedback_text))
                connection.commit()
                cursor.close()
                connection.close()
                st.success("Feedback verzonden! Bedankt voor uw feedback.")
        except BaseException as e:
            logging.error(f"Error inserting feedback: {e}")
            st.error("Er is een fout opgetreden bij het verzenden van uw feedback.")

if __name__ == "__main__":
    """
    Entry point for running the Streamlit application.

    This block ensures that the feedback page is displayed only if the script is executed directly.
    It will not run if the script is imported as a module in another script.
    """
    feedback_page()
