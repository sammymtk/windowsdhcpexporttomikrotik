import xml.etree.ElementTree as ET

def extract_dhcp_data(input_file, output_file):
    try:
        # Parse the XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        print("XML file parsed successfully.")
        
        # Open the output file in write mode
        with open(output_file, 'w') as f:
            print(f"Writing output to {output_file}...")
            
            # Find all elements that may contain <Reservation>
            reservations = root.findall(".//Reservation")
            
            if not reservations:
                print("No <Reservation> elements found.")
            
            for i, reservation in enumerate(reservations):
                # Extract IPAddress, ClientId, and Name
                ip_address_elem = reservation.find('IPAddress')
                client_id_elem = reservation.find('ClientId')
                name_elem = reservation.find('Name')
                
                if ip_address_elem is not None and client_id_elem is not None:
                    ip_address = ip_address_elem.text.strip()
                    client_id = client_id_elem.text.strip()
                    name = name_elem.text.strip() if name_elem is not None else 'Unknown'
                    
                    # Debug output
                    print(f"Processing Reservation {i+1}:")
                    print(f"  IP Address: {ip_address}")
                    print(f"  Client ID: {client_id}")
                    print(f"  Name: {name}")
                    
                    # Format and write to the file in the required format
                    f.write(f"/ip dhcp-server lease add address={ip_address} mac-address={client_id} comment={name}\n")
                else:
                    # Debug output for missing elements
                    if ip_address_elem is None:
                        print(f"  Missing <IPAddress> in Reservation {i+1}")
                    if client_id_elem is None:
                        print(f"  Missing <ClientId> in Reservation {i+1}")
        
        print("Data extraction complete.")
    
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the input and output file names
input_file = 'dhcpexport.xml'
output_file = 'dhcp-da-configurare.txt'

# Call the function to extract DHCP data
extract_dhcp_data(input_file, output_file)
