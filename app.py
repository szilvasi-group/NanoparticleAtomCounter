import os
import tempfile
import pandas as pd
import streamlit as st
# Re‑use the existing CLI entry‑point (adjust to your module layout)
from nanoparticleatomcounting.atom_count import main as atom_counter

st.set_page_config(page_title="Nanoparticle Atom Counter", page_icon="🧮")

st.title("Nanoparticle Atom Counter")

st.markdown(
    """
    Upload a **.csv**, **.xls**, or **.xlsx** file that contains the nanoparticle
    geometric parameters (**r**, **R**, **Theta**, **Element**, **Facet**).

    <u>Definitions:</u>  
    • **r** – footprint radius in Å  
    • **R** – radius of curvature in Å  
      *Note: supply **either** r **or** R; if you supply both, r is used and R ignored.*  
    • **Theta** – contact angle  
    • **Element** – atom type the nanoparticle is made of  
    • **Facet** – facet in contact with the support (optional)

    **Column headers must be exactly:**  
    `r (A),R (A),Theta,Element,Facet`

    e.g.
    r (A),R (A),Theta,Element,Facet
    34.88120454078012,0.0,100.0,Ag,(1, 0, 0)
    36.08176747235197,0.0,100.0,Ag,(1, 0, 0)
    36.37571748236948,0.0,100.0,Ag,(1, 0, 0)

    Leave blanks for whichever column you're not supplying, e.g. "Facet" or "R (A)"
    
    Finally, pick whether the atoms should be counted by **volume** or by **area**.
    The app will run the same calculation you use on the command line and
    return a results table you can download as CSV.
    """,
    unsafe_allow_html=True,   # needed for <u> underline
)


# ────────────────────────────────────────────────  INPUT  ─────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Input file (one table)",
    type=("csv", "xls", "xlsx"),
    accept_multiple_files=False,
)

mode = st.radio("Counting mode", ("volume", "area"), horizontal=True)

# ──────────────────────────────────────────────  PROCESS  ─────────────────────────────────────────────────
if uploaded is not None:
    with st.spinner("Processing …"):
        # 1️⃣  Save the upload to a temporary file so the CLI can read it
        in_suffix = os.path.splitext(uploaded.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=in_suffix) as tmp_in:
            tmp_in.write(uploaded.getbuffer())
            tmp_in.flush()
            in_path = tmp_in.name

        # 2️⃣  Prepare an output path (CSV)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_out:
            out_path = tmp_out.name

        # 3️⃣  Run the heavy computation
        try:
            atom_counter(in_path, out_path, mode=mode)
        except Exception as exc:
            st.error(f"❌ Calculation failed: {exc}")
            # Clean up before leaving
            os.remove(in_path)
            os.remove(out_path)
            st.stop()

        # ────────────────────────────────────────  OUTPUT  ────────────────────────────────────────────────
        # 4️⃣  Offer a download button
        with open(out_path, "rb") as f:
            st.download_button(
                label="Download results as CSV",
                data=f,
                file_name="atom_count_output.csv",
                mime="text/csv",
            )

        # 5️⃣  Preview the table inside the app
        df_out = pd.read_csv(out_path)
        st.subheader("Preview of results")
        st.dataframe(df_out, use_container_width=True)

        # 6️⃣  House‑keeping: remove temp files (they are outside /tmp cleanup scope on Streamlit Cloud)
        os.remove(in_path)
        os.remove(out_path)

