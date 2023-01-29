#!/usr/bin/python
# libs
import requests
# default
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-W', dest='wallet', type=str, help='Portfel do sprawdzenia')
args = parser.parse_args()


class Config:
    batchSize = 100
    offset = 100
    walletAddress = args.wallet
    wallet_id = None
    optionsString = 'Wybierz: \n[1] wyjdź z programu \n[2] sprawdź portfel w blockchain.info \n[3] ustaw nowy adres \n[4] ustaw głębokość przeszukiwania transakcji\n'
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
        print('!!! BŁĄD !!!')
        exit(127)
        return []


def walletexplorer_loop_n(n):
    print('pobieranie danych...')
    db = []
    time.sleep(1)
    for x in range(0, n, 100):
        time.sleep(1)
        data = check_transactions_walletexplorer(x)
        print(f'pobieranie danych dla transakcji {x}-{x + 100} z {n}')
        db.extend(data)

    save_file(s.walletAddress, db)



def get_address_data():

    print('pobieranie danych...')
    r = requests.get(f'https://blockchain.info/rawaddr/{s.walletAddress}?limit=0')
    wallet_id = requests.get(
        f'http://www.walletexplorer.com/api/1/address-lookup?address={s.walletAddress}&caller=test').json()

    if r.status_code == 404 or not wallet_id['found']:
        print("\nNie znaleziono adresu!!! \n")
        exit(127)
    else:
        s.data = r.json()
        print(s.data)
        s.wallet_id = wallet_id['wallet_id']

        print()
        _input = input(
            f'znaleziono {s.data["n_tx"]} transakcji, wybierz: \n[1] sprawdź wszystkie (UWAGA: może być powolne!) \n[2] sprawdź ograniczoną ilość (podaj liczbę) \n[3] wyjdź z programu \nWybór: ')
        if _input == '1':
            walletexplorer_loop_n(s.data["n_tx"])
        if _input == '2':
            x= int(input('podaj ilość transakcji do przeszukania: '))
            walletexplorer_loop_n(x)

def save_file(file_name, data):
        print(f'zapisywanie do pliku {file_name}.txt')
        out = list(map(lambda x: f'tx {x["txid"]} [W]: ' +" ".join( list(map(lambda y: f'{y["label"]} ', x['outputs']))), data ))
        with open(f'{file_name}.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(out))


if args.wallet is not None:
    get_address_data()
else:
    print("Błąd: brak adresu do sprawdzenia. \nPodaj adres do sprawdzenia w argumencie -W.\nPrzykład: ./script.py -W 1AXZ1SwA2uW2cYoKmH23XgDyWGdEf3RwRB")
    exit(127)

