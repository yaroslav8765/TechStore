from pydantic import BaseModel
from typing import  Optional
from ....models import Laptops

class AddEditLaptopRequest(BaseModel):
    Display_diagonal: float
    Screen_resolution: str
    Screen_type: Optional[str] = None
    Screen_refresh_rate: Optional[str] = None
    Processor_Model: str
    Number_of_Cores: int
    RAM: str
    Built_in_Memory: str
    Expandable_Memory: Optional[str] = None
    GPU_Model: Optional[str] = None
    VRAM: Optional[str] = None
    Wi_Fi_Standards: Optional[str] = None
    Bluetooth: Optional[str] = None
    USB_Ports: Optional[str] = None
    HDMI_Port: Optional[bool] = None
    Thunderbolt_Support: Optional[bool] = None
    Battery_capacity: Optional[str] = None
    Battery_life: Optional[str] = None
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
                "Processor_Model": "Empty",
                "Number_of_Cores": -1,
                "RAM": "Empty",
                "Built_in_Memory": "Empty",
                "Expandable_Memory": "Empty",
                "GPU_Model": "Empty",
                "VRAM": "Empty",
                "Wi_Fi_Standards": "Empty",
                "Bluetooth": "Empty",
                "USB_Ports": "Empty",
                "HDMI_Port": None,
                "Thunderbolt_Support": None,
                "Battery_capacity": "Empty",
                "Battery_life": "Empty",
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

def add_laptop_model(characteristics_request: AddEditLaptopRequest, new_goods_id: int):
    model = Laptops(
        goods_id=new_goods_id,
        Display_diagonal=characteristics_request.Display_diagonal,
        Screen_resolution=characteristics_request.Screen_resolution,
        Screen_type=characteristics_request.Screen_type,
        Screen_refresh_rate=characteristics_request.Screen_refresh_rate,
        Processor_Model=characteristics_request.Processor_Model,
        Number_of_Cores=characteristics_request.Number_of_Cores,
        RAM=characteristics_request.RAM,
        Built_in_Memory=characteristics_request.Built_in_Memory,
        Expandable_Memory=characteristics_request.Expandable_Memory,
        GPU_Model=characteristics_request.GPU_Model,
        VRAM=characteristics_request.VRAM,
        Wi_Fi_Standards=characteristics_request.Wi_Fi_Standards,
        Bluetooth=characteristics_request.Bluetooth,
        USB_Ports=characteristics_request.USB_Ports,
        HDMI_Port=characteristics_request.HDMI_Port,
        Thunderbolt_Support=characteristics_request.Thunderbolt_Support,
        Battery_capacity=characteristics_request.Battery_capacity,
        Battery_life=characteristics_request.Battery_life,
        Height=characteristics_request.Height,
        Width=characteristics_request.Width,
        Depth=characteristics_request.Depth,
        Weight=characteristics_request.Weight,
        Manufacturer_color=characteristics_request.Manufacturer_color,
        Warranty_period=characteristics_request.Warranty_period,
        Country_of_manufacture=characteristics_request.Country_of_manufacture,
        Brand=characteristics_request.Brand,
    )
    return model

def edit_laptop_model(goods_request: AddEditLaptopRequest, old_good: Laptops):
    update_fields = {
        "Display_diagonal": -1,
        "Screen_resolution": "Empty",
        "Screen_type": "Empty",
        "Screen_refresh_rate": "Empty",
        "Processor_Model": "Empty",
        "Number_of_Cores": -1,
        "RAM": "Empty",
        "Built_in_Memory": "Empty",
        "Expandable_Memory": "Empty",
        "GPU_Model": "Empty",
        "VRAM": "Empty",
        "Wi_Fi_Standards": "Empty",
        "Bluetooth": "Empty",
        "USB_Ports": "Empty",
        "HDMI_Port": None,
        "Thunderbolt_Support": None,
        "Battery_capacity": "Empty",
        "Battery_life": "Empty",
        "Height": -1,
        "Width": -1,
        "Depth": -1,
        "Weight": -1,
        "Manufacturer_color": "Empty",
        "Warranty_period": "Empty",
        "Country_of_manufacture": "Empty",
        "Brand": "Empty"
    }
    
    for field, empty_value in update_fields.items():
        new_value = getattr(goods_request, field, empty_value)
        if new_value != empty_value:
            setattr(old_good, field, new_value)
    
    return old_good