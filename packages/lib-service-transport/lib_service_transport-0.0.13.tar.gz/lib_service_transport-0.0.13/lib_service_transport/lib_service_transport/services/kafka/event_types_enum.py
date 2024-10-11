from enum import Enum


class EventTypeEnum(str, Enum):
    SALES_ORDER = 'sales_order'
    ORGANIZATION = 'organization'
