# libs
import requests
# default
import math
# local
import settings

###some
import io
import pandas as pd
import requests
import json
import csv
import time

s = settings.Config()
offset = s.batchSize
data = None

def check_transactions_(tx_num):
    print(f'found {tx_num} transactions. What you wish to do?\n1. To cancel \n2. Check all transactions in depth {s.depth} \n3. check batch of {s.batchSize} in {s.depth} depth')
    r_bytes = requests.get('https://www.walletexplorer.com/wallet/4f2bef8f274a0e23?from_address=bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h&format=csv')
    print("finished download")
    print(r_bytes.encoding)
    # r = r_bytes.decode('utf8')
    r = r_bytes.text
    print("finished decode")

    start_df_timestamp = time.time()
    df = pd.read_csv(io.StringIO(r), sep=";")
    result_df = json.dumps(df.to_dict('records'))
    end_df_timestamp = time.time()
    print("The df method took {d_t}s".format(d_t=end_df_timestamp - start_df_timestamp))

    start_csv_reader_timestamp = time.time()
    reader = csv.DictReader(io.StringIO(r))
    result_csv_reader =json.loads( json.dumps(list(reader)))
    end_csv_reader_timestamp = time.time()
    print("The csv-reader method took {d_t}s".format(d_t=end_csv_reader_timestamp - start_csv_reader_timestamp))
    print(type(result_csv_reader[0]))
    # x = input('chose option: \n')
# print(
#     f'checking transactions in page {round(offset/s.batchSize)} of {math.ceil(tx_num/s.batchSize)}')


def call_blockchain_info():
    print('downloading data...')
    r = requests.get(f'https://blockchain.info/rawaddr/{s.walletAddress}?limit={s.batchSize}&offset={offset}')

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