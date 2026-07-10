from enum import Enum


class InventoryStrategy(str, Enum):
    FIFO = "FIFO"
    FEFO = "FEFO"
    BATCH = "BATCH"