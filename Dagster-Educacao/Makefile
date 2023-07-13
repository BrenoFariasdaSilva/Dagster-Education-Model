# Author: Breno Farias da Silva
# Last update: 13/07/2023

# Set the pyenv environment
export PYENV_VERSION=dagster-dtw

# Run all of the makefile rules:
all:
	dependencies docker docker_compose dagster

# Install the external project dependencies (Not related to dagster, but to the model):
dependencies:
	clear;
	pip install pandas matplotlib seaborn scikit-learn

# Install Docker and Docker Compose:
docker:
	sudo apt update -y
	sudo apt-get install \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg \
	lsb-release
	curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo \
	"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
	$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
	sudo apt update -y
	sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
	sudo groupadd docker
	sudo usermod -aG docker $USER
	sudo apt get install docker -y
	sudo apt install docker.io -y
	sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	sudo docker run --name hello-world-container hello-world
	sudo systemctl enable docker.service
	sudo systemctl enable containerd.service
	sudo docker rm hello-world-container

# Run Docker Compose:
docker_compose:
	docker-compose up -d

# Run the dagster project:
dagster:
	clear;
	dagster dev -h 0.0.0.0 -p 3000
