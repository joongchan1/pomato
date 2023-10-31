import subprocess, sys, os
from pathlib import Path
    
def instantiate_julia(gurobi=True, redundancyremoval_branch="main", marketmodel_branch="main"):
    cwd = str(Path(__file__).parent)
    args = ["julia", "julia_install_from_git.jl", redundancyremoval_branch, marketmodel_branch] 
    with subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, cwd=cwd) as program:
        for line in program.stdout:
            print(line.decode(errors="ignore").strip())
    if gurobi:
        add_gurobi()
        
def instantiate_julia_dev(redundancyremoval_path, marketmodel_path, gurobi=True):
    """Instantiates julia env from local repositories. 
    
    pomato.tools.julia_management.instantiate_julia_dev()
    """
    cwd = str(Path(__file__).parent)
    args = ["julia", "julia_install_dev.jl", str(redundancyremoval_path), str(marketmodel_path)] 
    with subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, cwd=cwd) as program:
        for line in program.stdout:
            print(line.decode(errors="ignore").strip())

    if gurobi:
        add_gurobi()

def update_julia():
    cwd = str(Path(__file__).parent)
    args = ["julia", "julia_update.jl"] 
    with subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, cwd=cwd) as program:
        for line in program.stdout:
            print(line.decode(errors="ignore").strip())

def add_gurobi():
    """Add Gurobi to Julia environment"""
    cwd = str(Path(__file__).parent)
    args = ["julia", "add_gurobi.jl"] 
    with subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, cwd=cwd) as program:
        for line in program.stdout:
            print(line.decode(errors="ignore").strip())
