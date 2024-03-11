from .modelscope import ModelScope
from .zeroscope import ZeroScope


ALL_MODELS = [
    ModelScope,
    ZeroScope
]

ALL_MODEL_NAMES = [model.__name__ for model in ALL_MODELS]

def print_all_model_names():
    print("ALL_MODEL_NAMES:", ALL_MODEL_NAMES)

def get_model_class(model_name):
    """ Returns the model class corresponding to the provided model_name. """
    assert model_name in ALL_MODEL_NAMES, f"model_name must be one of {ALL_MODEL_NAMES}"
    return ALL_MODELS[ALL_MODEL_NAMES.index(model_name)]