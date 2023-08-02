import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_links(urls):
    all_links = {}
    for url in urls:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all links within <p> tags
            links = []
            for p in soup.find_all("p"):
                for link in p.find_all("a"):
                    link_url = link.get("href")
                    link_text = link.text.strip() if link.text else ""
                    links.append((link_url, link_text))

            all_links[url] = links
        else:
            st.error(f"Failed to retrieve data from {url}")
    return all_links

def main():
    st.title("URL Link Extractor")

    uploaded_file = st.file_uploader("Upload a file with URLs", type='txt')
    if uploaded_file is not None:
        text_string = uploaded_file.read().decode('utf-8')
        urls = text_string.split("\n")
        
        if st.button("Extract links"):
            links = get_links(urls)
            for url, link_list in links.items():
                st.write(f"URL: {url}")
                for link in link_list:
                    st.write(f"Link URL: {link[0]}")
                    st.write(f"Link Text: {link[1]}")

if __name__ == "__main__":
    main()
