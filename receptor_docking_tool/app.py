import streamlit as st
from docking_workflow import run_workflow, convert_to_pdbqt
import os
import subprocess

# Define directories for storage
LIGANDS_DIR = "/Users/cosmopax/Desktop/doc/ligands"
LIGANDS_PDBQT_DIR = "/Users/cosmopax/Desktop/doc/ligands/pdbq"
RECEPTORS_DIR = "/Users/cosmopax/Desktop/doc/receptors"
RECEPTORS_PDBQT_DIR = "/Users/cosmopax/Desktop/doc/receptors/pdbq"

# Ensure directories exist
os.makedirs(LIGANDS_PDBQT_DIR, exist_ok=True)
os.makedirs(RECEPTORS_PDBQT_DIR, exist_ok=True)

def convert_and_save(file, target_dir):
    """Convert PDB to PDBQT and save to the specified directory."""
    input_path = os.path.join(target_dir, file.name)
    output_path = os.path.join(target_dir, file.name.replace(".pdb", ".pdbqt"))

    # Save the uploaded file temporarily
    with open(input_path, "wb") as f:
        f.write(file.getbuffer())

    # Convert to PDBQT
    command = f"obabel {input_path} -O {output_path} --addh --gen3D"
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode == 0:
        return output_path
    else:
        st.error(f"Conversion failed for {file.name}: {result.stderr.decode()}")
        return None

st.title("Receptor-Ligand Docking Tool")

# Conversion Section
st.header("Convert PDB to PDBQT")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Convert Receptors")
    uploaded_receptor = st.file_uploader("Upload receptor (PDB)", type=["pdb"], key="receptor")
    if uploaded_receptor:
        converted_path = convert_and_save(uploaded_receptor, RECEPTORS_PDBQT_DIR)
        if converted_path:
            st.success(f"Receptor converted and saved to {converted_path}")

with col2:
    st.subheader("Convert Ligands")
    uploaded_ligand = st.file_uploader("Upload ligand (PDB)", type=["pdb"], key="ligand")
    if uploaded_ligand:
        converted_path = convert_and_save(uploaded_ligand, LIGANDS_PDBQT_DIR)
        if converted_path:
            st.success(f"Ligand converted and saved to {converted_path}")

# Docking Section
st.header("Run Docking")

st.write("Available Receptors:")
receptor_files = [f for f in os.listdir(RECEPTORS_PDBQT_DIR) if f.endswith(".pdbqt")]
selected_receptor = st.selectbox("Select a receptor", receptor_files)

st.write("Available Ligands:")
ligand_files = [f for f in os.listdir(LIGANDS_PDBQT_DIR) if f.endswith(".pdbqt")]
selected_ligand = st.selectbox("Select a ligand", ligand_files)

if st.button("Run Docking"):
    receptor_path = os.path.join(RECEPTORS_PDBQT_DIR, selected_receptor)
    ligand_path = os.path.join(LIGANDS_PDBQT_DIR, selected_ligand)

    # Run docking workflow
    run_workflow(receptor_path, ligand_path)
    st.success("Docking simulation complete! Check output.pdbqt and docking.log.")

