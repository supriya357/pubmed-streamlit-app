import streamlit as st
from Bio import Entrez
import pandas as pd

Entrez.email = "akkalasupriya3@gmail.com"
Entrez.api_key = "4bf23c35f17871cdfa7c036b44ea6eca5b09"

st.title("🧠 PubMed Paper Fetcher")

query = st.text_input("🔍 Search PubMed for:")
debug = st.checkbox("🛠️ Show debug info")
save_csv = st.checkbox("💾 Enable CSV download")

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
                titles = []
                links = []

                for pubmed_id in id_list:
                    summary_handle = Entrez.esummary(db="pubmed", id=pubmed_id)
                    summary = Entrez.read(summary_handle)
                    article = summary[0]

                    title = article["Title"]
                    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"

                    titles.append(title)
                    links.append(url)

                    st.subheader(title)
                    st.markdown(f"[🔗 View on PubMed]({url})", unsafe_allow_html=True)

                    if debug:
                        st.code(article)

                # Save to CSV
                if save_csv:
                    df = pd.DataFrame({"Title": titles, "Link": links})
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name="pubmed_results.csv",
                        mime="text/csv"
                    )

        except Exception as e:
            st.error(f"❌ Error: {e}")

