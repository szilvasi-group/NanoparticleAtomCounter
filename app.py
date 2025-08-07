import contextlib
import os
import tempfile
from pathlib import Path
import subprocess
import sys
import pandas as pd
import streamlit as st
from nanoparticleatomcounter.cli.atom_count import main as atom_counter


# ───────────────────────────  PAGE CONFIG  ───────────────────────────
st.set_page_config(page_title="Nanoparticle Atom Counter", page_icon="🧮")

# ---------- sidebar: resources ----------
with st.sidebar:
    st.header("Resources")

    SAMPLE_CSV = Path("sample_input.csv").read_bytes()

    st.download_button(
        "Sample input (.csv)",
        SAMPLE_CSV,
        file_name="sample_input.csv",
        mime="text/csv",
    )

    st.image("Acute.png", caption="θ < 90° (acute)", use_container_width=True)
    st.image("Obtuse.png", caption="θ > 90° (obtuse)", use_container_width=True)
    st.image("Nanoparticle_Legend.tif", caption="Definition of surface, interfacial, and perimeter atoms", use_container_width=True)
# ---------------------------------------------------------------------


# ───────────────────────────  MAIN LAYOUT  ────────────────────────────
st.title("Nanoparticle Atom Counter")

st.markdown(
    """
Upload a **.csv** containing the columns  
`r (A), R (A), Theta, Element, Interface Facet, Surface Facet`.

*Supply either **r** or **R** (if both are present, **r** is used).  
Interface Facet and Surface Facet are optional; leave blank if unknown.*

**Need a template or a visual guide?**  
A sample input file and explanatory diagrams are available in the sidebar.


**This note here is for me: when the paper has been written, add a link to the paper.md and the CITATION.cff**
""",
    unsafe_allow_html=True,
)

# counting-mode selector (now in main area)
mode = st.radio("**Select Counting Mode**", ("volume", "area"), horizontal=True)


# ──────────  FILE UPLOAD  ──────────
file = st.file_uploader(
    "Drag-and-drop or browse for your input file",
    type=("csv", "xls", "xlsx"),
    accept_multiple_files=False,
)

if file is None:
    st.stop()      # wait for user input


# ──────────  CALCULATION  ──────────
if st.button("⚙️ Run calculation"):
    with st.spinner("Processing …"):

        # temporary input file
        in_suffix = Path(file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=in_suffix) as tin:
            tin.write(file.getbuffer())
            tin.flush()
            in_path = tin.name

        # temporary output file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tout:
            out_path = tout.name





        
        try:
            # call the CLI module exactly as if you ran: python -m nanoparticleatomcounting.atom_count …
            subprocess.run(
                [
                    sys.executable,              # current Python executable
                    "-m", "nanoparticleatomcounter.cli.atom_count",
                    "--input",  in_path,
                    "--output", out_path,
                    "--mode",   mode,
                ],
                check=True,
                capture_output=True,             # optional: keeps stdout/stderr
                text=True,
            )

        except subprocess.CalledProcessError as err:
            st.error(f"Atom-counter failed:\n{err.stderr}")
            os.remove(in_path)
            st.stop()
        
#        # run CLI
#        success = True
#        with contextlib.suppress(Exception):
#            atom_counter(in_path, out_path, mode=mode)
#        if not Path(out_path).exists():
#            success = False

#        if not success:
#            st.error("Calculation failed. Please check your input and try again.")
#            os.remove(in_path)
#            os.remove(out_path)
#            st.stop()

        # read and show results
        df_out = pd.read_csv(out_path)

        st.markdown("#### Results")
        st.download_button(
            "Download CSV",
            data=open(out_path, "rb").read(),
            file_name="atom_count_output.csv",
            mime="text/csv",
        )
        st.dataframe(df_out, use_container_width=True)

        # cleanup
        os.remove(in_path)
        os.remove(out_path)
  
