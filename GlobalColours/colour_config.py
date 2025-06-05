try:
    from .colour_rgbs import COLOURS as COLOUR_DATA
except ImportError:
    from colour_rgbs import COLOURS as COLOUR_DATA


class ColourConfig:
    """Simple class to enable dot notation access for nested dictionaries"""
    
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively create ColourConfig objects for nested dictionaries
                setattr(self, key, ColourConfig(value))
            else:
                setattr(self, key, value)
    
    def __getitem__(self, key):
        """Allow both dot notation and bracket notation"""
        return getattr(self, key)
    
    def __repr__(self):
        return f"ColourConfig({self.__dict__})"

# Create the COLOURS object with dot notation support
G_COLOURS = ColourConfig(COLOUR_DATA)

if __name__ == '__main__':
    all_colours = ColourConfig(COLOUR_DATA)
    print(all_colours) # prints all the defined colours
