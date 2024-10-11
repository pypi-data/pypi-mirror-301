from pathlib import Path

from halerium_utilities.prompt.functions import register_function


REGISTRY = {
    # "my_function": {  # name of the function
    #     "file": "my_function.py",
    #     "function": "func",  # what it says after `def:`
    # }
    "get_docx_placeholders": {
        "file": "docx_templates.py",
        "function": "get_docx_placeholders"
    },
    "fill_docx_template": {
        "file": "docx_templates.py",
        "function": "fill_docx_template"
    },
    "get_pptx_placeholders": {
        "file": "pptx_templates.py",
        "function": "get_pptx_placeholders"
    },
    "fill_pptx_template": {
        "file": "pptx_templates.py",
        "function": "fill_pptx_template"
    },
    "load_website": {
        "file": "web_crawler_functions.py",
        "function": "load_website"
    }
}


def activate_function(name, config_parameters={}):

    if name not in REGISTRY:
        raise NotImplementedError(f"The function {name} is not contained in the library of this runner.")

    for cp in REGISTRY[name].get("config_parameters", {}):
        if cp not in config_parameters:
            raise ValueError(f"Config parameter {cp} has to be provided.")

    full_path = Path(__file__).parent.resolve() / "library" / REGISTRY[name]["file"]

    register_function(full_path, REGISTRY[name]["function"], name)


def activate_all_functions():
    for name in REGISTRY:
        activate_function(name)
