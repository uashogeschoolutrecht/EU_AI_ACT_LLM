"""
This script is designed for VM1 and implements a Streamlit page that displays contact information.

The main functionalities include:
1. Displaying the contact page: Provides the email and phone number for contacting the AI Lectoraat at Hogeschool Utrecht.
"""

import streamlit as st

def contact_page():
    """
    Displays the contact page of the website.

    The contact page provides the email and phone number for users to reach out for further inquiries or information.
    """
    st.title("Contact")
    st.markdown("""
        Email: ailectoraat@hu.nl\n
        Telefoon: +31 123 456 789
    """)

if __name__ == "__main__":
    """
    Entry point for running the Streamlit application.

    This block ensures that the contact page is displayed only if the script is executed directly.
    It will not run if the script is imported as a module in another script.
    """
    contact_page()
