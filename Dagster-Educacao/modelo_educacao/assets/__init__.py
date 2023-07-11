# TODO: Dagster cloud - Igor e Reginaldo.
    # Se funcionar, pegar o exemplo de classificação (forecast).
    # Dagster cloud tá rodando no python 3.7.17
# TODO: Olhar imagens 4 e 5, pois estão erradas.
# TODO: Criar um asset para cada imagem.
# TODO: Auto materializar assets.
# TODO: dagster venv - Anselmo e Reginaldo.
# TODO: Comment everything.

import os # For creating folders
import pandas as pd # For data manipulation
import matplotlib.pyplot as plt # For plotting
import seaborn as sns # For plotting
from sklearn.linear_model import LinearRegression # For regression
from dagster import asset, op, job, Out, AssetMaterialization # For dagster
from dotenv import load_dotenv
# import the /DTWModules/dtwdatabase.py class that is named DTWDataBase
# from modelo_educacao.DTWModules import DTWDataBase
from ..dataBaseModule.database import DataBase

load_dotenv(dotenv_path=r".env")

@asset
def read_escolas_csv(context):
    escolas = pd.read_csv('modelo_educacao/data/mview_escolas_202302271652.csv', sep=';')
    len_escolas = len(escolas)
    # print(escolas.head())
    return escolas

@op
def validate_output_folder(context):
    if not os.path.exists('./modelo_educacao/output'):
        os.makedirs('./modelo_educacao/output')

@op
def analyze_fundamental_qtd(context, escolas):
    sns.boxplot(data=escolas, x="bairro_zona", y="fundamental_qtd")
    plt.savefig('./modelo_educacao/output/01-fundamental_qtd_boxplot.png')
    plt.close()
    fundamental_qtd_desc = escolas["fundamental_qtd"].describe().to_dict()

@op
def analyze_infantil_qtd(context, escolas):
    sns.boxplot(data=escolas, x="bairro_zona", y="infantil_qtd")
    plt.savefig('./modelo_educacao/output/02-infantil_qtd_boxplot.png')
    plt.close()
    infantil_qtd_desc = escolas["infantil_qtd"].describe().to_dict()

@op
def filter_data(context, escolas):
    fund = escolas[["fundamental_qtd","bairro_zona"]].copy()
    fund["tipo"] = "fundamental"
    # create a pandas dataframe with fund
    fund = pd.DataFrame(fund)
    fund.columns = ["qtd", "bairro_zona", "tipo"]

    inf = escolas[["infantil_qtd","bairro_zona"]].copy()
    inf["tipo"] = "infantil"
    inf.columns = ["qtd", "bairro_zona", "tipo"]

    df = pd.concat([inf, fund], ignore_index=True)
    # save the df into an image
    sns.boxplot(data=df, x="bairro_zona", y="qtd", hue="tipo")
    plt.savefig('./modelo_educacao/output/03-combined_qtd_boxplot.png')
    return df
    # yield AssetMaterialization(asset_key='filtered_data', description='Filtered data', metadata={'length': len(df)})
    # yield Out(value=df, asset_key='filtered_data')

@op
def analyze_combined_qtd(context, filtered_data):
    # sns.boxplot(data=filtered_data, x="bairro_zona", y="qtd", hue="tipo")
    sns.boxplot(data=filtered_data, x="bairro_zona", y="qtd")
    plt.savefig('./modelo_educacao/output/04-combined_qtd_boxplot.png')
    plt.close()
    combined_qtd_desc = filtered_data.describe().to_dict()
    print(combined_qtd_desc)
    # yield AssetMaterialization(asset_key='combined_qtd_boxplot', description='Boxplot of combined qtd', metadata={'statistics': combined_qtd_desc})

@op
def analyze_fundamental_only(context, escolas):
    fundamental_only = escolas[escolas['modalidade_fund']]
    # yield AssetMaterialization(asset_key='fundamental_only', description='Fundamental only data', metadata={'length': len(fundamental_only)})
    # yield Out(value=fundamental_only, asset_key='fundamental_only')

@op
def analyze_infantil_only(context, escolas):
    infantil_only = escolas[escolas['modalidade_inf']]
    return infantil_only
    # yield AssetMaterialization(asset_key='infantil_only', description='Infantil only data', metadata={'length': len(infantil_only)})
    # yield Out(value=infantil_only, asset_key='infantil_only')

@op
def analyze_infantil_prof_aux_corr(context, infantil_only):
    infantil_only = infantil_only.fillna(0)
    infantil_only = infantil_only.astype({'auxiliares_qtd':'int'})
    infantil_only = infantil_only.astype({'professores_qtd':'int'})
    sns.scatterplot(data=infantil_only, x="professores_qtd", y="auxiliares_qtd")
    plt.savefig('./modelo_educacao/output/05-infantil_prof_aux_corr_scatterplot.png')
    plt.close()
    corr_value = infantil_only["professores_qtd"].corr(infantil_only["auxiliares_qtd"], method='spearman')
    # yield AssetMaterialization(asset_key='infantil_prof_aux_corr_scatterplot', description='Scatterplot of infantil professors vs auxiliares', metadata={'correlation': corr_value})

@op
def analyze_infantil_prof_aux_regression(context, infantil_only):
    infantil_only = infantil_only.fillna(0)
    infantil_only = infantil_only.astype({'auxiliares_qtd':'int'})
    infantil_only = infantil_only.astype({'professores_qtd':'int'})
    X = infantil_only["professores_qtd"].values.reshape(-1, 1)
    y = infantil_only["auxiliares_qtd"].values.reshape(-1, 1)
    regressor = LinearRegression()
    regressor.fit(X, y)
    plt.scatter(X, y, color='g')
    plt.plot(X, regressor.predict(X), color='k')
    plt.savefig('./modelo_educacao/output/06-infantil_prof_aux_regression.png')
    plt.close()
    r_sq = regressor.score(X, y)
    coefficient = regressor.coef_[0][0]
    # yield AssetMaterialization(asset_key='infantil_prof_aux_regression', description='Regression of infantil professors vs auxiliares', metadata={'coefficient': coefficient, 'r_squared': r_sq})

@job
def data_analysis_pipeline():
    db = DataBase()
    db.connect()
    escolas = read_escolas_csv()
    validate_output_folder()
    analyze_fundamental_qtd(escolas) # 1º Image
    analyze_infantil_qtd(escolas) # 2º Image
    filtered_data = filter_data(escolas) # 3º Image
    analyze_combined_qtd(filtered_data) # 4º Image
    analyze_fundamental_only(escolas)
    result = analyze_infantil_only(escolas)
    analyze_infantil_prof_aux_corr(result)
    analyze_infantil_prof_aux_regression(result) # 6º Image

result = data_analysis_pipeline.execute_in_process()
