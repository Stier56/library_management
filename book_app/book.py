from dataclasses import dataclass
import string

@dataclass
class Book:
    title: string="NoData"
    author: string="NoData"
    isbn: string="NoData"
    publisher: string="NoData"
    storage: string="NoData"
    description: string="NoData"
    thumbnail: string="static/images/no_image.png"
        


        
