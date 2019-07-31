# -*- coding: utf-8 -*-
from waitress import serve
from app import application

def run():
    return serve(application)