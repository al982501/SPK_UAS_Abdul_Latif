from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Mobil(Base):
    __tablename__ = "tb_mobil"
    no = Column(Integer, primary_key=True)
    nama_mobil = Column(String)
    harga = Column(Integer)
    warna = Column(String)
    merk = Column(String)
    tahun_rilis = Column(String) 
    garansi = Column(String) 

    def __repr__(self):
        return f"Mobil(type={self.type!r}, nama_mobil={self.nama_mobil!r}, harga={self.harga!r}, warna={self.warna!r}, merk={self.merk!r}, tahun_rilis={self.tahun_rilis!r}, garansi={self.garansi!r})"