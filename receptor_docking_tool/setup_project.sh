#!/bin/bash

# Set the project directory
PROJECT_DIR="/Users/cosmopax/Desktop/webpage/receptor_docking_tool"

# Create the project directory
mkdir -p "$PROJECT_DIR"

# Navigate to the project directory
cd "$PROJECT_DIR" || exit

# Create necessary files
echo "Creating files in $PROJECT_DIR..."

# Create docking_workflow.py
cat <<EOL > docking_workflow.py
import os
import subprocess

def prepare_receptor(receptor_path, output_path):
    \"\"\"Prepare receptor by converting PDB to PDBQT.\"\"\"
    command = f"obabel {receptor_path} -O {output_path} --addh --gen3D"
    subprocess.run(command, shell=True)
    return output_path

def prepare_ligand(ligand_path, output_path):
    \"\"\"Prepare ligand by converting PDB to PDBQT.\"\"\"
    command = f"obabel {ligand_path} -O {output_path} --addh --gen3D"
    subprocess.run(command, shell=True)
    return output_path

def perform_docking(receptor_pdbqt, ligand_pdbqt, output_file):
    \"\"\"Run AutoDock Vina docking simulation.\"\"\"
    vina_command = (
        f"vina --receptor {receptor_pdbqt} --ligand {ligand_pdbqt} "
        f"--center_x 0 --center_y 0 --center_z 0 "
        f"--size_x 20 --size_y 20 --size_z 20 "
        f"--out {output_file} --log docking.log"
    )
    subprocess.run(vina_command, shell=True)

def run_workflow(receptor, ligand):
    \"\"\"Complete docking workflow.\"\"\"
    receptor_pdbqt = prepare_receptor(receptor, "receptor.pdbqt")
    ligand_pdbqt = prepare_ligand(ligand, "ligand.pdbqt")
    perform_docking(receptor_pdbqt, ligand_pdbqt, "output.pdbqt")
    print("Docking simulation finished. Check output.pdbqt and docking.log.")
EOL

# Create app.py
cat <<EOL > app.py
import streamlit as st
from docking_workflow import run_workflow

st.title("Receptor-Ligand Docking Tool")

# File uploads for receptor and ligand
receptor_file = st.file_uploader("Upload Receptor (PDB)", type=["pdb"])
ligand_file = st.file_uploader("Upload Ligand (PDB)", type=["pdb"])

if st.button("Run Docking"):
    if receptor_file and ligand_file:
        # Save uploaded files temporarily
        receptor_path = "uploaded_receptor.pdb"
        ligand_path = "uploaded_ligand.pdb"
        with open(receptor_path, "wb") as f:
            f.write(receptor_file.getbuffer())
        with open(ligand_path, "wb") as f:
            f.write(ligand_file.getbuffer())

        # Run docking workflow
        run_workflow(receptor_path, ligand_path)

        st.success("Docking simulation complete! Check output.pdbqt and docking.log.")
    else:
        st.error("Please upload both receptor and ligand files.")
EOL

# Create requirements.txt
cat <<EOL > requirements.txt
streamlit
vina
openbabel
EOL

# Create README.md
cat <<EOL > README.md
# Receptor-Ligand Docking Tool

This project enables receptor-ligand docking simulations using AutoDock Vina with a Streamlit-based web interface.

## Features
- Prepare receptor and ligand files (PDB to PDBQT).
- Perform docking simulations with AutoDock Vina.
- View results directly.

## Setup Instructions
1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
2. Run the Streamlit app:
   \`\`\`bash
   streamlit run app.py
   \`\`\`

## Requirements
- Python 3.7+
- AutoDock Vina
- Open Babel
EOL

echo "All files created successfully in $PROJECT_DIR."
