class Location:
    def __init__(self, name, latitude=None, longitude=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None
        
    def __str__(self):
        if self.has_coordinates:
            return f"{self.name} ({self.latitude}, {self.longitude})"
        return f"{self.name} (coordinates not available)"
        
    def __repr__(self):
        return f"Location(name='{self.name}', latitude={self.latitude}, longitude={self.longitude})"
