from sqlalchemy import (
    Column,
    create_engine,
    Engine,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List, Optional


# delcarative base ORM class pulls in SQLAlchemy's MetaData construct to all tables
class Base(DeclarativeBase):
    pass


class AciHardware(Base):
    __tablename__ = "aci_hardware"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mac: Mapped[str]
    if_name: Mapped[str]
    ip: Mapped[str]
    node_name: Mapped[str]


class OneViewHardware(Base):
    __tablename__ = "oneview_hardware"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mac: Mapped[str]
    ov_id: Mapped[str]
    appliance_name: Mapped[str]
    bay_number: Mapped[int]
    enclosure_name: Mapped[str]
    ipv4: Mapped[str]
    ipv6: Mapped[Optional[str]]
    serial_num: Mapped[str]


def db_update(aci_entry: dict, ov_entry: dict, debug: bool):
    print("%% Connecting to Postgres")
    postgres_uri = None
    if not debug:
        postgres_uri = "postgresql://postgres:password@postgres/postgres"
    else:
        print("Debug enabled - connecting to internal sqlite database")
        postgres_uri = "sqlite+pysqlite:///:memory:"

    engine = create_engine(postgres_uri, echo=debug)
    metadata_obj = MetaData()
    Base.metadata.create_all(engine)
    db_send_aci(engine, aci_entry)
    db_send_oneview(engine, ov_entry)


def db_send_oneview(engine: Engine, ov_info: dict):
    print("Updating OneView table in Database")
    with Session(engine) as sesh:
        # build our new rows
        for key in ov_info:
            new_entry = OneViewHardware(
                mac=key,
                ov_id=ov_info[key].get("id"),
                appliance_name=ov_info[key].get("applianceName"),
                bay_number=ov_info[key].get("bayNumber"),
                enclosure_name=ov_info[key].get("enclosureName"),
                ipv4=ov_info[key].get("ipv4Addr"),
                ipv6=ov_info[key].get("ipv6Addr"),
                serial_num=ov_info[key].get("serialNumber"),
            )
            sesh.add(new_entry)
        # write our new rows
        sesh.commit()


def db_send_aci(engine: Engine, aci_info: dict):
    print("Updating ACI table in Database")
    with Session(engine) as sesh:
        # build our new rows
        for key in aci_info:
            new_entry = AciHardware(
                mac=key,
                if_name=aci_info[key].get("if_name"),
                ip=aci_info[key].get("ip"),
                node_name=aci_info[key].get("node_name"),
            )
            sesh.add(new_entry)
        # write our new rows
        sesh.commit()
