import sys
from colorama import Fore, Style
from models import Base, Mobil
from engine import engine
from tabulate import tabulate

from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import DEV_SCALE

session = Session(engine)


def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')


def review_data():
    query = select(Mobil)
    for phone in session.scalars(query):
        print(Mobil)


class BaseMethod():

    def __init__(self):
        # 1-5
        self.raw_weight = {'harga': 9, 'warna':9,'merk': 8, 
                           'tahun_rilis': 7, 'garansi': 6}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Mobil.no, Mobil.nama_mobil, Mobil.harga, Mobil.warna,
                       Mobil.merk, Mobil.tahun_rilis, Mobil.garansi)
        result = session.execute(query).fetchall()
        return [{'no': mobil.no, 'nama_mobil': mobil.nama_mobil, 'harga': mobil.harga, 'warna':mobil.   
        warna,
                 'merk': mobil.merk, 'tahun_riis': mobil.tahun_rilis, 'garansi': mobil.garansi} for mobil in result]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        harga_values = []  # min
        warna_values = []  # max
        merk_values = []  # max
        tahun_rilis_values = []  # max
        garansi_values = []  # max

        for data in self.data:
            # Harga
            harga_cleaned = ''.join(
                char for char in data['harga'] if char.isdigit())
            harga_values.append(float(harga_cleaned)
                                if harga_cleaned else 0)  # Convert to float
            
            # Warna
            warna = data['warna']
            numeric_values = [int(value.split()[0]) for value in warna.split(
                ',') if value.split()[0].isdigit()]
            max_warna_value = max(numeric_values) if numeric_values else 1
            warna_values.append(max_warna_value)

            # Merk
            merk = data['merk']
            merk_numeric_values = [int(
                value.split()[0]) for value in merk.split() if value.split()[0].isdigit()]
            max_merk_value = max(
                merk_numeric_values) if merk_numeric_values else 1
            merk_values.append(max_merk_value)

            # Tahun_rilis
            tahun_rilis = data['tahun_rilis']
            tahun_rilis_numeric_values = [
                int(value) for value in tahun_rilis.split() if value.isdigit()]
            max_tahun_rilis_value = max(
                tahun_rilis_numeric_values) if tahun_rilis_numeric_values else 1
            tahun_rilis_values.append(max_tahun_rilis_value)

            # Garansi
            garansi_value = DEV_SCALE['garansi'].get(data['garansi'], 1)
            garansi_values.append(garansi_value)

        return [
            {'no': data['no'],
             'harga': min(harga_value) / max(harga_values) if max(harga_values) != 0 else 0,
             'warna': warna_value / max(warna_values),
             'merk': merk_value / max(merk_values),
             'tahun_rilis': tahun_rilis_value / max(tahun_rilis_values),
             'garansi': garansi_value / max(garansi_values)
             }
            for data, harga_value, warna_value, merk_value, tahun_rilis_value, garansi_value
            in zip(self.data, harga_values, warna_values, merk_values, tahun_rilis_values, garansi_values)
        ]


class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                'no': row['no'],
                'produk': row['harga']**self.weight['harga'] *
                row['warna']**self.weight['warna'] *
                row['merk']**self.weight['merk'] *
                row['tahun_rilis']**self.weight['tahun_rilis'] *
                row['garansi']**self.weight['garansi']
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'no': product['no'],
                'harga': product['produk'] / self.weight['harga'],
                'warna': product['produk'] / self.weight['warna'],
                'merk': product['produk'] / self.weight['merk'],
                'tahun_rilis': product['produk'] / self.weight['tahun_rilis'],
                'garansi': product['produk'] / self.weight['garansi'],
                'score': product['produk']  # Nilai skor akhir
            }
            for product in sorted_produk
        ]
        return sorted_data


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['no']:
                  round(row['harga'] * weight['harga'] +
                        row['warna'] * weight['warna'] +
                        row['merk'] * weight['merk'] +
                        row['tahun_rilis'] * weight['tahun_rilis'] +
                        row['garansi'] * weight['garansi'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result


def run_saw():
    saw = SimpleAdditiveWeighting()
    result = saw.calculate
    print(tabulate(result.items(), headers=['No', 'Score'], tablefmt='pretty'))


def run_wp():
    wp = WeightedProduct()
    result = wp.calculate
    headers = result[0].keys()
    rows = [
        {k: round(v, 4) if isinstance(v, float) else v for k, v in val.items()}
        for val in result
    ]
    print(tabulate(rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == 'create_table':
            create_table()
        elif arg == 'saw':
            run_saw()
        elif arg == 'wp':
            run_wp()
        else:
            print('command not found')
