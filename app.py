import contextlib
import os
import tempfile
from pathlib import Path
import pandas as pd
import streamlit as st

from nanoparticleatomcounting.atom_count import main as atom_counter


# ─────────────────────────────  SET-UP  ─────────────────────────────
st.set_page_config(page_title="Nanoparticle Atom Counter", page_icon="🧮")

# ---------- sidebar ----------
with st.sidebar:
    st.header("Quick start")

    #  sample download
    SAMPLE_CSV = (
        "r (A),R (A),Theta,Element,Facet\n"
        "1000,,70.0,Ag,\n"
        "120,,85,Ag,\n"
        "36.37,,102,Cu,\n"
    ).encode()
    st.download_button(
        "📥 Sample input (.csv)",
        SAMPLE_CSV,
        file_name="sample_input.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # diagrams
    st.image("Acute.png", caption="θ < 90°", use_column_width=True)
    st.image("Obtuse.png", caption="θ > 90°", use_column_width=True)

    st.markdown("---")

    # mode selector
    mode = st.radio("Counting mode", ("volume", "area"))
# ----------------------------------------


st.title("Nanoparticle Atom Counter")

st.markdown(
    """
**Step 1.** Upload a **.csv**, **.xls**, or **.xlsx** containing the columns  
`r (A)`, `R (A)`, `Theta`, `Element`, `Facet`.

*Supply **either** r **or** R (if both are given, r is used).  
Facet is optional; leave blank if unknown.*
""",
    unsafe_allow_html=True,
)

# ───────────  STEP 1 – FILE UPLOAD  ───────────
file = st.file_uploader(
    "Drag-and-drop or browse your file",
    type=("csv", "xls", "xlsx"),
    accept_multiple_files=False,
)

if file is None:
    st.stop()      # wait for the user


# ───────────  STEP 2 – CALCULATION  ───────────
st.markdown("### Step 2. Run calculation")
if st.button("⚙️ Compute atom counts"):
    with st.spinner("Crunching numbers …"):

        # temp → CLI → temp
        in_suffix = Path(file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=in_suffix) as tin:
            tin.write(file.getbuffer())
            tin.flush()
            in_path = tin.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tout:
            out_path = tout.name

        error = None
        with contextlib.suppress(Exception):
            atom_counter(in_path, out_path, mode=mode)

        if not Path(out_path).exists():
            error = f"Calculation failed. Please check your input and try again."
        if error:
            st.error(error)
            os.remove(in_path)
            os.remove(out_path)
            st.stop()

        df_out = pd.read_csv(out_path)

        # ───────────  STEP 3 – OUTPUT  ───────────
        st.markdown("### Step 3. Download & preview results")

        # download button
        with open(out_path, "rb") as f:
            st.download_button(
                "💾 Download CSV",
                data=f,
                file_name="atom_count_output.csv",
                mime="text/csv",
            )

        # preview & summary in tabs
        tab1, tab2 = st.tabs(["Preview table", "Quick stats"])
        with tab1:
            st.dataframe(df_out, use_container_width=True)
        with tab2:
            st.metric("Total particles", len(df_out))
            st.metric("Sum of atoms", int(df_out["Total"].sum()))

        # cleanup
        os.remove(in_path)
        os.remove(out_path)
