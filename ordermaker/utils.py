import os
import random


def get_filename_ext(filepath):
    """
    Receive a filepath; get and separate the original file name
    from the extension and return both
    :param filepath: the directory from where the file is inputted
    :return: the original file name and the extension
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(filename, model):
    """
    Receive a file name and a model name and return a new name with the local of the file
    :param filename: Name of the file
    :param model: Name of the model
    :return: New name and local of the file
    """
    new_filename = random.randint(1, 39010209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{}{}'.format(new_filename, ext)
    if model == 'clients':
        return 'clients/{}/{}'.format(new_filename, final_filename)
    else:
        return 'products/{}/{}'.format(new_filename, final_filename)


def validate_quantity(quantity, default_quantity):
    """
    Verifies if 'quantity' is multiple of 'default_quantity
    :param quantity: Value inputted by user
    :param default_quantity: Default value of the system
    :return: True or False
    """
    result = quantity % default_quantity
    if result != 0:
        return False
    return True


def validate_profitability(profitability):
    """
    Verifies if 'profitability' is 'Bad'
    :param profitability: Value inputted by user
    :return: True or False
    """
    if profitability == 'Bad':
        return False
    return True
