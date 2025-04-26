html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudShell Inventory</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                background-color: #f9f9f9;
            }
            .header {
                background-color: #0078d7;
                color: white;
                padding: 10px 20px;
                display: flex;
                align-items: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .logo {
                height: 40px;
                margin-right: 15px;
            }
            .header-title {
                font-size: 22px;
                font-weight: 500;
            }
            .header-info {
                margin-left: auto;
                font-size: 14px;
            }
            .main-content {
                display: flex;
                flex: 1;
                overflow: hidden;
            }
            .panel {
                border: 1px solid #ddd;
                padding: 15px;
                overflow: auto;
                height: 100%;
                box-sizing: border-box;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            }
            #left-panel {
                flex: 1;
                background-color: #f5f5f5;
                border-right: none;
            }
            #center-panel {
                flex: 2;
                background-color: #ffffff;
                border-left: 1px solid #e0e0e0;
                border-right: 1px solid #e0e0e0;
            }
            #right-panel {
                flex: 1;
                background-color: #f5f5f5;
                border-left: none;
            }
            .tree-view {
                font-size: 14px;
            }
            .tree-item {
                cursor: pointer;
                padding: 5px;
                margin: 3px 0;
                border-radius: 3px;
                transition: background-color 0.2s;
            }
            .tree-item:hover {
                background-color: #e0e0e0;
            }
            .selected {
                background-color: #d0e8ff;
                border-left: 3px solid #0078d7;
            }
            .caret {
                cursor: pointer;
                user-select: none;
            }
            .caret::before {
                content: "▶";
                color: #0078d7;
                display: inline-block;
                margin-right: 6px;
                font-size: 10px;
            }
            .caret-down::before {
                content: "▼";
            }
            .nested {
                display: none;
                padding-left: 20px;
            }
            .active {
                display: block;
            }
            h2 {
                margin-top: 0;
                color: #0078d7;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
                font-size: 18px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                border: 1px solid #eee;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f8fd;
                color: #0078d7;
            }
            /* Prevent attribute names from wrapping */
            td.tooltip {
                white-space: nowrap;
                container: body;
            }
            .error-message {
                color: #d9534f;
                padding: 15px;
                margin: 15px;
                border: 1px solid #d9534f;
                background-color: #f2dede;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .search-bar {
                margin-bottom: 15px;
                display: flex;
            }
            .search-bar input {
                flex-grow: 1;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
            .badge {
                display: inline-block;
                background-color: #0078d7;
                color: white;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 12px;
                margin-left: 5px;
            }
            .status-indicator {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 5px;
            }
            .status-online {
                background-color: #5cb85c;
            }
            .status-offline {
                background-color: #d9534f;
            }
            .status-unknown {
                background-color: #f0ad4e;
            }
            .footer {
                background-color: #f5f5f5;
                border-top: 1px solid #ddd;
                padding: 10px 20px;
                text-align: center;
                font-size: 12px;
                color: #777;
            }
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: help;
                border-bottom: 1px dotted #0078d7;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: auto;
                min-width: 200px;
                max-width: 300px;
                background-color: #333;
                color: #fff;
                text-align: left;
                border-radius: 4px;
                padding: 5px 10px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 0;
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 12px;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <img src="{{ cloudshell_logo }}" alt="CloudShell Logo" class="logo">
            <div class="header-title">CloudShell Inventory</div>
            <div class="header-info">
                <div>Server: {{ server }}</div>
                <div>Domain: {{ domain }}</div>
            </div>
        </div>
        
        {% if error_message %}
        <div class="error-message">
            <h3>Connection Error</h3>
            <p>{{ error_message }}</p>
            <p>Please check your CloudShell connection settings and try again.</p>
        </div>
        {% endif %}
        
        <div class="main-content">
            <div id="left-panel" class="panel">
                <h2>Resource Tree</h2>
                <div class="search-bar">
                    <input type="text" id="resourceSearch" placeholder="Search resources..." onkeyup="filterResources()">
                </div>
                <div class="tree-view" id="resource-tree">
                    {% if error_message %}
                    <p>CloudShell connection failed. Cannot load resources.</p>
                    {% endif %}
                    <!-- Resource tree will be populated dynamically -->
                </div>
            </div>
            <div id="center-panel" class="panel">
                <h2>Resource Details</h2>
                <div id="resource-details">
                    {% if error_message %}
                    <p>CloudShell connection failed. Cannot load resource details.</p>
                    {% else %}
                    <p>Select a resource from the left panel to view details.</p>
                    <div class="welcome-info">
                        <h3>CloudShell Inventory Explorer</h3>
                        <p>Use this tool to explore your CloudShell inventory:</p>
                        <ul>
                            <li>Browse resources in the left panel</li>
                            <li>View resource details and attributes here</li>
                            <li>Explore device structure in the right panel</li>
                            <li>View connection information by clicking on ports</li>
                        </ul>
                    </div>
                    {% endif %}
                </div>
            </div>
            <div id="right-panel" class="panel">
                <h2>Device Structure</h2>
                <div class="tree-view" id="device-structure">
                    {% if error_message %}
                    <p>CloudShell connection failed. Cannot load device structure.</p>
                    {% else %}
                    <p>Select a resource from the left panel to view its structure.</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="footer">
            CloudShell Inventory Explorer v1.0 | © {{ current_year }} | Server time: {{ server_time }}
        </div>

        {% if not error_message %}
        <script>
            // Store all resources data
            const allResources = {{ resources_json|safe }};
            
            // Function to filter resources in the tree
            function filterResources() {
                const searchInput = document.getElementById('resourceSearch');
                const filter = searchInput.value.toUpperCase();
                const treeItems = document.querySelectorAll('.tree-item');
                
                treeItems.forEach(item => {
                    const resourceName = item.dataset.resourceName.toUpperCase();
                    if (resourceName.includes(filter)) {
                        item.style.display = "";
                        // Make sure parent folders are visible
                        let parent = item.parentElement;
                        while (parent && !parent.classList.contains('tree-view')) {
                            if (parent.classList.contains('nested')) {
                                parent.classList.add('active');
                                const parentCaret = parent.previousElementSibling;
                                if (parentCaret && parentCaret.classList.contains('caret')) {
                                    parentCaret.classList.add('caret-down');
                                }
                            }
                            parent = parent.parentElement;
                        }
                    } else {
                        item.style.display = "none";
                    }
                });
            }
            
            // Function to build the resource tree
            function buildResourceTree() {
                const rootResources = allResources.filter(r => !r.FullAddress.includes('/'));
                const treeContainer = document.getElementById('resource-tree');
                
                function buildTreeRecursively(parentElement, parentFullAddress) {
                    const children = allResources.filter(r => {
                        if (!parentFullAddress) {
                            return !r.FullAddress.includes('/');
                        }
                        const parts = r.FullAddress.split('/');
                        return r.FullAddress.startsWith(parentFullAddress + '/') && 
                               parts.length === parentFullAddress.split('/').length + 1;
                    });
                    
                    if (children.length > 0) {
                        const ul = document.createElement('ul');
                        ul.className = 'nested';
                        
                        children.forEach(child => {
                            const li = document.createElement('li');
                            
                            if (allResources.some(r => r.FullAddress.startsWith(child.FullAddress + '/'))) {
                                const span = document.createElement('span');
                                span.className = 'caret';
                                span.textContent = child.Name;
                                span.onclick = function(e) {
                                    this.parentElement.querySelector('.nested').classList.toggle('active');
                                    this.classList.toggle('caret-down');
                                    e.stopPropagation();
                                };
                                li.appendChild(span);
                            } else {
                                const span = document.createElement('span');
                                span.textContent = child.Name;
                                li.appendChild(span);
                            }
                            
                            li.className = 'tree-item';
                            li.dataset.resourceName = child.Name;
                            li.dataset.resourceFullAddress = child.FullAddress;
                            li.onclick = function(e) {
                                selectResource(child);
                                e.stopPropagation();
                                
                                // Remove selected class from all items
                                document.querySelectorAll('.tree-item').forEach(item => {
                                    item.classList.remove('selected');
                                });
                                
                                // Add selected class to this item
                                this.classList.add('selected');
                            };
                            
                            buildTreeRecursively(li, child.FullAddress);
                            ul.appendChild(li);
                        });
                        
                        parentElement.appendChild(ul);
                    }
                }
                
                // Create the root level resources
                rootResources.forEach(root => {
                    const li = document.createElement('li');
                    
                    if (allResources.some(r => r.FullAddress.startsWith(root.FullAddress + '/'))) {
                        const span = document.createElement('span');
                        span.className = 'caret';
                        span.textContent = root.Name;
                        span.onclick = function(e) {
                            this.parentElement.querySelector('.nested')?.classList.toggle('active');
                            this.classList.toggle('caret-down');
                            e.stopPropagation();
                        };
                        li.appendChild(span);
                    } else {
                        const span = document.createElement('span');
                        span.textContent = root.Name;
                        li.appendChild(span);
                    }
                    
                    li.className = 'tree-item';
                    li.dataset.resourceName = root.Name;
                    li.dataset.resourceFullAddress = root.FullAddress;
                    li.onclick = function(e) {
                        selectResource(root);
                        e.stopPropagation();
                        
                        // Remove selected class from all items
                        document.querySelectorAll('.tree-item').forEach(item => {
                            item.classList.remove('selected');
                        });
                        
                        // Add selected class to this item
                        this.classList.add('selected');
                    };
                    
                    buildTreeRecursively(li, root.FullAddress);
                    treeContainer.appendChild(li);
                });
            }
            
            // Function to select a resource and show its details
            function selectResource(resource) {
                // Display resource details in center panel
                const detailsPanel = document.getElementById('resource-details');
                let detailsHtml = `
                    <h3>${resource.Name}</h3>
                    <table>
                        <tr><th>Model</th><td>${resource.ResourceModelName}</td></tr>
                        <tr><th>Address</th><td>${resource.Address}</td></tr>
                        <tr><th>Full Address</th><td>${resource.FullAddress}</td></tr>
                    </table>
                    <h4>Attributes</h4>
                    <div id="attributes-loading">Loading attributes...</div>
                `;
                detailsPanel.innerHTML = detailsHtml;
                
                // Load attributes via AJAX
                fetch('/get_attributes?resource_name=' + encodeURIComponent(resource.Name))
                    .then(response => response.json())
                    .then(data => {
                        const attributesContainer = document.getElementById('attributes-loading');
                        if (data.length > 0) {
                            let attributesHtml = '<table><tr><th>Name</th><th>Value</th></tr>';
                            data.forEach(attr => {
                                // Add tooltip without disrupting table layout
                                attributesHtml += `<tr>
                                    <td title="Full name: ${attr.FullName || attr.Name}">${attr.Name}</td>
                                    <td>${attr.Value}</td>
                                </tr>`;
                            });
                            attributesHtml += '</table>';
                            attributesContainer.innerHTML = attributesHtml;
                        } else {
                            attributesContainer.innerHTML = '<p>No attributes found.</p>';
                        }
                    })
                    .catch(error => {
                        document.getElementById('attributes-loading').innerHTML = 
                            '<p>Error loading attributes: ' + error.message + '</p>';
                    });
                
                // Load device structure in right panel
                const structurePanel = document.getElementById('device-structure');
                structurePanel.innerHTML = '<div id="structure-loading">Loading device structure...</div>';
                
                fetch('/get_structure?resource_name=' + encodeURIComponent(resource.Name))
                    .then(response => response.json())
                    .then(data => {
                        const structureContainer = document.getElementById('structure-loading');
                        
                        if (data.subresources && data.subresources.length > 0) {
                            structureContainer.innerHTML = '';
                            
                            function buildStructureTree(subresources, container) {
                                const ul = document.createElement('ul');
                                ul.className = 'nested active';
                                
                                subresources.forEach(sub => {
                                    const li = document.createElement('li');
                                    li.className = 'tree-item';
                                    
                                    if (sub.subresources && sub.subresources.length > 0) {
                                        const span = document.createElement('span');
                                        span.className = 'caret caret-down';
                                        span.textContent = sub.name;
                                        span.onclick = function(e) {
                                            this.parentElement.querySelector('.nested').classList.toggle('active');
                                            this.classList.toggle('caret-down');
                                            e.stopPropagation();
                                        };
                                        li.appendChild(span);
                                    } else {
                                        const span = document.createElement('span');
                                        span.textContent = sub.name;
                                        li.appendChild(span);
                                    }
                                    
                                    li.onclick = function(e) {
                                        showSubresourceDetails(sub.name, resource.Name);
                                        e.stopPropagation();
                                        
                                        // Remove selected class from all items
                                        document.querySelectorAll('#device-structure .tree-item').forEach(item => {
                                            item.classList.remove('selected');
                                        });
                                        
                                        // Add selected class to this item
                                        this.classList.add('selected');
                                    };
                                    
                                    if (sub.subresources && sub.subresources.length > 0) {
                                        buildStructureTree(sub.subresources, li);
                                    }
                                    
                                    ul.appendChild(li);
                                });
                                
                                container.appendChild(ul);
                            }
                            
                            buildStructureTree(data.subresources, structureContainer);
                        } else {
                            structureContainer.innerHTML = '<p>No subresources found.</p>';
                        }
                    })
                    .catch(error => {
                        document.getElementById('structure-loading').innerHTML = 
                            '<p>Error loading device structure: ' + error.message + '</p>';
                    });
            }
            
            // Function to show subresource details and connections
            function showSubresourceDetails(subresourceName, parentName) {
                const detailsPanel = document.getElementById('resource-details');
                detailsPanel.innerHTML = `
                    <h3>Port Details: ${subresourceName}</h3>
                    <div id="port-loading">Loading port information...</div>
                `;
                
                // Get the full path of the subresource
                const fullPath = parentName + '/' + subresourceName;
                
                // Fetch port attributes
                fetch('/get_port_details?resource_name=' + encodeURIComponent(parentName) + 
                      '&subresource=' + encodeURIComponent(subresourceName))
                    .then(response => response.json())
                    .then(data => {
                        const portLoadingDiv = document.getElementById('port-loading');
                        let portDetailsHtml = '';
                        
                        // Display attributes
                        if (data.attributes && data.attributes.length > 0) {
                            portDetailsHtml += `
                                <h4>Port Attributes</h4>
                                <table>
                                    <tr><th>Name</th><th>Value</th></tr>
                            `;
                            
                            data.attributes.forEach(attr => {
                                portDetailsHtml += `
                                    <tr>
                                        <td class="tooltip">${attr.Name}
                                            <span class="tooltiptext">Full name: ${attr.FullName || attr.Name}</span>
                                        </td>
                                        <td>${attr.Value}</td>
                                    </tr>
                                `;
                            });
                            
                            portDetailsHtml += '</table>';
                        } else {
                            portDetailsHtml += '<p>No port attributes found.</p>';
                        }
                        
                        // Display connections
                        portDetailsHtml += '<h4>Connections</h4>';
                        
                        if (data.connections && data.connections.length > 0) {
                            portDetailsHtml += `
                                <table>
                                    <tr>
                                        <th>Connected To</th>
                                        <th>Device</th>
                                        <th>Direction</th>
                                        <th>Status</th>
                                    </tr>
                            `;
                            
                            data.connections.forEach(conn => {
                                const targetParts = conn.target.split('/');
                                const targetDevice = targetParts.length > 1 ? targetParts[targetParts.length - 2] : '—';
                                const targetPort = targetParts[targetParts.length - 1];
                                
                                portDetailsHtml += `
                                    <tr>
                                        <td>${targetPort}</td>
                                        <td>${targetDevice}</td>
                                        <td>${conn.direction}</td>
                                        <td><span class="status-indicator status-online"></span>Active</td>
                                    </tr>
                                `;
                            });
                            
                            portDetailsHtml += '</table>';
                        } else {
                            portDetailsHtml += '<p>This port is not connected.</p>';
                        }
                        
                        portLoadingDiv.innerHTML = portDetailsHtml;
                    })
                    .catch(error => {
                        document.getElementById('port-loading').innerHTML = 
                            '<p>Error loading port information: ' + error.message + '</p>';
                    });
            }
            
            // Initialize the resource tree
            window.onload = buildResourceTree;
        </script>
        {% else %}
        <script>
            // Basic initialization for error state
            const allResources = [];
            
            document.getElementById('resourceSearch').addEventListener('input', function(e) {
                alert('Search functionality is not available when disconnected from CloudShell.');
            });
        </script>
        {% endif %}
    </body>
    </html>
    """