from pathlib import Path

from halerium_utilities.prompt.functions.custom_service import prepare_register


REGISTRY = {
    # "my_function": {  # name of the function
    #     "file": "my_function.py",
    #     "function": "func",  # what it says after `def:`
    # }
    "get_docx_placeholders": {
        "file_path": "docx_templates.py",
        "function": "get_docx_placeholders",
    },
    "fill_docx_template": {
        "file_path": "docx_templates.py",
        "function": "fill_docx_template",
    },
    "get_pptx_placeholders": {
        "file_path": "pptx_templates.py",
        "function": "get_pptx_placeholders",
    },
    "fill_pptx_template": {
        "file_path": "pptx_templates.py",
        "function": "fill_pptx_template",
    },
    "load_website": {
        "file_path": "web_crawler_functions.py",
        "function": "load_website",
    }
}


def get_full_registry():
    full_registry = {}
    for function_name, params in REGISTRY.items():
        file_path = Path(__file__).parent.resolve() / "library" / params["file_path"]
        function = params["function"]
        full_spec = prepare_register(file_path=file_path, function=function, function_name=function_name,
                                     allow_gpt=False)
        full_registry[function_name] = full_spec
    return full_registry

