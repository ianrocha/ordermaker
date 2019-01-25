import os
import random


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(filename, model):
    new_filename = random.randint(1, 39010209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{}{}'.format(new_filename, ext)
    if model == 'clients':
        return 'clients/{}/{}'.format(new_filename, final_filename)
    else:
        return 'products/{}/{}'.format(new_filename, final_filename)


def validate_quantity(quantity, default_quantity):
    result = quantity % default_quantity
    if result != 0:
        return False
    return True


def validate_profitability(profitability):
    if profitability == 'Bad':
        return False
    return True
