import model_library
from model_library.library import ModelLibrary

if __name__ == "__main__":
    model_library = ModelLibrary()
    model_library.auto_register()

    # Convert to dictionary
    print(model_library.to_dict())
