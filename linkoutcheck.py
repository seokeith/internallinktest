import streamlit as st
import urllib.request
from html.parser import HTMLParser
import csv
import pandas as pd
import io

class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_paragraph = False
        self.links = []
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_paragraph = True
        elif tag == 'a' and self.in_paragraph:
            self.current_link = dict(attrs).get('href')

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_paragraph = False
        elif tag == 'a' and self.in_paragraph:
            self.current_link = None

    def handle_data(self, data):
        if self.current_link is not None:
            self.links.append((self.current_link, data.strip()))

def get_links(urls):
    results = []
    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
                parser = MyHTMLParser()
                parser.feed(html)
                for link, text in parser.links:
                    results.append((url, link, text))
        except Exception as e:
            st.error(f"Failed to retrieve data from {url}. Error: {str(e)}")
    return results

def main():
    st.title("URL Link Extractor")
st.write("Please upload a CSV file. The CSV file should have one column with the URLs you want to check. The output will tell you where this page is linking to.")
    uploaded_file = st.file_uploader("Upload a CSV file with URLs", type='csv')
    if uploaded_file is not None:
        text_io = io.TextIOWrapper(uploaded_file)
        csv_reader = csv.reader(text_io)
        urls = [row[0] for row in csv_reader]  # Assumes URLs are in first column
        if st.button("Extract links"):
            data = get_links(urls)
            df = pd.DataFrame(data, columns=['Scraped URL', 'Link URL', 'Link Text'])
            st.table(df)

if __name__ == "__main__":
    main()
