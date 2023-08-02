import streamlit as st
import urllib.request
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_paragraph = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_paragraph = True
        elif tag == 'a' and self.in_paragraph:
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_paragraph = False

def get_links(urls):
    parser = MyHTMLParser()
    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read()
                parser.feed(str(html))
        except Exception as e:
            st.error(f"Failed to retrieve data from {url}. Error: {str(e)}")
    return parser.links

def main():
    st.title("URL Link Extractor")
    uploaded_file = st.file_uploader("Upload a file with URLs", type='txt')
    if uploaded_file is not None:
        text_string = uploaded_file.read().decode('utf-8')
        urls = text_string.split("\n")
        if st.button("Extract links"):
            links = get_links(urls)
            for link in links:
                st.write(link)

if __name__ == "__main__":
    main()
