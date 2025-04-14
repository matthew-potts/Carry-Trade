import sys
import argparse
import yaml
import ast
from src.data_client.bond_data_client import BondDataClient
from src.data_client.fx_data_client import FXDataClient

def run_batch(type: str):
    
    if (type == ""):
        load_data()
    elif (type == "analysisOnly"):
        run_analysis()
    else:
        load_data()
        run_analysis()
    
def load_data():

    with open(_CONF_FILE) as stream:
        currencies = ast.literal_eval(yaml.safe_load(stream)['currency_list'])

    # load currencies data
    fx_client = FXDataClient(_CONF_FILE)
    
    for currency in currencies:
        history = fx_client.fetch(currency, '10y')
        fx_client.write(history)

    # load bond data 
    bond_client = BondDataClient(_CONF_FILE)

    for currency in currencies:
        history = bond_client.fetch(f'{currency}.S.1M', '10y')
        bond_client.write(history)
    
    return


def run_analysis():

    raise NotImplementedError()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['full', 'dataOnly', 'analysisOnly'], required=True, help="Choices: full, dataOnly, analysisOnly")
    type = parser.parse_args(sys.argv[1:]).type

    run_batch(type)
