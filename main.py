from flask import Flask, render_template_string, request, jsonify
from cloudshell.api.cloudshell_api import CloudShellAPISession
import json
import base64
from http_template import html_template

app = Flask(__name__)

# Replace with your CloudShell server details
CLOUDSHELL_SERVER = 'qs-il-lt-costay'
USERNAME = 'admin'
PASSWORD = 'admin'
DOMAIN = 'Global'

# Base64 encoded CloudShell logo (replace with actual logo if available)
CLOUDSHELL_LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAyCAYAAAAZUZThAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEz0lEQVR4nO2dz28bRRTHv29mdmPHdhynSUqaNIGWQoADB4S4ckGIGwdO/Av8CZy5cuXEkSMHDggJIRAVQQVKoYQWStKkSRI7ju3Y3p15HKgCVePdWQcn9uz7HCztzrz3tPPV7PObWQIREREREREREdcLdRlB7ty5w3fv3n1PSnlTSrlBRCvzLm5RMcY4AI4AHCil9u/fv//tRRqKjEQqF9+8efPdJEluAXgHwOq8C7pCHCulvtvc3Pz6IoNEHrrzDl1fX9eTJNkC8DKAS/kNF5AVAD/s7e1JADuTDsZBTED1+jVXfv2V0DQ9BdCY91muCvIcMXaJqM5aq9l+i+J+UK9qW6sizfOTNCfBhHrofT85z0dE8OAtrbW91lrQpGW4R0ktZD/QvZ88z01tbc/OeFprZ611Ig0hhDHGiDRN81o8uwVkoR72fa8vBU0hCWmUMfUkgV+mEF1O6HhpDmKMcQDgeR4554gWYc2sNSnljNZaCCE45xSPqT3nnBNSSiEl7yuj0u2ctTZ3zhEzyMwrTAghrLX/91JEWHPnXK6Ucs65isc8T7TWtWq+1JKlVCoFzoU/clXlvX3vlb9AIT14AGCGMcZXVlYwGAzmnUGmAlwr5/cviFiYmKqqAPBJlTGXtFYp5ccAHs+7sKvEGPMQwKdhgy5nR/F1ZmVlZd4lXClhsV66BznPtNvteRdwpYTFCkGuwWV/FfQhw+Fw3iVcKWGxQpBrQJ7nYzUkN2/eDBlOAUw/8luCc46JC+QYUzmOcs4Z55ziMMswa+2x1jrTWttvvvvm69XVtQ+YsTUy40vOORsJcV4eyuuDMQYppeh0OvHoqXTFEJMZY4QQgrXWEsCRVuq7dw/2v3zYOTaMMfv553t3b9++/XGr1Xrp1q2XmHNuAbAsy1ApNb08VBbGOfhq8pr9d1jVUeYsm02K800x+ri3vPPOu5/s7/9e/efxQUee59g/OPj54cODn3Z3d1Gv1UXWz4a9PKtrrY3WWkcABu12+93Dw8NPB4NBPY5jCiHH8i8KASYN/ydCCJFlGRpRhFpt5Qww+c8nMrg7o0ACwPnYuvWN9Q3s7OxgZ2cHTJP47beHOOz10D1+gn4/Q5plUFojVxqDwQB6NMJwOMQozyGEGPumAMgyRHGMJGmi2WwhSRpYW1tHs9lEFCfgYgjnXFlWWF4G6yJBLotutwtmxsMoRHGMJGmi0aigVqujWq2iVquNld1qteaVclYURbTSDJixs6KqRkyT5HtPzIu+j+M4rLHnzNQzmGazabwFhc5Gu92m3d1d1TnqPG63230AAwCZMUZ2u93nzPyMcy6YeZ2ZmwCWZyDZgrOEsn9aAHrM3GHm35VSj5xzA+/9IMuyJMuyZRc9mX5GlYVZR4VC/csXkX9or4hxTH1Rfpm2t7fFlDsKf3qKmVytVsuSJDGe5wmAyDkXAYiNMXFxvOj9cYwxHoDSWlcAVAAkzrkKM9ett5HAd6qqTnYyxrmgrxk/YF3RtvK8cWNmQWttvXOZtdZqrXOlVJ5lWVYU+XA4HAZFngQFdsbk1VpbIhoNh6O+1jpnjKEsG42cc2OxmF9Jozid9BxSSiO1ulQCn9jm7v17WXHf+c8yKhYU/FPncV8yQ1t1XstzVrxnjeoh2T92H+5DikXD6KknOue8Mjx3Tnrvvbf2J+fc71rrU621MsZ4rcevKyIiIiIiIiIiIiIiIiLiavEvCZp99FQofIoAAAAASUVORK5CYII="

@app.route('/')
def display_inventory():
    resources_json = []
    error_message = None
    
    try:
        # Connect to CloudShell API
        session = CloudShellAPISession(host=CLOUDSHELL_SERVER, username=USERNAME, password=PASSWORD, domain=DOMAIN)

        # Get inventory
        resources = session.GetResourceList().Resources
        
        # Convert resources to JSON for use in JavaScript
        for resource in resources:
            resources_json.append({
                'Name': resource.Name,
                'ResourceModelName': resource.ResourceModelName,
                'Address': resource.Address,
                'FullAddress': resource.FullAddress
            })
    except Exception as e:
        error_message = f"Failed to connect to CloudShell server: {str(e)}"

    # Generate HTML content with three panels
    
    from datetime import datetime
    
    return render_template_string(html_template, 
                                resources_json=json.dumps(resources_json),
                                error_message=error_message,
                                cloudshell_logo=CLOUDSHELL_LOGO,
                                server=CLOUDSHELL_SERVER,
                                domain=DOMAIN,
                                current_year=datetime.now().year,
                                server_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/get_attributes')
def get_attributes():
    resource_name = request.args.get('resource_name')
    
    if not resource_name:
        return jsonify([])
    
    try:
        # Connect to CloudShell API
        session = CloudShellAPISession(host=CLOUDSHELL_SERVER, username=USERNAME, password=PASSWORD, domain=DOMAIN)
        
        # Get resource attributes
        resource = session.GetResourceDetails(resource_name)
        attributes = resource.ResourceAttributes
        model = resource.ResourceModelName
        result = []
        for attr in attributes:
            value = attr.Value
            if attr.Type.lower() == "password":
                value = "********"  # Mask password values
            result.append({
                'Name': attr.Name.replace(model + '.', ''),
                'FullName': attr.Name,
                'Value': value
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_structure')
def get_structure():
    resource_name = request.args.get('resource_name')
    
    if not resource_name:
        return jsonify({'subresources': []})
    
    try:
        # Connect to CloudShell API
        session = CloudShellAPISession(host=CLOUDSHELL_SERVER, username=USERNAME, password=PASSWORD, domain=DOMAIN)
        
        # Get resource details with subresources
        details = session.GetResourceDetails(resource_name)
        
        def process_subresources(subresources):
            result = []
            for sub in subresources:
                sub_data = {
                    'name': sub.Name,
                    'model': sub.ResourceModelName,
                    'subresources': process_subresources(sub.ChildResources)
                }
                result.append(sub_data)
            return result
        
        return jsonify({
            'subresources': process_subresources(details.ChildResources)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_port_details')
def get_subresource_details():
    """
    Get details of a subresource including its attributes and connections (if it's a port)
    """
    resource_name = request.args.get('resource_name')
    subresource = request.args.get('subresource')
    
    if not resource_name or not subresource:
        return jsonify({'attributes': [], 'connections': []})
    
    try:
        # Connect to CloudShell API
        session = CloudShellAPISession(host=CLOUDSHELL_SERVER, username=USERNAME, password=PASSWORD, domain=DOMAIN)
        
        # full_path = resource_name + '/' + subresource
        full_path = subresource
        result = {'attributes': [], 'connections': []}
        
        # Get subresource attributes
        try:
            # First try: Get direct details from the subresource
            sub_resource = session.GetResourceDetails(full_path)
            
            # Process attributes
            # for sub_resource in sub_details.ChildResources:
                # if sub_resource.Name != subresource:
                #     continue
            for attr in sub_resource.ResourceAttributes:
                value = attr.Value if attr.Value is not None else ""
                if attr.Type and attr.Type.lower() == "password":
                    value = "********"  # Mask password values
                
                # Remove model prefix from attribute name if present
                attr_name = attr.Name
                if '.' in attr.Name:
                    attr_name = attr.Name.split('.', 1)[1]
                
                result['attributes'].append({
                    'Name': attr_name,
                    'Value': value
                })
                
            # Add basic properties as attributes
            result['attributes'].append({'Name': 'Model', 'Value': sub_resource.ResourceModelName})
            
        except Exception as e:
            # If fetching direct details failed, report it in the result
            result['attributes'].append({
                'Name': 'Error',
                'Value': f"Could not get direct attributes: {str(e)}"
            })
        
        # For ports only: Get connections information
        # Check if this appears to be a port resource
        is_port = False
        if full_path.lower().endswith('/port') or 'port' in subresource.lower():
            is_port = True
        
        if is_port:
            connections = []
            
            # Try to get connections from the parent resource first
            try:
                parent_details = session.GetResourceDetails(resource_name)
                for conn in parent_details.Connections:
                    if conn.Source.endswith('/' + subresource) or conn.Target.endswith('/' + subresource):
                        direction = "Outgoing" if conn.Source.endswith('/' + subresource) else "Incoming"
                        target = conn.Target if direction == "Outgoing" else conn.Source
                        connections.append({
                            'target': target,
                            'port': conn.FullPath if hasattr(conn, 'FullPath') else '',
                            'direction': direction
                        })
            except Exception as e:
                result['attributes'].append({
                    'Name': 'Warning',
                    'Value': f"Could not check parent connections: {str(e)}"
                })
                
            # Also check for connections directly from the subresource
            try:
                sub_details = session.GetResourceDetails(full_path)
                for conn in sub_details.Connections:
                    direction = "Outgoing" if conn.Source == full_path else "Incoming"
                    target = conn.Target if direction == "Outgoing" else conn.Source
                    connections.append({
                        'target': target,
                        'port': conn.FullPath if hasattr(conn, 'FullPath') else '',
                        'direction': direction
                    })
            except:
                # Ignore if this fails - we already tried getting connections from parent
                pass
                
            result['connections'] = connections
        else:
            result['connections'] = []
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

