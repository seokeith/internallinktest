import pandas as pd
import requests
import json
import streamlit as st

# Add a title to the Streamlit app
st.title("Internal Link Opps")

def search(query, api_key, cse_id, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
    }
    params.update(kwargs)
    response = requests.get(url, params=params)
    return json.loads(response.text)

# Ask the user to input a domain
site = st.text_input("Enter the domain")

# Google API key and Custom Search Engine ID
api_key = "AIzaSyAsHeIpxd-FCLdyg4mXLjmlc3iH76pd1Es"
cse_id = "152d311f722f0406c"

# Instructions for uploading CSV file
st.write("Please upload a CSV file. The CSV file should have two columns. Column one should be called target_page, column 2 should be called keyword.")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Create a new dataframe to store results
    results_df = pd.DataFrame()

    for index, row in df.iterrows():
        # search query
        query = f"site:{site} {row['keyword']} -inurl:{row['target_page']}"

        # get the search results
        results = search(query, api_key, cse_id)

        # Extract the URLs of the search results
        link_list = [result['link'] for result in results.get('items', [])]

        # If less than 10 links are returned, fill the rest with None
        while len(link_list) < 10:
            link_list.append(None)

        # Append the list of links to the results dataframe
        results_df = pd.concat([results_df, pd.Series(link_list, name=index)], axis=1)

    # Transpose the results dataframe and set column names
    results_df = results_df.transpose()
    results_df.columns = [f'link{i+1}' for i in range(10)]

    # Concatenate the original dataframe with the results dataframe
    df = pd.concat([df, results_df], axis=1)

    # Display the updated dataframe in the app
    st.write(df)
