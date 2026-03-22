import folium
import webbrowser
import math

# ============================================================================
# PART 1: BASE CLASS
# ============================================================================

class Place:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    def get_info(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
    
    def distance_to(self, other_place):
        lat_diff = self.latitude - other_place.latitude
        lon_diff = self.longitude - other_place.longitude
        distance_km = math.sqrt(lat_diff**2 + lon_diff**2) * 111
        return round(distance_km, 2)
    
    def get_marker_color(self):
        return "blue"
    
    def get_popup_text(self):
        return f"<b>{self.name}</b><br>Click for more info!"


# ============================================================================
# PART 2: TODO CLASSES (YOU WILL COMPLETE THESE)
# ============================================================================

class Restaurant(Place):
    def __init__(self, name, latitude, longitude, food_type):
        super().__init__(name, latitude, longitude)
        self.food_type = food_type

    def get_popup_text(self):
        return f"<b>RESTAURANT: {self.name}</b><br>Food: {self.food_type}"

    def get_marker_color(self):
        return "red"



class Park(Place):
    def __init__(self, name, latitude, longitude, has_playground):
        super().__init__(name, latitude, longitude)
        self.has_playground = has_playground

    def get_popup_text(self):
        playground = "Yes" if self.has_playground else "No"
        return f"<b>PARK: {self.name}</b><br>Playground: {playground}"

    def get_marker_color(self):
        return "green"
    


class Museum(Place):
    def __init__(self, name, latitude, longitude, entry_fee):
        super().__init__(name, latitude, longitude)
        self.entry_fee = entry_fee

    def get_popup_text(self):
        return f"<b>MUSEUM: {self.name}</b><br>Entry: €{self.entry_fee}"

    def get_marker_color(self):
        return "purple"


# ============================================================================
# PART 3: MAP CLASS
# ============================================================================

class MyMap:
    def __init__(self, city, zoom=12):
        self.city = city
        self.places = []
        
        centers = {
    "Paris": [48.8566, 2.3522],
    "London": [51.5074, -0.1278],
    "New York": [40.7128, -74.0060],
    "Tokyo": [35.6762, 139.6503],
    "Calgary": [51.0447, -114.0719]
}
        
        if city in centers:
            center = centers[city]
        else:
            center = [0, 0]
            print(f"Warning: {city} not in our list, using (0,0)")
        
        self.map = folium.Map(location=center, zoom_start=zoom)
        print(f"🗺️  Created map of {city}")
    
    def add_place(self, place):
        self.places.append(place)
        
        folium.Marker(
            location=[place.latitude, place.longitude],
            popup=place.get_popup_text(),
            tooltip=place.name,
            icon=folium.Icon(color=place.get_marker_color())
        ).add_to(self.map)
        
        print(f"  ✅ Added: {place.name}")
    
    def show_distances(self):
        if len(self.places) < 2:
            print("Add at least 2 places to see distances")
            return
        
        print(f"\n📏 Distances in {self.city}:")
        for i in range(len(self.places)):
            for j in range(i+1, len(self.places)):
                place1 = self.places[i]
                place2 = self.places[j]
                dist = place1.distance_to(place2)
                print(f"  {place1.name} → {place2.name}: {dist} km")
    
    def save(self, filename="my_map.html"):
        self.map.save(filename)
        print(f"\n💾 Map saved as '{filename}'")
        return filename


# ============================================================================
# PART 4: MAIN PROGRAM
# ============================================================================

def main():
    print("=" * 50)
    print("🗺️  MY FAVORITE PLACES MAP")
    print("=" * 50)
    
    my_city = "Calgary"
    
    mymap = MyMap(my_city)
    
    print("\n📝 Using Calgary places")
    
    # Define places
    tower = Place("Calgary Tower", 51.0447, -114.0719)
    museum = Museum("Glenbow Museum", 51.0465, -114.0580, 16)
    restaurant = Restaurant("Native Tongues Taqueria", 51.0247, -114.0870, "Mexican")
    park = Park("Prince's Island Park", 51.0543, -114.0719, True)
    
    # Add places to map
    mymap.add_place(tower)
    mymap.add_place(museum)
    mymap.add_place(restaurant)
    mymap.add_place(park)
    
    mymap.show_distances()
    
    filename = mymap.save("my_favorite_places.html")
    
    webbrowser.open(filename)


if __name__ == "__main__":
    main()