#!/usr/bin/python3
"""
Contains the Website class
"""

import models
from models.base_model import BaseModel, Base
import random
import string
import sqlalchemy
from sqlalchemy import Column, String
import uuid


class Website(BaseModel, Base):
    """Representation of a website"""
    __tablename__ = 'website'
    name = Column(String(500), nullable=False)
    short_url = Column(String(8), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes the website"""
        super().__init__(*args, **kwargs)
        short_url = ''.join(random.choice(string
                                          .ascii_letters + string.digits)
                            for _ in range(8))
        self.short_url = short_url
