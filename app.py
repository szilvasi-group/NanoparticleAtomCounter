import streamlit as st
import tempfile, os, io

# Re-use the existing entry point
from atom_count import main as atom_counter

st.title("Nanoparticle Atom Counter")

uploaded = st.file_uploader(
    "Upload input (.csv / .xls / .xlsx)",
    type=["csv", "xls", "xlsx"]
)
mode = st.selectbox("Counting mode", ("volume", "area"))

if uploaded is not None:
    # 1️⃣  save the uploaded file to a temp location
    ext = os.path.splitext(uploaded.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_in:
        tmp_in.write(uploaded.getbuffer())
        tmp_in_path = tmp_in.name

    # 2️⃣  pick a temp path for output (plain-text)
    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp_out_path = tmp_out.name
    tmp_out.close()          # we only need its name

    # 3️⃣  run the original workflow
    atom_counter(tmp_in_path, tmp_out_path, mode=mode)

    # 4️⃣  offer the result for download
    with open(tmp_out_path, "rb") as f:
        st.download_button(
            label="Download results",
            data=f,
            file_name="atom_count_output.txt",
            mime="text/plain"
        )

    # (optional) preview the output right in the app
    with open(tmp_out_path) as f:
        st.text(f.read())

