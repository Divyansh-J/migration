import json
import xml.etree.ElementTree as ET
import os

# Hardcoded file paths
TWB_FILE_PATH = r"C:\Users\divyansh.jain\OneDrive - Fresh Gravity\Documents\Learninig\Migration\tableau to PowerBi\Book1.twb" # Replace with your actual .twb file path
JSON_OUTPUT_PATH = r"C:\Users\divyansh.jain\OneDrive - Fresh Gravity\Documents\Learninig\Migration\tableau to PowerBi\output.json"  # Replace with your desired JSON output path

def xml_to_dict(element):
    """Convert XML element to dictionary recursively."""
    result = {}
    
    # Add attributes
    if element.attrib:
        result["@attributes"] = dict(element.attrib)
    
    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_name = child.tag
            child_data = xml_to_dict(child)
            
            # Handle multiple children with same tag
            if child_name in child_dict:
                if isinstance(child_dict[child_name], list):
                    child_dict[child_name].append(child_data)
                else:
                    child_dict[child_name] = [child_dict[child_name], child_data]
            else:
                child_dict[child_name] = child_data
        
        result.update(child_dict)
    
    # Add text content if it exists and is not just whitespace
    if element.text and element.text.strip():
        result["#text"] = element.text.strip()
    
    return result

def convert_twb_to_json(twb_path, json_path):
    """Convert a Tableau Workbook (.twb) file to JSON."""
    if not os.path.exists(twb_path):
        print(f"Error: File '{twb_path}' not found.")
        return False
    
    try:
        # Parse XML
        tree = ET.parse(twb_path)
        root = tree.getroot()
        
        # Convert XML to dict
        twb_dict = {root.tag: xml_to_dict(root)}
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        # Write to JSON file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(twb_dict, json_file, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted '{twb_path}' to '{json_path}'")
        return True
    
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Error during conversion: {e}")
    
    return False

def main():
    convert_twb_to_json(TWB_FILE_PATH, JSON_OUTPUT_PATH)

if __name__ == "__main__":
    main()