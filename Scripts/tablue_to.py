import xml.etree.ElementTree as ET

# Load the Tableau workbook
tree = ET.parse('./Book1.twb')
root = tree.getroot()

# Get data source info (e.g., CSV path)
datasources = root.find('data/sample_data')
for ds in datasources:
    connection = ds.find('connection')
    csv_path = connection.get('filename')  # Adjust based on actual XML structure
    print(f"Data source: {csv_path}")

# Get worksheet details
worksheets = root.find('worksheets')
for ws in worksheets:
    name = ws.get('name')
    table = ws.find('table')
    rows = table.find('rows').text  # Fields on rows
    cols = table.find('cols').text  # Fields on columns
    print(f"Worksheet: {name}, Rows: {rows}, Columns: {cols}")