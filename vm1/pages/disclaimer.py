"""
This script is designed for VM1 and implements a Streamlit page that displays a disclaimer.

The main functionalities include:
1. Displaying the disclaimer page: Provides information about the purpose and limitations of the tool.
"""

import streamlit as st

def disclaimer_page():
    """
    Displays the disclaimer page of the website.

    The disclaimer provides information about the purpose of the tool, its research context,
    and a notice that it should not be considered as legal advice. Users are encouraged to seek
    professional legal advice and refer to official EU publications for authoritative information.
    """
    st.title("Disclaimer")
    st.markdown("""
        Deze tool is ontwikkeld als onderdeel van het onderzoeksproject van het AI Lectoraat aan de Hogeschool Utrecht.
        Het doel van deze tool is om inzicht te krijgen in hoe individuen en organisaties Artificial Intelligence (AI)
        toepassen en welke impact de naderende implementatie van de EU AI Act kan hebben op deze toepassingen.

        Deze tool is strikt voor onderzoeksdoeleinden en mag niet worden beschouwd als een definitieve bron van juridisch
        advies of een volledige gids over de EU AI Act. Gebruikers worden aangemoedigd om altijd professioneel juridisch
        advies in te winnen en de laatste officiële publicaties van de Europese Unie te raadplegen voordat zij beslissingen
        nemen die worden beïnvloed door de inhoud van deze tool.
    """)

if __name__ == "__main__":
    """
    Entry point for running the Streamlit application.

    This block ensures that the disclaimer page is displayed only if the script is executed directly.
    It will not run if the script is imported as a module in another script.
    """
    disclaimer_page()
