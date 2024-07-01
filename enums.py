from enum import Enum

class ListingStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    SOLD = "Sold"

class OrderStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    CANCELED = "Canceled"