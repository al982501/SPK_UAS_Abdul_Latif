USER = 'postgres'
PASSWORD = 'admin'
HOST = 'localhost'
PORT = '5432'
DATABASE_NAME = 'db_spk'

DEV_SCALE = {
    'harga': {
        '5000000000 - 6000000000': 1,
        '1420000000 - 1945000000': 2, 
        '609000000 -  1350000000': 3, 
        '288000000 -  577600000': 4, 
        '207000000 -  235000000': 1, 
    },
    'warna': {
        'hitam': 5, 
        'putih': 4, 
        'merah': 3, 
        'biru': 2, 
        'hijau': 1,
    },
    'merk': {
        'bmw': 5,
        'daihatsyu': 4,
        'mitsubishi': 3,
        'toyota' : 2,
        'honda' : 1,
    },
    'tahun_rilis' : {
        '2023': 5,
        '2022': 4,
        '2021' : 3,
        '2020' : 2,
        '2019' : 1,
    },
    'garansi' : {
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
        '1': 1,
    },
}