from flask import Flask, render_template_string, request, jsonify
from cloudshell.api.cloudshell_api import CloudShellAPISession
import json
import base64
import logging
from http_template import html_template

app = Flask(__name__)
# Setup logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your CloudShell server details
# CLOUDSHELL_SERVER = '192.168.85.22'
CLOUDSHELL_SERVER = 'qs-il-lt-costay'
USERNAME = 'admin'
PASSWORD = 'admin'
DOMAIN = 'Global'

# Base64 encoded CloudShell logo (replace with actual logo if available)
CLOUDSHELL_LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAyCAYAAAAZUZThAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEz0lEQVR4nO2dz28bRRTHv29mdmPHdhynSUqaNIGWQoADB4S4ckGIGwdO/Av8CZy5cuXEkSMHDggJIRAVQQVKoYQWStKkSRI7ju3Y3p15HKgCVePdWQcn9uz7HCztzrz3tPPV7PObWQIREREREREREdcLdRlB7ty5w3fv3n1PSnlTSrlBRCvzLm5RMcY4AI4AHCil9u/fv//tRRqKjEQqF9+8efPdJEluAXgHwOq8C7pCHCulvtvc3Pz6IoNEHrrzDl1fX9eTJNkC8DKAS/kNF5AVAD/s7e1JADuTDsZBTED1+jVXfv2V0DQ9BdCY91muCvIcMXaJqM5aq9l+i+J+UK9qW6sizfOTNCfBhHrofT85z0dE8OAtrbW91lrQpGW4R0ktZD/QvZ88z01tbc/OeFprZ611Ig0hhDHGiDRN81o8uwVkoR72fa8vBU0hCWmUMfUkgV+mEF1O6HhpDmKMcQDgeR4554gWYc2sNSnljNZaCCE45xSPqT3nnBNSSiEl7yuj0u2ctTZ3zhEzyMwrTAghrLX/91JEWHPnXK6Ucs65isc8T7TWtWq+1JKlVCoFzoU/clXlvX3vlb9AIT14AGCGMcZXVlYwGAzmnUGmAlwr5/cviFiYmKqqAPBJlTGXtFYp5ccAHs+7sKvEGPMQwKdhgy5nR/F1ZmVlZd4lXClhsV66BznPtNvteRdwpYTFCkGuwWV/FfQhw+Fw3iVcKWGxQpBrQJ7nYzUkN2/eDBlOAUw/8luCc46JC+QYUzmOcs4Z55ziMMswa+2x1jrTWttvvvvm69XVtQ+YsTUy40vOORsJcV4eyuuDMQYppeh0OvHoqXTFEJMZY4QQgrXWEsCRVuq7dw/2v3zYOTaMMfv553t3b9++/XGr1Xrp1q2XmHNuAbAsy1ApNb08VBbGOfhq8pr9d1jVUeYsm02K800x+ri3vPPOu5/s7/9e/efxQUee59g/OPj54cODn3Z3d1Gv1UXWz4a9PKtrrY3WWkcABu12+93Dw8NPB4NBPY5jCiHH8i8KASYN/ydCCJFlGRpRhFpt5Qww+c8nMrg7o0ACwPnYuvWN9Q3s7OxgZ2cHTJP47beHOOz10D1+gn4/Q5plUFojVxqDwQB6NMJwOMQozyGEGPumAMgyRHGMJGmi2WwhSRpYW1tHs9lEFCfgYgjnXFlWWF4G6yJBLotutwtmxsMoRHGMJGmi0aigVqujWq2iVquNld1qteaVclYURbTSDJixs6KqRkyT5HtPzIu+j+M4rLHnzNQzmGazabwFhc5Gu92m3d1d1TnqPG63230AAwCZMUZ2u93nzPyMcy6YeZ2ZmwCWZyDZgrOEsn9aAHrM3GHm35VSj5xzA+/9IMuyJMuyZRc9mX5GlYVZR4VC/csXkX9or4hxTH1Rfpm2t7fFlDsKf3qKmVytVsuSJDGe5wmAyDkXAYiNMXFxvOj9cYwxHoDSWlcAVAAkzrkKM9ett5HAd6qqTnYyxrmgrxk/YF3RtvK8cWNmQWttvXOZtdZqrXOlVJ5lWVYU+XA4HAZFngQFdsbk1VpbIhoNh6O+1jpnjKEsG42cc2OxmF9Jozid9BxSSiO1ulQCn9jm7v17WXHf+c8yKhYU/FPncV8yQ1t1XstzVrxnjeoh2T92H+5DikXD6KknOue8Mjx3Tnrvvbf2J+fc71rrU621MsZ4rcevKyIiIiIiIiIiIiIiIiLiavEvCZp99FQofIoAAAAASUVORK5CYII="

def get_api_session():
    """Establish a session with the CloudShell API"""
    return CloudShellAPISession(host=CLOUDSHELL_SERVER, username=USERNAME, password=PASSWORD, domain=DOMAIN)

@app.route('/')
def display_inventory():
    resources_json = []
    folders_json = []
    error_message = None
    
    try:
        # Connect to CloudShell API
        session = get_api_session()

        # Get inventory resources
        resources = session.GetResourceList().Resources
        
        # Debug print to verify folder data
        logger.debug(f"Folders: {json.dumps(folders_json)}")
        
        # Convert resources to JSON for use in JavaScript
        for resource in resources:
            # Get folder path for this resource (if available)
            folder_path = ''
            try:
                if hasattr(resource, 'FolderFullPath') and resource.FolderFullPath:
                    folder_path = resource.FolderFullPath
                elif hasattr(resource, 'FolderPath') and resource.FolderPath:
                    folder_path = resource.FolderPath
                elif hasattr(resource, 'FolderInfo') and resource.FolderInfo:
                    folder_path = resource.FolderInfo
            except Exception as e:
                logger.error(f"Error getting folder for resource {resource.Name}: {str(e)}")
                
            resources_json.append({
                'Name': resource.Name,
                'ResourceModelName': resource.ResourceModelName,
                'Address': resource.Address,
                'FullAddress': resource.FullAddress,
                'FolderPath': folder_path
            })
            
        # If we don't have folder info from the API, try to infer it from the resource structure
        if not folders_json:
            # Create a set of unique folder paths from the resources
            unique_folders = set()
            for resource in resources_json:
                if resource['FolderPath']:
                    unique_folders.add(resource['FolderPath'])
                    
                    # Also add parent folders
                    parts = resource['FolderPath'].split('/')
                    for i in range(1, len(parts)):
                        parent_path = '/'.join(parts[:i])
                        if parent_path:
                            unique_folders.add(parent_path)
            
            # Convert to folder objects
            for folder_path in unique_folders:
                path_parts = folder_path.split('/')
                folder_name = path_parts[-1]
                parent_path = '/'.join(path_parts[:-1]) if len(path_parts) > 1 else ''
                
                folders_json.append({
                    'Name': folder_name,
                    'FullPath': folder_path,
                    'ParentName': parent_path
                })
            
            logger.info(f"Inferred {len(folders_json)} folders from resource paths")
            
    except Exception as e:
        error_message = f"Failed to connect to CloudShell server: {str(e)}"
        logger.error(f"Error: {error_message}")

    # Generate HTML content with three panels
    from datetime import datetime
    
    return render_template_string(html_template, 
                                resources_json=json.dumps(resources_json),
                                folders_json=json.dumps(folders_json),
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
        session = get_api_session()
        
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
        session = get_api_session()
        
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

@app.route('/get_subresource_details')
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
        session = get_api_session()
        
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

@app.route('/get_port_details')
def get_port_details():
    """
    Alias for get_subresource_details for backward compatibility
    """
    return get_subresource_details()

# === User Management Routes from http_server.py ===

@app.route('/get_user_attributes')
def get_user_attributes():
    """Get all attributes for the current user"""
    try:
        api = get_api_session()
        user_details = api.GetUserDetails()
        return jsonify({
            'Username': user_details.Username,
            'Email': user_details.Email,
            'IsActive': user_details.IsActive,
            'IsAdmin': user_details.IsAdmin,
            'Groups': [group.Name for group in user_details.Groups] if hasattr(user_details, 'Groups') else []
        })
    except Exception as e:
        app.logger.error(f"Error getting user attributes: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_users')
def get_users():
    """Get all CloudShell users"""
    try:
        api = get_api_session()
        users_info = api.GetAllUsersDetails()
        return jsonify([{
            'Username': user.Username,
            'Email': user.Email,
            'IsActive': user.IsActive,
            'IsAdmin': user.IsAdmin,
            'Groups': [group.Name for group in user.Groups] if hasattr(user, 'Groups') else []
        } for user in users_info.Users])
    except Exception as e:
        app.logger.error(f"Error getting users: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_groups')
def get_groups():
    """Get all CloudShell groups"""
    try:
        api = get_api_session()
        groups_info = api.GetGroupsDetails()
        return jsonify([{
            'Name': group.Name,
            'Description': group.Description if hasattr(group, 'Description') else '',
            'Role': group.Role if hasattr(group, 'Role') else '',
            'Users': [user.Username for user in group.Users] if hasattr(group, 'Users') else [],
            'Domains': [domain.Name for domain in group.Domains] if hasattr(group, 'Domains') else []
        } for group in groups_info.Groups])
    except Exception as e:
        app.logger.error(f"Error getting groups: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    """Add a new CloudShell user"""
    try:
        api = get_api_session()
        data = request.json
        username = data.get('username', '')
        password = data.get('password', '')
        email = data.get('email', '')
        is_active = data.get('isActive', False)
        is_admin = data.get('isAdmin', False)
        
        result = api.AddNewUser(username, password, email, is_active, is_admin)
        
        # Add user to groups if specified
        groups = data.get('groups', [])
        for group in groups:
            try:
                api.AddUsersToGroup([username], group)
            except Exception as e:
                app.logger.error(f"Error adding user {username} to group {group}: {str(e)}")
        
        return jsonify({"success": True, "message": f"User {username} added successfully"})
    except Exception as e:
        app.logger.error(f"Error adding user: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/add_group', methods=['POST'])
def add_group():
    """Add a new CloudShell group"""
    try:
        api = get_api_session()
        data = request.json
        group_name = data.get('groupName', '')
        description = data.get('description', '')
        role = data.get('role', 'Regular')  # Default to Regular if not specified
        
        result = api.AddNewGroup(group_name, description, role)
        
        # Add users to group if specified
        users = data.get('users', [])
        if users:
            try:
                api.AddUsersToGroup(users, group_name)
            except Exception as e:
                app.logger.error(f"Error adding users to group {group_name}: {str(e)}")
        
        # Add domains to group if specified
        domains = data.get('domains', [])
        for domain in domains:
            try:
                read_only = data.get('readOnly', False)
                api.AddGroupsToDomain(domain, [group_name], read_only)
            except Exception as e:
                app.logger.error(f"Error adding group {group_name} to domain {domain}: {str(e)}")
        
        return jsonify({"success": True, "message": f"Group {group_name} added successfully"})
    except Exception as e:
        app.logger.error(f"Error adding group: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_domains')
def get_domains():
    """Get all CloudShell domains"""
    try:
        api = get_api_session()
        # This is a simplified approach - in real world, you'd need to collect domains from different sources
        # as there's no direct GetAllDomains method in the API
        # Here we'll get the Global domain and any others we can find
        domains = ['Global']
        
        # Try to get more domains from the current user's context
        try:
            user_details = api.GetUserDetails(username='')  # Empty means current user
            if hasattr(user_details, 'Groups'):
                for group in user_details.Groups:
                    if hasattr(group, 'Domains'):
                        for domain in group.Domains:
                            if domain.Name not in domains:
                                domains.append(domain.Name)
        except:
            pass
            
        return jsonify(domains)
    except Exception as e:
        app.logger.error(f"Error getting domains: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete_user', methods=['POST'])
def delete_user():
    """Delete a CloudShell user"""
    try:
        api = get_api_session()
        data = request.json
        username = data.get('username', '')
        
        api.DeleteUser(username)
        return jsonify({"success": True, "message": f"User {username} deleted successfully"})
    except Exception as e:
        app.logger.error(f"Error deleting user: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/delete_group', methods=['POST'])
def delete_group():
    """Delete a CloudShell group"""
    try:
        api = get_api_session()
        data = request.json
        group_name = data.get('groupName', '')
        
        api.DeleteGroup(group_name)
        return jsonify({"success": True, "message": f"Group {group_name} deleted successfully"})
    except Exception as e:
        app.logger.error(f"Error deleting group: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/get_user_structure')
def get_user_structure():
    """Get the structure of the current user including groups and domains"""
    try:
        api = get_api_session()
        user_details = api.GetUserDetails()
        structure = {
            'Username': user_details.Username,
            'Groups': [],
            'Domains': []
        }
        
        if hasattr(user_details, 'Groups'):
            for group in user_details.Groups:
                group_info = {
                    'Name': group.Name,
                    'Domains': [domain.Name for domain in group.Domains] if hasattr(group, 'Domains') else []
                }
                structure['Groups'].append(group_info)
                # Add domains to the top-level domains list if not already present
                for domain in group_info['Domains']:
                    if domain not in structure['Domains']:
                        structure['Domains'].append(domain)
        
        return jsonify(structure)
    except Exception as e:
        app.logger.error(f"Error getting user structure: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting CloudShell Inventory Explorer server on port 5001")
    app.run(debug=True, port=5001, host='0.0.0.0')

