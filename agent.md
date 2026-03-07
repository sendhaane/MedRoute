# Mission: MedRoute - Open Source Search Logic

## 1. Geocoding Logic
- Use the Nominatim API to convert the 'YOUR LOCATION' text input into coordinates.
- If Nominatim fails, default to Puducherry center (11.9416, 79.8083).

## 2. Fallback "Places" Logic
- If the medicine search in SQLite returns 0 results:
    - Trigger an Overpass API query for 'amenity=pharmacy' within 5km of the user.
    - Display these as 🟡 'Unverified Nearby' markers on the map.

## 3. Constraints
- Use Leaflet.js only. 
- Strictly NO Google API calls.
- Follow the **No Comments** rule.