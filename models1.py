from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Mobil(Base):
    __tablename__ = "tb_mobil"
    no = Column(Integer, primary_key=True)
    nama_mobil = Column(String(255))
    harga = Column(String(255))
    warna = Column(String(255))
    merk = Column(String(255))
    tahun_riis = Column(String(255))
    garansi = Column(String(255))

    def __init__(self, no, nama_mobil, harga, warna, merk, tahun_rilis, garansi):
        self.no = no
        self.nama_mobil = nama_mobil
        self.harga = harga
        self.warna = warna
        self.merk = merk
        self.tahun_rilis = tahun_rilis
        self.garansi = garansi

    def calculate_score(self, dev_scale):
        score = 0
        score -= self.harga * dev_scale['harga']
        score += self.warna * dev_scale['warna']
        score += self.merk * dev_scale['merk']
        score += self.tahun_rilis * dev_scale['tahun_rilis']
        score += self.garansi * dev_scale['garansi']
        return score

    def __repr__(self):
        return f"Mobil(no={self.no!r}, nama_mobil={self.nama_mobil!r}, harga={self.harga!r}, warna={self.warna!r}, merk={self.merk!r}, tahun_rilis={self.tahun_rilis!r}, garansi={self.garansi!r})"
