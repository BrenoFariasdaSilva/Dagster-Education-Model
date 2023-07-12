# Dagster-EducationModel

Este exemplo é feito como a tradução do modelo de educação do Jupyer notebook para o Dagster.

---

## Install Dependencies:
#### Dagster Dependencies:
Você pode executar o comando abaixo para instalar as dependencias do projeto.

```shell
	chmod +x ./prerequisites.sh # Irá dar permissão de execução para o arquivo
	./prerequisites.sh # Irá instalar as dependencias do projeto
	chmod +x ./backend.sh # Irá dar permissão de execução para o arquivo
	./backend.sh # Irá instalar as dependencias do projeto
```
#### Python Dependencies:
Agora que você já tem o Python 3.7.17 instalado e as dependencias do Dagster, abra um terminal novo e execute os comandos abaixo para iniciar o Dagster.

```shell
	cd Dagster-Educacao # Irá entrar na pasta do projeto
	pyenv activate dagster-dtwy # Irá ativar o ambiente virtual do Python
	make dependencies # Irá instalar o pandas, matplotlib, seaborn e scikit-learn
```

## How to Run:
Neste ponto, você pode abrir a IU do Dagster e ver a execução do código.
```shell
clear; dagster dev -h 0.0.0.0 -p 3000 # Irá iniciar a IU do Dagster
```
