# libs
import requests
# default
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-W', dest='wallet', type=str, help='Add wallet')
args = parser.parse_args()


class Config:
    batchSize = 100
    offset = 100
    walletAddress = args.wallet
    wallet_id = None
    optionsString = 'Enter: \n1. to quit \n2. to check wallet in blockchain info \n3.to set new address \n4. to set new depth\n'
    data = None


s = Config()


def check_transactions_walletexplorer(offset):
    r = requests.get(
        f'http://www.walletexplorer.com/api/1/wallet?wallet={s.wallet_id}&from={offset}&count=100&caller=panerurkar_p16@ce.vjti.ac.in')
    try:
        data = r.json()['txs']
        data = list(filter(lambda d: ('outputs' in d.keys()), data))
        if len(data) != 0:
            for i in range(len(data)):
                data[i]['outputs'] = list(filter(lambda x: ('label' in x.keys()), data[i]['outputs']))
        data = list(filter(lambda d: (len(d['outputs']) != 0), data))
        return data

    except:
        print('error happened')
        return []


def walletexplorer_loop_n(n):
    print('starting download...')
    db = []
    time.sleep(1)
    for x in range(0, n, 100):
        time.sleep(1)
        data = check_transactions_walletexplorer(x)
        print(f'downloading data for transactions {x}-{x + 100} of {n}')
        db.extend(data)

    save_file(s.walletAddress, db)



def get_address_data():

    print('downloading data...')
    r = requests.get(f'https://blockchain.info/rawaddr/{s.walletAddress}?limit=0')
    wallet_id = requests.get(
        f'http://www.walletexplorer.com/api/1/address-lookup?address={s.walletAddress}&caller=test').json()

    if r.status_code == 404 or not wallet_id['found']:
        print("\nAddress not found!!! \n")
    else:
        s.data = r.json()
        print(s.data)
        s.wallet_id = wallet_id['wallet_id']

        print()
        _input = input(
            f'found {s.data["n_tx"]} transactions 1. check all 2. check  limited amount (provide number) 3. quit ')
        if _input == '1':
            walletexplorer_loop_n(s.data["n_tx"])
        if _input == '2':
            x= int(input('provide number: \n'))
            walletexplorer_loop_n(x)

def save_file(file_name, data):
        print(f'saving to file {file_name}.txt')
        out = list(map(lambda x: f'tx {x["txid"]} [W]: ' +" ".join( list(map(lambda y: f'{y["label"]} ', x['outputs']))), data ))
        with open(f'{file_name}.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(out))


if args.wallet is not None:
    get_address_data()

