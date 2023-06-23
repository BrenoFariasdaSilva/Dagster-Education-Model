#!/bin/bash -i

pyenv install 3.9.16

echo "Python 3.9.16 instalado com sucesso"

pyenv virtualenv 3.9.16 dagster-dtw

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate dagster-dtw

brew install yarn

make dev_install

echo "Make instalado com sucesso!"

dagster dev -h 0.0.0.0 -p 3000

echo "Servidor backend ativo ...."
