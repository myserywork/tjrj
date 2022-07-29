from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

user = 'dev'
password = 'NEdPdUtp6iymdvW4Kmu2oVJS9qFhy1BGq8zajyh'
dbname = 'marlandb'
dburl = 'marlan.c5xzwdrzenal.us-east-2.rds.amazonaws.com'

dbstr = f'postgresql://{user}:{password}@{dburl}/{dbname}'

Base = declarative_base()

def getDbSession():
    print('Connecting to database...')
    engine = create_engine(dbstr)

    Session = sessionmaker(bind=engine)
    session = Session()
    print('Database connected!')
    return session

class Processo(Base):
    __tablename__ = 'Processo'
    id = Column(Integer, primary_key=True)
    numero_cnj = Column(String(30))
    numero_antigo = Column(String(20))
    date_dist = Column(Date)
    datetime_in = Column(DateTime)
    segredo = Column(Boolean)
    idoso = Column(Text)
    acao = Column(Text)
    assunto = Column(Text)
    serventia = Column(Text)
    vara = Column(Text)
    rito = Column(Text)
    tipo_recurso = Column(String(50))
    informacoes_autos = Column(Text)
    polo_ativo = Column(Text)
    polo_passivo = Column(Text)
    advogados = Column(Text)
    dividas_ativas = Column(Text)
    movimentos = Column(Text)
    serv_code = Column(String(5))

    def __repr__(self):
        return f'{self.numero_cnj}\t{self.numero_antigo}\t{self.date_dist}'

if __name__ == '__main__':
    engine = create_engine(dbstr)
    Base.metadata.create_all(engine)
