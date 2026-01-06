from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    category: str
    quantity: int
    price: float
    description: str
