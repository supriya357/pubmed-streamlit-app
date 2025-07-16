import streamlit as st
from Bio import Entrez

# Set your email (required by Entrez)
Entrez.email = "akkalasupriya3@gmail.com"  # ✅ Replace with your actual email
Entrez.api_key = "4bf23c35f17871cdfa7c036b44ea6eca5b09"

st.title("🧠 PubMed Paper Fetcher")
st.write("Enter a keyword to fetch the latest PubMed research articles.")

query = st.text_input("🔍 Search PubMed for:")

if query:
    with st.spinner("Fetching articles..."):
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=5)
            record = Entrez.read(handle)
            handle.close()

            id_list = record["IdList"]
            if not id_list:
                st.warning("No articles found.")
            else:
                for pubmed_id in id_list:
                    summary_handle = Entrez.esummary(db="pubmed", id=pubmed_id)
                    summary = Entrez.read(summary_handle)
                    article = summary[0]
                    st.subheader(article["Title"])
                    st.markdown(f"🔗 [View on PubMed](https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/)", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
