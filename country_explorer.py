import requests
import streamlit as st
import wikipedia

# --- Helper: Get Country Info ---
def Country(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    country_data = response.json()
    if isinstance(country_data, list) and country_data:
        country = country_data[0]
        info = {
            'Name': country.get('name', {}).get('common', 'N/A'),
            'Capital': country.get('capital', ['N/A'])[0],
            'Population': f"{country.get('population', 'N/A'):,}",
            'Area': f"{country.get('area', 'N/A'):,} km²",
            'Region': country.get('region', 'N/A'),
            'Subregion': country.get('subregion', 'N/A'),
            'Languages': ', '.join(country.get('languages', {}).values()),
            'Currency': ', '.join([c.get('name', 'N/A') for c in country.get('currencies', {}).values()]),
            'Flag': country.get('flags', {}).get('png', '')
        }
        return info
    return None

# --- Helper: Wikipedia Summary ---
def wiki(country_name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/Tourism_in_{country_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No information available.")
    return "No information available."

# --- Streamlit App ---
st.title("🌍 Country Explorer")
st.write("Type a country name to explore details, flag, and famous places!")

country_input = st.text_input("Enter a country name:")

if st.button("Search"):
    if country_input:
        info = Country(country_input)
        summary = wiki(country_input)

        if info:
            st.subheader(f"📌 General Information: {info['Name']}")
            st.write(f"**Capital:** {info['Capital']}")
            st.write(f"**Population:** {info['Population']}")
            st.write(f"**Area:** {info['Area']}")
            st.write(f"**Region:** {info['Region']} ({info['Subregion']})")
            st.write(f"**Languages:** {info['Languages']}")
            st.write(f"**Currency:** {info['Currency']}")

            if info['Flag']:
                st.image(info['Flag'], caption=f"Flag of {info['Name']}")

            st.subheader("🏛️ Famous Places & Tourism")
            st.write(summary)
        else:
            st.error("❌ Country not found. Please try again.")
