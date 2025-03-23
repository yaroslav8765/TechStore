from database import Base
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    phone_number = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

class Smartphones(Base):
    __tablename__ = "smatrpones"

    id = Column(Integer, primary_key=True, index=True)
    Display_diagonal = Column(Float)
    Screen_resolution = Column(String)
    Screen_type = Column(String)
    Screen_refresh_rate = Column(String)
    Communication_standards = Column(String)
    Number_of_SIM_cards = Column(Integer)
    SIM_card_size = Column(String)
    e_SIM_support = Column(Boolean)
    Processor_Model = Column(String)
    Number_of_Cores = Column(Integer)
    RAM = Column(String)
    Built_in_Memory = Column(String)
    Expandable_Memory = Column(String)
    Main_camera = Column(String)
    Front_camera = Column(String)
    Maximum_video_resolution = Column(String)
    Stabilization = Column(String)
    Wi_Fi_Standards = Column(String)
    Bluetooth = Column(String)
    Navigation_System = Column(String)
    NFC = Column(Boolean)
    USB_Interface = Column(String)
    Battery_capacity = Column(String)
    Height = Column(Integer)
    Width = Column(Integer)
    Depth = Column(Integer)
    Weight = Column(Integer)
    Manufacturer_color = Column(String)
    Warranty_period = Column(String) 
    Country_of_manufacture = Column(String)
    Brand = Column(String)