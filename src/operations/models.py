from sqlalchemy import Column, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

operation = Table(
    'operation',
    Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('quantity', String),
    Column('figi', String),
    Column('type', String),
    Column('date', DateTime),
)

