import os
import pathlib
import logging
import argparse

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s')


def create_vdst():
    parser=argparse.ArgumentParser(description='create a new data science project using vdst-vansh_data_science_template')
    parser.add_argument('project_name',type=str,help="name of your data science project using vdst")
    arg=parser.parse_args()
    project_name=arg.project_name
    print(f"Creating your new vdst data science project {project_name}")

    files_in_project=[
        ".github/workflows/.gitkeep"
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/config/__init__.py",
        f"src/{project_name}/config/configuration.py",
        f"src/{project_name}/pipeline/__init__.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/constants/__init__.py",
        "config/config.yaml",
        "params.yaml",
        "requirements.txt",
        "setup.py",
        ".gitignore",
        "notebooks/trials.ipynb"



    ]

    for file_path in files_in_project:
        file_path=pathlib.Path(file_path)
        file_dir,file_name=os.path.split(file_path)

        if file_dir!="":
            os.makedirs(file_dir,exist_ok=True)
            logging.info(f"creating a file directory {file_dir} : for {file_name}")

        if(not os.path.exists(file_path) or os.path.getsize(file_path)==0):
            with open(file_path,'w'):
                pass
            logging.info(f"created the file {file_path}")
        else:
            logging.info(f"file {file_path} already exists")

            