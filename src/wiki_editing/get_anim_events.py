import os
import pyperclip
import xml.etree.ElementTree as ET

path = "/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid/projectzomboid/media/AnimSets"

def extract_events_from_xml(file_path):
    """Extract all m_Events blocks from an XML file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        events = []
        
        for event_elem in root.findall('.//m_Events'):
            event_data = {
                'x_name': event_elem.get('x_name', 'Unknown'),
                'EventName': event_elem.findtext('m_EventName', ''),
                'Time': event_elem.findtext('m_Time', ''),
                'ParameterValue': event_elem.findtext('m_ParameterValue', '')
            }
            events.append(event_data)
        
        return events
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
        return []

TEMPLATE = """|-
| <code>{x_name}</code>
|
"""

def main():
    all_events = {}
    unique_event_names = set()
    
    for root_dir, _, files in os.walk(path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root_dir, file)
                events = extract_events_from_xml(file_path)
                
                if events:
                    all_events[file_path] = events
                    for event in events:
                        unique_event_names.add(event['EventName'])
    
    print("Unique EventNames:")
    txt = ""
    for event_name in sorted(unique_event_names):
        txt += TEMPLATE.format(x_name=event_name)
    
    pyperclip.copy(txt)
    print(txt)
    print(f"\nTotal unique EventNames: {len(unique_event_names)}")

if __name__ == "__main__":
    main()