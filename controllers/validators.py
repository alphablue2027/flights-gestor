# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from models.gestor import FlightsGestor

def is_name_valid(*name : str) -> bool:
    for i in name:
        for j in i.split():
            if not j.isalpha():
                return False
    return True

def is_name_exist(name : str) -> bool:
    return not FlightsGestor.airline_name_exists(name)

def is_fcode_valid(code : str, acode : str) -> bool:
    if not (len(code) >= 3 and code[:2] == acode and code[2:].isdigit()):
        return False
    return True

def is_fcode_exist(code : str) -> bool:
    return not FlightsGestor.flight_code_exists(code)

def is_acode_valid(code : str) -> bool:
    if not (len(code) == 2 and code.isalpha()):
        return False
    return True

def is_acode_exist(code : str) -> bool:
    return not FlightsGestor.airline_code_exists(code)

def is_mm_valid(*text : str) -> bool:
    for i in text:
        if not (len(i) >= 3 and i.isalnum() and i.isascii()):
            return False
    return True