# libs
import requests
# default
import math
import json


class Config:
    depth = 1
    batchSize = 100
    walletAddress = 'bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h'
    wallet_id = None
    optionsString = 'Enter: \n1. to quit \n2. to check wallet in blockchain info \n3.to set new address \n4. to set new depth\n'
    data = None

s = Config()
offset = s.batchSize


def check_transactions_walletexplorer():
    print(s.wallet_id)
    r = requests.get(f'http://www.walletexplorer.com/api/1/wallet?wallet={s.wallet_id}&from=0&count=100&caller=panerurkar_p16@ce.vjti.ac.in')
    data = r.json()['txs']
    data = list(filter(lambda d: ('outputs' in d.keys()), data))
    if len(data) != 0:
        for i in range(len(data)):
            data[i]['outputs'] = list(filter(lambda x: ('label' in x.keys()), data[i]['outputs']))
    data = list(filter(lambda d: (len(d['outputs']) != 0), data))
    # print(data)
    # print(json.dumps(data))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    # print(data)
    # if len(data) != 0:
    #     for i in range(len(data)):
    #         if 'outputs' in data[i].keys():
    #             print(data[i]['outputs'])
    #         pass

        # print(list(filter(lambda d: ('outputs' in d.keys()), data)))
        # result = list(filter(lambda x: (x % 13 == 0), my_list))
        # print(r.json()['txs'])



def get_address_data():
    print('downloading data...')
    r = requests.get(f'https://blockchain.info/rawaddr/{s.walletAddress}?limit=0')
    wallet_id = requests.get(f'http://www.walletexplorer.com/api/1/address-lookup?address={s.walletAddress}&caller=test').json()


    if r.status_code == 404 or not wallet_id['found']:
        print("\nAddress not found!!! \n")
    else:
        s.data = r.json()
        s.wallet_id = wallet_id['wallet_id']
        print('\ndata:')
        # print(f'Status code: {r.status_code}')
        print(f'n of transactions {s.data["n_tx"]}')
        # print(len(r.json()['txs']))
        # x = input('check transactions in x [y]/[N]\n')
        # if x == 'y':
        #     check_transactions_(s.data["n_tx"])
        check_transactions_walletexplorer()


def set_address():
    s.walletAddress = input('enter address: \n')
def set_depth():
    s.depth = int(input('enter new depth: \n'))

# print(len(r._content))



while (True):
    print(f'Wallet: {s.walletAddress} batch size: {s.batchSize}')
    _input = input(s.optionsString)
    if _input == '1':
        break
    elif _input == '2':
        get_address_data()
    elif _input == '3':
        set_address()
    elif _input == '4':
        set_depth()
    elif _input == '5':
        check_transactions_(5)