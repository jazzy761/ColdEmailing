# python -m streamlit run .\app\main.py

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chain import Chain
from portfolio import portfolio
from utils import clean_text


def process_url(url, llm, portfolio, clean_text_func):
    """Processes the URL to generate cold emails."""
    try:
        # Load data from the URL
        loader = WebBaseLoader([url])
        raw_data = loader.load().pop().page_content

        # Clean the text
        data = clean_text_func(raw_data)

        # Load the portfolio
        portfolio.load_portfolio()

        # Extract jobs and generate emails
        jobs = llm.extract_jobs(data)
        emails = []
        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)
            emails.append(email)

        return emails
    except Exception as e:
        raise RuntimeError(f"Failed to process URL: {e}")


def render_streamlit_app(llm, portfolio, clean_text_func):
    """Renders the Streamlit application."""
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Email Generator")

    # Input field for URL
    url = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-45852?from=job%20search%20funnel")

    # Process button
    if st.button("Submit"):
        try:
            emails = process_url(url, llm, portfolio, clean_text_func)
            for email in emails:
                st.code(email, language="markdown")
        except RuntimeError as e:
            st.error(str(e))


if __name__ == "__main__":
    # Initialize the required objects
    chain = Chain()
    portfolio = portfolio()

    # Run the Streamlit app
    render_streamlit_app(chain, portfolio, clean_text)
