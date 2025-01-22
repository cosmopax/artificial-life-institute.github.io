import os
import subprocess

def prepare_receptor(receptor_path, output_path):
    """Prepare receptor by converting PDB to PDBQT."""
    command = f"obabel {receptor_path} -O {output_path} --addh --gen3D"
    subprocess.run(command, shell=True)
    return output_path

def prepare_ligand(ligand_path, output_path):
    """Prepare ligand by converting PDB to PDBQT."""
    command = f"obabel {ligand_path} -O {output_path} --addh --gen3D"
    subprocess.run(command, shell=True)
    return output_path

def perform_docking(receptor_pdbqt, ligand_pdbqt, output_file):
    """Run AutoDock Vina docking simulation."""
    vina_command = (
        f"vina --receptor {receptor_pdbqt} --ligand {ligand_pdbqt} "
        f"--center_x 0 --center_y 0 --center_z 0 "
        f"--size_x 20 --size_y 20 --size_z 20 "
        f"--out {output_file} --log docking.log"
    )
    subprocess.run(vina_command, shell=True)

def run_workflow(receptor, ligand):
    """Complete docking workflow."""
    receptor_pdbqt = prepare_receptor(receptor, "receptor.pdbqt")
    ligand_pdbqt = prepare_ligand(ligand, "ligand.pdbqt")
    perform_docking(receptor_pdbqt, ligand_pdbqt, "output.pdbqt")
    print("Docking simulation finished. Check output.pdbqt and docking.log.")
