# libs
import requests
# default
import math
# local
import settings


s = settings.Config()
offset = s.batchSize
data = None

def check_transactions_(tx_num):
    pass
    # x = input('chose option: \n')
# print(
#     f'checking transactions in page {round(offset/s.batchSize)} of {math.ceil(tx_num/s.batchSize)}')


def call_blockchain_info():
    print('downloading data...')
    r = requests.get(f'https://blockchain.info/rawaddr/{s.walletAddress}?limit=0')

    if r.status_code == 404:
        print("\nAddress not found!!! \n")
    else:
        global data
        data = r.json()
        print('\ndata:')
        print(f'Status code: {r.status_code}')
        print(f'n of transactions {data["n_tx"]}')
        # print(len(r.json()['txs']))
        x = input('check transactions in x [y]/[N]\n')
        if x == 'y':
            check_transactions_(data["n_tx"])


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
        call_blockchain_info()
    elif _input == '3':
        set_address()
    elif _input == '4':
        set_depth()
    elif _input == '5':
        check_transactions_(5)