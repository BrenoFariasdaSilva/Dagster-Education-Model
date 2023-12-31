# [Dagster-EducationModel](https://github.com/BrenoFariasdaSilva/Dagster-EducationModel)
---
#### This repository is a translation of a Jupyter notebook education model to Dagster, in which uses Dagster 1.3.11 and Python 3.7.17.
#### Dagster is a data orchestrator for machine learning, analytics, and ETL. It lets you define pipelines in terms of the data flow between reusable, logical components, then test locally and run anywhere. With a unified view of pipelines and the assets they produce, Dagster can schedule and orchestrate Pandas, Spark, SQL, or anything else that Python can invoke. It abstracts away the infrastructure details and job execution, so that you can focus on what matters: building data applications. For more information, please visit the [Dagster website](https://dagster.io/).
---

## Project Files Structure:
There are two levels of folders in this project. The first level is the project folder (root), and the second level is the Dagster folder (translated model). The project folder contains the files that are related setting up the python to a specific version (3.7.17) and dagster depencies. The Dagster folder contains the files that are related to Dagster project. Each folder level have a README.md file and a Makefile file.

## Install Dependencies:
### Pre-requisites:
First you need to run the `prerequisites.sh` file to install the project dependencies, such as `python`, `homebrew` and `node`. This file will install the `pyenv` and `pyenv-virtualenv` to manage the Python versions and virtual environments. The `homebrew` will be installed as package manager for the dagster packages. Lastly, the `node` is installed for the use of the website, in which we will have the dagster UI.

```shell
chmod +x ./prerequisites.sh # Gives execution permission to the file
./prerequisites.sh # Installs project dependencies
```

### Backend:
Now you need to run the `backend.sh` file (also located in the root directory of the project), which will create the python virtual environment and install the dagster packages, install `yarn`, the python modules and `dagit` (dagster UI).
```shell
chmod +x ./backend.sh # Gives execution permission to the file
./backend.sh # Installs project dependencies
```
Great, the dagster dependencies are installed. Now we need to install the project/model dependencies, located in `Dagster-Model/` folder.

### Model Dependencies:
Now that you have Python 3.7.17 installed, the Dagster dependencies and the pyenv virtual environment created, open a new terminal in the `Dagster-Model/` folder and execute the following makefile rule:

```shell
cd Dagster-Model # Enters the project folder
make dependecies # Installs the project dependencies, such as:
# Install Python dependencies of the model -> pandas, matplotlib, seaborn and scikit-learn.
# Install the database module dependencies -> psycopg2-binary and sqlalchemy, etc.
# Install Docker and Docker-Compose.
# Build the docker-compose.
```
Now you have the project dependencies installed. Let's run the model.
## How to Run:
At this point, you can simply run the following command to run the model:
```shell
make dagster # Run the dagster model
```
This will run the dagster dev command, which will be executed on port 3000 and receive requests from any host. You can access the dagster UI by accessing the following link: http://localhost:3000.