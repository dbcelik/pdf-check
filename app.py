import streamlit as st
from tools.pdf_compare import compare_pdfs

# -------------------
# LOGIN FUNCTION
# -------------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Hardcoded credentials for now (can be moved to secrets for Streamlit Cloud)
        if username == "orsusfacades" and password == "123456":
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password")

# -------------------
# CHECK LOGIN
# -------------------
if "logged_in" not in st.session_state:
    login()
    st.stop()  # Stop further execution until login is successful

# -------------------
# MAIN APP
# -------------------
st.set_page_config(page_title="PDF Compare Tool", layout="wide")

st.sidebar.title("Tools")

tool = st.sidebar.selectbox(
    "Select a tool",
    ["PDF Compare"]
)

if tool == "PDF Compare":
    st.title("📄 PDF Compare")

    tab1, tab2 = st.tabs(["PDF 1 (Old)", "PDF 2 (New)"])

    with tab1:
        pdf1 = st.file_uploader(
            "Select OLD PDF",
            type="pdf",
            key="pdf1"
        )

    with tab2:
        pdf2 = st.file_uploader(
            "Select NEW PDF",
            type="pdf",
            key="pdf2"
        )

    if st.button("Compare"):
        if pdf1 and pdf2:
            with st.spinner("Comparing PDFs..."):
                result = compare_pdfs(pdf1, pdf2)

            if result == "SAME":
                st.success("The PDFs are identical 🎉")
            else:
                st.error("Differences found")
                st.text_area(
                    "Comparison Result",
                    result,
                    height=400
                )
        else:
            st.warning("Please select both PDFs")
