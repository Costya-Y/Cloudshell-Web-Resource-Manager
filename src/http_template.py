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
                font-size: 14px;
                line-height: 1.4;
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
                font-family: 'Segoe UI', Arial, sans-serif;
                display: block;
                width: 100%;
            }
            .tree-view ul {
                margin: 0;
                padding-left: 20px;
                list-style-type: none;
                width: 100%;
                display: block;
            }
            .tree-view li {
                width: 100%;
                display: block;
                position: relative;
            }
            .tree-item {
                cursor: pointer;
                padding: 6px 8px;
                margin: 4px 0;
                border-radius: 3px;
                transition: background-color 0.2s;
                display: block;
                position: relative;
            }
            .tree-item span {
                display: flex;
                align-items: center;
                width: 100%;
            }
            .tree-item:hover {
                background-color: #e0e0e0;
            }
            .selected {
                background-color: #d0e8ff;
                border-left: 3px solid #0078d7;
            }
            .folder {
                color: #0078d7;
                font-weight: 500;
                margin: 8px 0;
                display: flex;
                align-items: center;
            }
            .folder-icon {
                color: #0078d7;
                margin-right: 8px;
                font-size: 16px; /* Slightly larger folder icon */
            }
            .resource-icon {
                margin-right: 8px;
                color: #555;
                font-size: 15px; /* Consistent with folder icon */
            }
            .caret {
                cursor: pointer;
                user-select: none;
                margin-right: 4px;
                display: inline-block;
                min-width: 16px;
                min-height: 16px;
                text-align: center;
                position: relative;
                z-index: 2;
            }
            .caret::before {
                content: "▶";
                color: #0078d7;
                display: inline-block;
                margin-right: 6px;
                font-size: 12px;
                transition: transform 0.2s;
                position: relative;
                top: -1px;
            }
            .caret-down::before {
                content: "▼";
                transform: rotate(0deg);
            }
            .nested {
                display: none;
                padding-left: 20px;
                margin-top: 2px;
                margin-bottom: 2px;
                list-style-type: none;
                width: 100%;
            }
            .active {
                display: block !important;
            }
            .nested .tree-item {
                margin: 3px 0;
                width: 100%;
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
                vertical-align: top;
                font-size: 14px;
            }
            th {
                background-color: #f2f8fd;
                color: #0078d7;
                font-weight: 600;
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
                font-size: 14px;
                font-family: inherit;
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
            .tooltip-inner  {
                white-space:pre; /* you can also try white-space: normal; */
                max-width:none;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            .folder-path {
                color: #777;
                font-size: 12px;
                font-style: italic;
                margin-top: 4px;
                margin-bottom: 4px;
                margin-left: 24px; /* Align with resource content */
            }
            .view-toggle {
                margin-bottom: 15px;
                display: flex;
            }
            .view-toggle button {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 6px 12px;
                cursor: pointer;
                font-family: inherit;
                font-size: 13px;
            }
            .view-toggle button.active {
                background-color: #0078d7;
                color: white;
                border-color: #0078d7;
            }
            .view-toggle button:first-child {
                border-radius: 3px 0 0 3px;
            }
            .view-toggle button:last-child {
                border-radius: 0 3px 3px 0;
            }
            /* Styles for improved alignment and spacing */
            .resource-name, .folder-name {
                display: inline-block;
                vertical-align: middle;
                line-height: 1.4;
            }
            /* Add spacing between different folder levels */
            .nested .folder {
                margin-left: 0px;
            }
            .welcome-info {
                padding: 10px;
                background-color: #f5f9ff;
                border-radius: 4px;
                border-left: 3px solid #0078d7;
                margin: 10px 0;
            }
            .welcome-info h3 {
                color: #0078d7;
                margin-top: 0;
            }
            .welcome-info ul {
                margin-bottom: 0;
                padding-left: 20px;
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
                <div class="view-toggle">
                    <button id="btnFlatView" onclick="switchView('flat')">Flat View</button>
                    <button id="btnFolderView" class="active" onclick="switchView('folder')">Folder View</button>
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
                            <li>Toggle between flat and folder view to see resources organized by folders</li>
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
            const allFolders = {{ folders_json|safe }};
            let currentView = 'flat'; // Default to flat view for stability
            
            // Function to filter resources in the tree
            function filterResources() {
                const searchInput = document.getElementById('resourceSearch');
                const filter = searchInput.value.toUpperCase();
                const treeItems = document.querySelectorAll('.tree-item');
                
                treeItems.forEach(item => {
                    const resourceName = item.dataset.resourceName ? item.dataset.resourceName.toUpperCase() : "";
                    if (resourceName.includes(filter)) {
                        item.style.display = "";
                        // Make parent folders visible if needed
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

            // Function to switch between flat and folder views
            function switchView(viewType) {
                currentView = viewType;
                
                // Update button states
                document.getElementById('btnFlatView').classList.toggle('active', viewType === 'flat');
                document.getElementById('btnFolderView').classList.toggle('active', viewType === 'folder');
                
                // Rebuild the tree with the new view
                buildResourceTree();
            }
            
            // Function to build the resource tree
            function buildResourceTree() {
                const treeContainer = document.getElementById('resource-tree');
                treeContainer.innerHTML = '';  // Clear the tree container
                
                if (currentView === 'flat' || !allFolders || allFolders.length === 0) {
                    buildFlatTree();
                } else {
                    try {
                        buildFolderTree();
                    } catch (e) {
                        console.error("Error building folder tree:", e);
                        // Fall back to flat view if there's an error
                        buildFlatTree();
                    }
                }
            }
            
            // Build a flat list of resources without folder structure
            function buildFlatTree() {
                const treeContainer = document.getElementById('resource-tree');
                
                allResources.forEach(resource => {
                    const li = document.createElement('li');
                    const span = document.createElement('span');
                    
                    span.textContent = resource.Name;
                    // Add resource icon
                    const icon = document.createElement('i');
                    icon.className = 'resource-icon';
                    icon.textContent = '📄';
                    span.prepend(icon);
                    
                    li.appendChild(span);
                    li.className = 'tree-item';
                    li.dataset.resourceName = resource.Name;
                    li.dataset.resourceFullAddress = resource.FullAddress;
                    
                    // Show folder path if available
                    if (resource.FolderPath) {
                        const folderPath = document.createElement('div');
                        folderPath.className = 'folder-path';
                        folderPath.textContent = 'Path: ' + resource.FolderPath;
                        li.appendChild(folderPath);
                    }
                    
                    li.onclick = function(e) {
                        selectResource(resource);
                        e.stopPropagation();
                        
                        // Remove selected class from all items
                        document.querySelectorAll('.tree-item').forEach(item => {
                            item.classList.remove('selected');
                        });
                        
                        // Add selected class to this item
                        this.classList.add('selected');
                    };
                    
                    treeContainer.appendChild(li);
                });
            }
            
            // Build a hierarchical tree with folder structure
            function buildFolderTree() {
                const treeContainer = document.getElementById('resource-tree');
                const folderResources = {};
                const rootResources = [];
                const folderMap = {};
                
                // Group resources by folder
                allResources.forEach(resource => {
                    if (resource.FolderPath) {
                        if (!folderResources[resource.FolderPath]) {
                            folderResources[resource.FolderPath] = [];
                        }
                        folderResources[resource.FolderPath].push(resource);
                    } else {
                        rootResources.push(resource);
                    }
                });
                
                // Build a folder map with parent-child relationships
                allFolders.forEach(folder => {
                    folderMap[folder.FullPath] = {
                        name: folder.Name,
                        fullPath: folder.FullPath,
                        parentPath: folder.ParentName || null,
                        subFolders: [],
                        resources: folderResources[folder.FullPath] || []
                    };
                });
                
                // Establish parent-child relationships
                for (const path in folderMap) {
                    const folder = folderMap[path];
                    if (folder.parentPath && folderMap[folder.parentPath]) {
                        folderMap[folder.parentPath].subFolders.push(folder);
                    }
                }
                
                // Find root folders
                const rootFolders = [];
                for (const path in folderMap) {
                    const folder = folderMap[path];
                    if (!folder.parentPath || !folderMap[folder.parentPath]) {
                        rootFolders.push(folder);
                    }
                }
                
                // If no folders exist at all, just display resources in flat view
                if (rootFolders.length === 0 && Object.keys(folderMap).length === 0) {
                    console.log("No folders found, displaying resources in flat view");
                    buildFlatTree();
                    return;
                }
                
                // Recursively build the folder tree
                function createFolderElement(folderObj, container) {
                    const folderLi = document.createElement('li');
                    // Create separate caret span for expand/collapse
                    const caretSpan = document.createElement('span');
                    caretSpan.className = 'caret';
                    folderLi.appendChild(caretSpan);
                    // Create folder text span for name and icon
                    const folderTextSpan = document.createElement('span');
                    folderTextSpan.className = 'folder';
                    // Add folder icon
                    const folderIcon = document.createElement('i');
                    folderIcon.className = 'folder-icon';
                    folderIcon.textContent = '📁';
                    folderTextSpan.prepend(folderIcon);
                    folderTextSpan.append(' ' + folderObj.name);
                    folderLi.appendChild(folderTextSpan);

                    // Create nested container for resources and subfolders
                    const nestedUl = document.createElement('ul');
                    nestedUl.className = 'nested';

                    // Add resources in this folder
                    folderObj.resources.forEach(resource => {
                        const resourceLi = document.createElement('li');
                        const resourceSpan = document.createElement('span');
                        
                        // Add resource icon
                        const resourceIcon = document.createElement('i');
                        resourceIcon.className = 'resource-icon';
                        resourceIcon.textContent = '📄';
                        
                        resourceSpan.textContent = resource.Name;
                        resourceSpan.prepend(resourceIcon);
                        
                        resourceLi.appendChild(resourceSpan);
                        resourceLi.className = 'tree-item';
                        resourceLi.dataset.resourceName = resource.Name;
                        resourceLi.dataset.resourceFullAddress = resource.FullAddress;
                        
                        resourceLi.onclick = function(e) {
                            selectResource(resource);
                            e.stopPropagation();
                            
                            // Remove selected class from all items
                            document.querySelectorAll('.tree-item').forEach(item => {
                                item.classList.remove('selected');
                            });
                            
                            // Add selected class to this item
                            this.classList.add('selected');
                        };
                        
                        nestedUl.appendChild(resourceLi);
                    });
                    
                    // Add subfolders (recursively)
                    folderObj.subFolders.forEach(subFolder => {
                        createFolderElement(subFolder, nestedUl);
                    });

                    // Toggle expand/collapse on caret click
                    caretSpan.addEventListener('click', function(e) {
                        nestedUl.classList.toggle('active');
                        this.classList.toggle('caret-down');
                        //e.stopPropagation();
                    });
                    // Also toggle expand/collapse when clicking the folder name
                    folderTextSpan.addEventListener('click', function(e) {
                        nestedUl.classList.toggle('active');
                        caretSpan.classList.toggle('caret-down');
                        //e.stopPropagation();
                    });

                    folderLi.appendChild(nestedUl);
                    container.appendChild(folderLi);
                }
                
                // Build root folders and their children recursively
                rootFolders.forEach(rootFolder => {
                    createFolderElement(rootFolder, treeContainer);
                });
                
                // Add root resources (not in any folder)
                rootResources.forEach(resource => {
                    const li = document.createElement('li');
                    const span = document.createElement('span');
                    
                    // Add resource icon
                    const icon = document.createElement('i');
                    icon.className = 'resource-icon';
                    icon.textContent = '📄';
                    
                    span.textContent = resource.Name;
                    span.prepend(icon);
                    
                    li.appendChild(span);
                    li.className = 'tree-item';
                    li.dataset.resourceName = resource.Name;
                    li.dataset.resourceFullAddress = resource.FullAddress;
                    
                    li.onclick = function(e) {
                        selectResource(resource);
                        e.stopPropagation();
                        
                        // Remove selected class from all items
                        document.querySelectorAll('.tree-item').forEach(item => {
                            item.classList.remove('selected');
                        });
                        
                        // Add selected class to this item
                        this.classList.add('selected');
                    };
                    
                    treeContainer.appendChild(li);
                });
                
                // If nothing was added to the tree, fall back to flat view
                if (treeContainer.children.length === 0) {
                    console.log("No items added to folder view, falling back to flat view");
                    buildFlatTree();
                }
            }
            
            // Function to select a resource and show its details
            function selectResource(resource) {
                // Display resource details in center panel
                const detailsPanel = document.getElementById('resource-details');
                
                let detailsHtml = `
                    <h3>${resource.Name}</h3>
                `;
                
                // Add folder path if available
                if (resource.FolderPath) {
                    detailsHtml += `<div class="folder-path">Folder: ${resource.FolderPath}</div>`;
                }
                
                detailsHtml += `
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
                
                // Store the current resource for later reference
                window.currentResource = resource;
                
                // Load device structure in right panel
                const structurePanel = document.getElementById('device-structure');
                structurePanel.innerHTML = '<div id="structure-loading">Loading device structure...</div>';
                
                fetch('/get_structure?resource_name=' + encodeURIComponent(resource.Name))
                    .then(response => response.json())
                    .then(data => {
                        buildDeviceStructure(data, resource);
                    })
                    .catch(error => {
                        document.getElementById('structure-loading').innerHTML = 
                            '<p>Error loading device structure: ' + error.message + '</p>';
                    });
            }
            
            // Separate function to build device structure to avoid code duplication
            function buildDeviceStructure(data, resource) {
                const structureContainer = document.getElementById('structure-loading');
                
                // Create a root element for the device itself
                const rootUl = document.createElement('ul');
                rootUl.className = 'tree-view';
                
                // Create root resource node
                const rootLi = document.createElement('li');
                rootLi.className = 'tree-item'; // Add tree-item class to make it selectable
                
                // Add caret for root element
                const caretSpan = document.createElement('span');
                caretSpan.className = 'caret caret-down';
                caretSpan.style.cursor = 'pointer';
                caretSpan.style.paddingLeft = '1px';
                caretSpan.style.width = '10px';
                
                // Add device name and icon in a separate span
                const rootSpan = document.createElement('span');
                rootSpan.style.paddingLeft = '1px';
                
                // Add device icon for the root resource
                const deviceIcon = document.createElement('i');
                deviceIcon.className = 'folder-icon';
                
                // Choose appropriate device icon based on model name
                if (resource.ResourceModelName && resource.ResourceModelName.toLowerCase().includes('router')) {
                    deviceIcon.textContent = '🌐'; // Router icon
                } else if (resource.ResourceModelName && resource.ResourceModelName.toLowerCase().includes('switch')) {
                    deviceIcon.textContent = '🔄'; // Switch icon
                } else if (resource.ResourceModelName && resource.ResourceModelName.toLowerCase().includes('firewall')) {
                    deviceIcon.textContent = '🛡️'; // Firewall icon
                } else if (resource.ResourceModelName && resource.ResourceModelName.toLowerCase().includes('server')) {
                    deviceIcon.textContent = '🖥️'; // Server icon
                } else if (resource.ResourceModelName && resource.ResourceModelName.toLowerCase().includes('load balancer')) {
                    deviceIcon.textContent = '⚖️'; // Load Balancer icon
                } else {
                    deviceIcon.textContent = '📟'; // Generic network device icon
                }
                
                rootSpan.textContent = resource.Name;
                rootSpan.prepend(deviceIcon);
                
                // Create a container div that will hold both caret and text
                const rootItemContainer = document.createElement('div');
                rootItemContainer.className = 'folder';
                rootItemContainer.style.display = 'flex';
                rootItemContainer.style.alignItems = 'center';
                rootItemContainer.appendChild(caretSpan);
                rootItemContainer.appendChild(rootSpan);
                
                rootLi.appendChild(rootItemContainer);
                
                // Make the root name clickable to show resource attributes
                rootSpan.addEventListener('click', function(e) {
                    selectResourceDetailsOnly(resource);
                    
                    // Visual feedback - add selected class
                    document.querySelectorAll('#device-structure .tree-item').forEach(item => {
                        item.classList.remove('selected');
                    });
                    rootLi.classList.add('selected');
                    
                    e.stopPropagation();
                });
                
                if (data.subresources && data.subresources.length > 0) {
                    // Create container for subresources
                    const nestedUl = document.createElement('ul');
                    nestedUl.className = 'nested active';
                    
                    // Toggle root resource expand/collapse when clicking on caret
                    caretSpan.addEventListener('click', function(e) {
                        nestedUl.classList.toggle('active');
                        this.classList.toggle('caret-down');
                        e.stopPropagation();
                    });
                    
                    // Build subresources tree recursively
                    buildStructureTree(data.subresources, nestedUl, resource);
                    
                    rootLi.appendChild(nestedUl);
                    rootUl.appendChild(rootLi);
                    structureContainer.innerHTML = '';
                    structureContainer.appendChild(rootUl);
                } else {
                    // No subresources
                    rootUl.appendChild(rootLi);
                    structureContainer.innerHTML = '';
                    structureContainer.appendChild(rootUl);
                    
                    // Add message that there are no subresources
                    const noSubMsg = document.createElement('p');
                    noSubMsg.textContent = 'This resource has no subresources or ports.';
                    noSubMsg.style.marginLeft = '20px';
                    noSubMsg.style.fontStyle = 'italic';
                    noSubMsg.style.color = '#777';
                    structureContainer.appendChild(noSubMsg);
                }
            }
            
            // Function to show resource details without rebuilding the right panel
            function selectResourceDetailsOnly(resource) {
                // Display resource details in center panel
                const detailsPanel = document.getElementById('resource-details');
                
                let detailsHtml = `
                    <h3>${resource.Name}</h3>
                `;
                
                // Add folder path if available
                if (resource.FolderPath) {
                    detailsHtml += `<div class="folder-path">Folder: ${resource.FolderPath}</div>`;
                }
                
                detailsHtml += `
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
            }
            
            // Build the structure tree - separated into its own function
            function buildStructureTree(subresources, container, resource, path = "") {
                // Sort resources by type: first directories (items with children), then leaf items
                const sortedResources = [...subresources].sort((a, b) => {
                    const aHasChildren = a.subresources && a.subresources.length > 0;
                    const bHasChildren = b.subresources && b.subresources.length > 0;
                    if (aHasChildren && !bHasChildren) return -1;
                    if (!aHasChildren && bHasChildren) return 1;
                    return a.name.localeCompare(b.name); // Then sort alphabetically
                });
                
                sortedResources.forEach(sub => {
                    // Track the full path to this subresource for unique identification
                    const currentPath = path ? `${path}/${sub.name}` : sub.name;
                    const li = document.createElement('li');
                    li.dataset.path = currentPath; // Store path for later reference
                    li.className = 'tree-item'; // All items are tree items
                    
                    // Create a container for the row to hold all elements
                    const rowContainer = document.createElement('div');
                    rowContainer.style.display = 'flex';
                    rowContainer.style.alignItems = 'center';
                    rowContainer.style.width = '100%';
                    
                    if (sub.subresources && sub.subresources.length > 0) {
                        // This is a folder/component with children
                        // Add explicit caret for expansion/collapse
                        const caretSpan = document.createElement('span');
                        caretSpan.className = 'caret'; // Start without caret-down class
                        caretSpan.style.width = '10px';
                        
                        // Add the name span separately
                        const nameSpan = document.createElement('span');
                        nameSpan.style.paddingLeft = '5px';
                        nameSpan.style.cursor = 'pointer';
                        nameSpan.style.flexGrow = '1';
                        
                        // Choose appropriate icon based on subresource type
                        const subIcon = document.createElement('i');
                        subIcon.className = 'folder-icon';
                        
                        const lowerName = sub.name.toLowerCase();
                        const lowerModel = (sub.model || '').toLowerCase();
                        
                        // Set icon based on component type
                        if (lowerName.includes('port') || lowerModel.includes('port')) {
                            subIcon.textContent = '🔌'; // Port icon
                        } else if (lowerName.includes('ethernet') || lowerModel.includes('ethernet')) {
                            subIcon.textContent = '📶'; // Ethernet port icon
                        } else if (lowerName.includes('module') || lowerModel.includes('module')) {
                            subIcon.textContent = '🧩'; // Module icon
                        } else if (lowerName.includes('blade') || lowerModel.includes('blade')) {
                            subIcon.textContent = '🔳'; // Blade icon
                        } else if (lowerName.includes('chassis') || lowerModel.includes('chassis')) {
                            subIcon.textContent = '📦'; // Chassis icon
                        } else if (lowerName.includes('power') || lowerModel.includes('power')) {
                            subIcon.textContent = '⚡'; // Power supply icon
                        } else if (lowerName.includes('card') || lowerModel.includes('card')) {
                            subIcon.textContent = '💳'; // Card icon
                        } else if (lowerName.includes('fan') || lowerModel.includes('fan')) {
                            subIcon.textContent = '💨'; // Fan icon
                        } else if (lowerName.includes('controller') || lowerModel.includes('controller')) {
                            subIcon.textContent = '🎮'; // Controller icon
                        } else {
                            subIcon.textContent = '📁'; // Default folder icon
                        }
                        
                        nameSpan.textContent = sub.name;
                        nameSpan.prepend(subIcon);
                        
                        // Add elements to the row container
                        rowContainer.appendChild(caretSpan);
                        rowContainer.appendChild(nameSpan);
                        li.appendChild(rowContainer);
                        
                        // Create container for children
                        const childUl = document.createElement('ul');
                        childUl.className = 'nested'; // Start with nested class (collapsed)
                        
                        // 1. Caret click only toggles expand/collapse
                        caretSpan.onclick = function(e) {
                            childUl.classList.toggle('active');
                            this.classList.toggle('caret-down');
                            e.stopPropagation(); // Prevent any other handlers from firing
                        };
                        
                        // 2. Name click only shows attributes
                        nameSpan.onclick = function(e) {
                            showSubresourceDetails(sub.name, resource.Name, currentPath);
                            
                            // Remove selected class from all items
                            document.querySelectorAll('#device-structure .tree-item').forEach(item => {
                                item.classList.remove('selected');
                            });
                            
                            // Add selected class to this item
                            li.classList.add('selected');
                            
                            e.stopPropagation();
                        };
                        
                        // Recursively build the tree
                        buildStructureTree(sub.subresources, childUl, resource, currentPath);
                        li.appendChild(childUl);
                    } else {
                        // This is a leaf node (port/endpoint) - no caret needed
                        const nameSpan = document.createElement('span');
                        nameSpan.style.paddingLeft = '20px'; // Align with siblings that have carets
                        nameSpan.style.cursor = 'pointer';
                        nameSpan.style.flexGrow = '1';
                        
                        // Choose appropriate icon based on subresource type
                        const subIcon = document.createElement('i');
                        subIcon.className = 'resource-icon';
                        
                        const lowerName = sub.name.toLowerCase();
                        const lowerModel = (sub.model || '').toLowerCase();
                        
                        // Set icon based on port type
                        if (lowerName.includes('ethernet') || lowerModel.includes('ethernet')) {
                            subIcon.textContent = '📶'; // Ethernet port
                        } else if (lowerName.includes('fiber') || lowerModel.includes('fiber') || 
                                  lowerName.includes('sfp') || lowerModel.includes('sfp')) {
                            subIcon.textContent = '🔆'; // Fiber port icon
                        } else if (lowerName.includes('serial') || lowerModel.includes('serial')) {
                            subIcon.textContent = '📎'; // Serial port icon
                        } else if (lowerName.includes('console') || lowerModel.includes('console')) {
                            subIcon.textContent = '💻'; // Console icon
                        } else if (lowerName.includes('usb') || lowerModel.includes('usb')) {
                            subIcon.textContent = '🔌'; // USB icon
                        } else if (lowerName.includes('power') || lowerModel.includes('power')) {
                            subIcon.textContent = '⚡'; // Power icon
                        } else if (lowerName.includes('mgmt') || lowerModel.includes('mgmt') || 
                                  lowerName.includes('management') || lowerModel.includes('management')) {
                            subIcon.textContent = '🔧'; // Management port icon
                        } else if (lowerName.includes('port') || lowerModel.includes('port')) {
                            subIcon.textContent = '🔌'; // Generic port icon
                        } else {
                            subIcon.textContent = '📄'; // Default resource icon
                        }
                        
                        nameSpan.textContent = sub.name;
                        nameSpan.prepend(subIcon);
                        
                        // Add elements to the row container
                        rowContainer.appendChild(nameSpan);
                        li.appendChild(rowContainer);
                        
                        // Make the leaf node clickable to show attributes
                        nameSpan.onclick = function(e) {
                            showSubresourceDetails(sub.name, resource.Name, currentPath);
                            
                            // Visual feedback - highlight the selected item
                            document.querySelectorAll('#device-structure .tree-item').forEach(item => {
                                item.classList.remove('selected');
                            });
                            li.classList.add('selected');
                            
                            e.stopPropagation(); // Prevent the click from bubbling up
                        };
                    }
                    
                    container.appendChild(li);
                });
            }
            
            // Function to show subresource details and connections
            function showSubresourceDetails(subresourceName, parentName, path) {
                const detailsPanel = document.getElementById('resource-details');
                detailsPanel.innerHTML = `
                    <h3>Port Details: ${subresourceName}</h3>
                    <div id="port-loading">Loading port information...</div>
                `;
                
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
                                // Use the shortened attribute name if available, otherwise use the full name
                                const displayName = attr.Name || attr.FullName.split('.')?.pop() || attr.FullName;
                                
                                portDetailsHtml += `
                                    <tr>
                                        <td class="tooltip">${displayName}
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
            
            // Initialize the resource tree - start with flat view for reliability
            window.onload = function() {
                document.getElementById('btnFlatView').classList.add('active');
                document.getElementById('btnFolderView').classList.remove('active');
                buildResourceTree();
            };
        </script>
        {% else %}
        <script>
            // Basic initialization for error state
            const allResources = [];
            const allFolders = [];
            
            document.getElementById('resourceSearch').addEventListener('input', function(e) {
                alert('Search functionality is not available when disconnected from CloudShell.');
            });
        </script>
        {% endif %}
    </body>
    </html>
    """
