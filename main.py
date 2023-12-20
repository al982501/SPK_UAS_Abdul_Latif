from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api
from models import Mobil as MobilModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from tabulate import tabulate

session = Session(engine)

app = Flask(__name__)
api = Api(app)


class BaseMethod():

    def __init__(self):
        self.raw_weight = {'harga': 9, 'warna':9,'merk': 8, 
                           'tahun_rilis': 7, 'garansi': 6}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(MobilModel.no, MobilModel.nama_mobil, MobilModel.harga, MobilModel.warna,
                       MobilModel.merk, MobilModel.tahun_rilis, MobilModel.garansi)
        result = session.execute(query).fetchall()
        print(result)
        return [{'no':  Mobil.no,'nama_mobil': Mobil.nama_mobil, 'harga': Mobil.harga,
                'warna': Mobil.warna, 'merk': Mobil.merk, 'tahun_rilis': Mobil.tahun_rilis, 'garansi': Mobil.garansi} for Mobil in result]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        nama_mobil_values = [] # max
        harga_values = []  # min
        warna_values = []  # max
        merk_values = []  # max
        tahun_rilis_values = []  # max
        garansi_values = []  # max

        for data in self.data:
            # Nama_Mobil
            nama_mobil = data['nama_mobil']
            numeric_values = [int(value.split()[0]) for value in nama_mobil.split(
                ',') if value.split()[0].isdigit()]
            max_nama_mobil_value = max(numeric_values) if numeric_values else 1
            nama_mobil_values.append(max_nama_mobil_value)

            # Harga
            harga_values.append(int(data['harga']))

            # warna
            warna = data['warna']
            warna_numeric_values = [int(
                value.split()[0]) for value in warna.split() if value.split()[0].isdigit()]
            max_warna_value = max(
                warna_numeric_values) if warna_numeric_values else 1
            warna_values.append(max_warna_value)

            # Merk
            merk = data['merk']
            merk_numeric_values = [float(value.split()[0]) for value in merk.split(
            ) if value.replace('.', '').isdigit()]
            max_merk_value = max(
                merk_numeric_values) if merk_numeric_values else 1
            merk_values.append(max_merk_value)

            # Garansi
            garansi = data['garansi']
            garansi_numeric_values = [
                int(value) for value in garansi.split() if value.isdigit()]
            max_garansi_value = max(
                garansi_numeric_values) if garansi_numeric_values else 1
            garansi_values.append(max_garansi_value)
            
            # tahun_rilis
            tahun_rilis = data['tahun_rilis']
            tahun_rilis_numeric_values = [
                int(value) for value in tahun_rilis.split() if value.isdigit()]
            max_tahun_rilis_value = max(
                tahun_rilis_numeric_values) if tahun_rilis_numeric_values else 1
            tahun_rilis_values.append(max_tahun_rilis_value)

        return [
    {
        'no': data['no'],
        'nama_mobil': nama_mobil_value / max(nama_mobil_values),
        'harga': int(data['harga']) / max(harga_values) if max(harga_values) != 0 else 0,
        'warna': warna_value / max(warna_values),
        'merk': merk_value / max(merk_values),
        'tahun_rilis': tahun_rilis_value / max(tahun_rilis_values),
        'garansi': garansi_value / max(garansi_values),
    }
    for data, nama_mobil_value, harga_value, warna_value, merk_value, tahun_rilis_value, garansi_value
    in zip(self.data, nama_mobil_values, harga_values, warna_values, merk_values, tahun_rilis_values, garansi_values)
]


    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

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
                row['garansi']**self.weight['garansi'],
                'nama_mobil': row.get('nama_mobil', '')
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'ID': product['no'],
                'score': round(product['produk'], 3)
            }
            for product in sorted_produk
        ]
        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return sorted(result, key=lambda x: x['score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'mobil': sorted(result, key=lambda x: x['score'], reverse=True)}, HTTPStatus.OK.value


class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = [
            {
                'ID': row['no'],
                'Score': round(row['harga'] * weight['harga'] +
                               row['warna'] * weight['warna'] +
                               row['merk'] * weight['merk'] +
                               row['tahun_rilis'] * weight['tahun_rilis'] +
                               row['garansi'] * weight['garansi'], 3)
            }
            for row in self.normalized_data
        ]
        sorted_result = sorted(result, key=lambda x: x['Score'], reverse=True)
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return sorted(result, key=lambda x: x['Score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'mobil': sorted(result, key=lambda x: x['Score'], reverse=True)}, HTTPStatus.OK.value


class   Mobil(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None

        if page > page_count or page < 1:
            abort(404, description=f'Data Tidak Ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next_page,
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = session.query(MobilModel).order_by(MobilModel.no)
        result_set = query.all()
        data = [{'no': row.no, 'nama_mobil': row.nama_mobil, 'harga': row.harga,
                 'warna': row.warna, 'merk': row.merk, 'tahun_rilis': row.tahun_rilis, 'garansi': row.garansi}
                for row in result_set]
        return self.get_paginated_result('mobil/', data, request.args), 200


api.add_resource(Mobil, '/mobil')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)