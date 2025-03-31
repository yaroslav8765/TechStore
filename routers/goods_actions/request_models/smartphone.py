from pydantic import BaseModel
from typing import  Optional
from ....models import Smartphones

class AddEditSmartphoneRequest(BaseModel):
    Display_diagonal: float
    Screen_resolution: str
    Screen_type: Optional[str] = None
    Screen_refresh_rate: Optional[str] = None
    Communication_standards: str
    Number_of_SIM_cards: int
    SIM_card_size: str
    e_SIM_support: bool
    Processor_Model: Optional[str] = None
    Number_of_Cores: Optional[int] = None
    RAM: Optional[str] = None
    Built_in_Memory: str
    Expandable_Memory: Optional[str] = None
    Main_camera: Optional[str] = None
    Front_camera: Optional[str] = None
    Maximum_video_resolution: Optional[str] = None
    Stabilization: Optional[str] = None
    Wi_Fi_Standards: Optional[str] = None
    Bluetooth: Optional[str] = None
    Navigation_System: Optional[str] = None
    NFC: Optional[bool] = None
    USB_Interface: Optional[str] = None
    Battery_capacity: Optional[str] = None
    Height: int
    Width: int
    Depth: int
    Weight: int
    Manufacturer_color: str
    Warranty_period: str
    Country_of_manufacture: str
    Brand: str

    class Config:
        json_schema_extra = {
            "example": {
                "Display_diagonal": -1,
                "Screen_resolution": "Empty",
                "Screen_type": "Empty",
                "Screen_refresh_rate": "Empty",
                "Communication_standards": "Empty",
                "Number_of_SIM_cards": -1,
                "SIM_card_size": "Empty",
                "e_SIM_support": False,
                "Processor_Model": "Empty",
                "Number_of_Cores": -1,
                "RAM": "Empty",
                "Built_in_Memory": "Empty",
                "Expandable_Memory": "Empty",
                "Main_camera": "Empty",
                "Front_camera": "Empty",
                "Maximum_video_resolution": "Empty",
                "Stabilization": "Empty",
                "Wi_Fi_Standards": "Empty",
                "Bluetooth": "Empty",
                "Navigation_System": "Empty",
                "NFC": False,
                "USB_Interface": "Empty",
                "Battery_capacity": "Empty",
                "Height": -1,
                "Width": -1,
                "Depth": -1,
                "Weight": -1,
                "Manufacturer_color": "Empty",
                "Warranty_period": "Empty",
                "Country_of_manufacture": "Empty",
                "Brand": "Empty"
            }
        }

def add_smartphones_model(characteristics_request: AddEditSmartphoneRequest, new_goods_id:int):
        model = Smartphones(
        goods_id                            = new_goods_id,
        Display_diagonal                    = characteristics_request.Display_diagonal,
        Screen_resolution                   = characteristics_request.Screen_resolution,
        Screen_type                         = characteristics_request.Screen_type,
        Screen_refresh_rate                 = characteristics_request.Screen_refresh_rate,
        Communication_standards             = characteristics_request.Communication_standards,
        Number_of_SIM_cards                 = characteristics_request.Number_of_SIM_cards,
        SIM_card_size                       = characteristics_request.SIM_card_size,
        e_SIM_support                       = characteristics_request.e_SIM_support,
        Processor_Model                     = characteristics_request.Processor_Model,
        Number_of_Cores                     = characteristics_request.Number_of_Cores,
        RAM                                 = characteristics_request.RAM,
        Built_in_Memory                     = characteristics_request.Built_in_Memory,
        Expandable_Memory                   = characteristics_request.Expandable_Memory,
        Main_camera                         = characteristics_request.Main_camera,
        Front_camera                        = characteristics_request.Front_camera,
        Maximum_video_resolution            = characteristics_request.Maximum_video_resolution,
        Stabilization                       = characteristics_request.Stabilization,
        Wi_Fi_Standards                     = characteristics_request.Wi_Fi_Standards,
        Bluetooth                           = characteristics_request.Bluetooth,
        Navigation_System                   = characteristics_request.Navigation_System,
        NFC                                 = characteristics_request.NFC,
        USB_Interface                       = characteristics_request.USB_Interface,
        Battery_capacity                    = characteristics_request.Battery_capacity,
        Height                              = characteristics_request.Height,
        Width                               = characteristics_request.Width,
        Depth                               = characteristics_request.Depth,
        Weight                              = characteristics_request.Weight,
        Manufacturer_color                  = characteristics_request.Manufacturer_color,
        Warranty_period                     = characteristics_request.Warranty_period,
        Country_of_manufacture              = characteristics_request.Country_of_manufacture,
        Brand                               = characteristics_request.Brand,
        )
        
        return model


def edit_smartphone_model(goods_request: AddEditSmartphoneRequest, old_good: Smartphones):
    update_fields = {
        "Display_diagonal": -1,
                "Screen_resolution": "Empty",
                "Screen_type": "Empty",
                "Screen_refresh_rate": "Empty",
                "Communication_standards": "Empty",
                "Number_of_SIM_cards": -1,
                "SIM_card_size": "Empty",
                "e_SIM_support": None,
                "Processor_Model": "Empty",
                "Number_of_Cores": -1,
                "RAM": "Empty",
                "Built_in_Memory": "Empty",
                "Expandable_Memory": "Empty",
                "Main_camera": "Empty",
                "Front_camera": "Empty",
                "Maximum_video_resolution": "Empty",
                "Stabilization": "Empty",
                "Wi_Fi_Standards": "Empty",
                "Bluetooth": "Empty",
                "Navigation_System": "Empty",
                "NFC": None,
                "USB_Interface": "Empty",
                "Battery_capacity": "Empty",
                "Height": -1,
                "Width": -1,
                "Depth": -1,
                "Weight": -1,
                "Manufacturer_color": "Empty",
                "Warranty_period": "Empty",
                "Country_of_manufacture": "Empty",
                "Brand": "Empty",
    }

    for field, empty_value in update_fields.items():
        new_value = getattr(goods_request, field, empty_value)
        if new_value != empty_value:
            setattr(old_good, field, new_value)

    return old_good