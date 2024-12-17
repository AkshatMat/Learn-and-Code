import json
import os

def load_json(filename):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}.")
        return None

def find_adjacent_countries(country_code, country_codes, adjacent_countries):
    country_code = country_code.upper()
    if country_code not in country_codes:
        return None
    
    adj_data = adjacent_countries['adjacent_countries'].get(country_code, {})
    
    result = {
        "country_name": country_codes[country_code],
        "adjacent_countries": {}
    }
    
    if 'land_borders' in adj_data:
        result['adjacent_countries']['land_borders'] = [
            {
                "code": adj_code, 
                "name": country_codes.get(adj_code, "Unknown")
            } 
            for adj_code in adj_data['land_borders'] 
            if adj_code in country_codes
        ]
    
    if 'maritime_borders' in adj_data:
        result['adjacent_countries']['maritime_borders'] = [
            {
                "code": adj_code, 
                "name": country_codes.get(adj_code, "Unknown")
            } 
            for adj_code in adj_data['maritime_borders'] 
            if adj_code in country_codes
        ]
    
    return result

def main():
    country_codes_data = load_json('D:/L&C/Assignment-1-Console-Application/country-code.json')
    adjacent_countries_data = load_json('D:/L&C/Assignment-1-Console-Application/adjacent-countries.json')
    
    if not country_codes_data or not adjacent_countries_data:
        print("Failed to load required data. Exiting.")
        return
    
    country_codes = country_codes_data.get('country_codes', {})
    
    print("Country Adjacency Finder")
    print("----------------------")
    
    while True:
        country_code = input("\nEnter a country code (e.g., US, IN, DE) or 'Q' to quit: ").strip()
        
        if country_code.upper() == 'Q':
            print("Goodbye!")
            break
        
        if len(country_code) != 2:
            print("Invalid input. Please enter a 2-letter country code.")
            continue
        
        try:
            adjacent_countries = find_adjacent_countries(
                country_code, 
                country_codes, 
                adjacent_countries_data
            )
            
            if adjacent_countries is None:
                print(f"Error: Country code '{country_code}' not found.")
            elif not adjacent_countries['adjacent_countries']:
                print(f"No adjacent countries found for {adjacent_countries['country_name']}.")
            else:
                print(f"Adjacent countries to {adjacent_countries['country_name']}:")
                
                if 'land_borders' in adjacent_countries['adjacent_countries']:
                    print("\nLand Borders:")
                    for country in adjacent_countries['adjacent_countries']['land_borders']:
                        print(f"- {country['name']} ({country['code']})")
                
                if 'maritime_borders' in adjacent_countries['adjacent_countries']:
                    print("\nMaritime Borders:")
                    for country in adjacent_countries['adjacent_countries']['maritime_borders']:
                        print(f"- {country['name']} ({country['code']})")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()