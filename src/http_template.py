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
            
            /* Tab Navigation */
            .tab-nav {
                display: flex;
                background-color: #f0f0f0;
                border-bottom: 1px solid #ddd;
            }
            .tab-button {
                padding: 12px 20px;
                background-color: #f0f0f0;
                border: none;
                border-right: 1px solid #ddd;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: background-color 0.2s;
                color: #555;
            }
            .tab-button:hover {
                background-color: #e0e0e0;
            }
            .tab-button.active {
                background-color: #ffffff;
                color: #0078d7;
                border-bottom: 3px solid #0078d7;
                margin-bottom: -1px;
            }
            
            /* Tab Content */
            .tab-content {
                display: none;
                flex: 1;
                overflow: hidden;
            }
            .tab-content.active {
                display: flex;
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
            }
            .tree-view ul {
                margin: 0;
                padding-left: 20px;
                list-style-type: none;
            }
            .tree-item {
                cursor: pointer;
                padding: 6px 8px;
                margin: 4px 0;
                border-radius: 3px;
                transition: background-color 0.2s;
                display: flex;
                align-items: center;
                position: relative;
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
                display: flex;
                align-items: center;
            }
            .caret::before {
                content: "▶";
                color: #0078d7;
                display: inline-block;
                margin-right: 6px;
                font-size: 10px;
                transition: transform 0.2s;
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
            }
            .nested .tree-item {
                margin: 3px 0;
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
            /* Empty tab styles */
            .empty-tab {
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #f9f9f9;
                padding: 20px;
                text-align: center;
            }
            .empty-tab-icon {
                font-size: 48px;
                color: #0078d7;
                margin-bottom: 20px;
            }
            .coming-soon {
                font-size: 24px;
                color: #0078d7;
                margin-bottom: 10px;
            }
            .empty-tab p {
                color: #777;
                max-width: 600px;
            }
            
            /* User management tab styles */
            .tab-section {
                margin-bottom: 30px;
            }
            
            .action-buttons {
                margin: 15px 0;
            }
            
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.4);
                overflow: auto;
            }
            
            .modal-content {
                background-color: #fff;
                margin: 10% auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 4px;
                width: 50%;
                max-width: 500px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            
            .close-modal {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
            }
            
            .close-modal:hover {
                color: #000;
            }
            
            .form-row {
                margin-bottom: 15px;
            }
            
            .form-row label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
            }
            
            .form-row input[type="text"],
            .form-row input[type="email"],
            .form-row input[type="password"],
            .form-row textarea,
            .form-row select {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 3px;
                font-family: inherit;
                font-size: 14px;
                box-sizing: border-box;
            }
            
            .form-row select[multiple] {
                height: 120px;
            }
            
            .form-row .checkbox-label {
                display: inline-flex;
                align-items: center;
                margin-right: 15px;
                font-weight: normal;
            }
            
            .form-row .checkbox-label input[type="checkbox"] {
                margin-right: 5px;
            }
            
            .form-actions {
                margin-top: 20px;
                text-align: right;
            }
            
            .btn {
                padding: 8px 16px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 3px;
                cursor: pointer;
                font-family: inherit;
                font-size: 14px;
                transition: all 0.2s;
                margin-left: 10px;
            }
            
            .btn-primary {
                background-color: #0078d7;
                color: white;
                border-color: #0078d7;
            }
            
            .btn-danger {
                background-color: #d9534f;
                color: white;
                border-color: #d9534f;
            }
            
            .btn-primary:hover {
                background-color: #006cc1;
            }
            
            .btn-danger:hover {
                background-color: #c9302c;
            }
            
            .tabs-container {
                display: flex;
                height: 100%;
            }
            
            .user-panel {
                flex: 1;
                padding: 20px;
                overflow: auto;
            }
            
            .success-message,
            .error-message {
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
            }
            
            .success-message {
                background-color: #dff0d8;
                color: #3c763d;
                border: 1px solid #d6e9c6;
            }
            
            .error-message {
                background-color: #f2dede;
                color: #a94442;
                border: 1px solid #ebccd1;
            }
            
            .user-tabs {
                display: flex;
                border-bottom: 1px solid #ddd;
                margin-bottom: 20px;
            }
            
            .user-tab {
                padding: 10px 20px;
                cursor: pointer;
                border: 1px solid transparent;
                border-bottom: none;
                margin-bottom: -1px;
            }
            
            .user-tab.active {
                border-color: #ddd;
                border-bottom-color: #fff;
                background-color: #fff;
                font-weight: 500;
            }
            
            .user-tab-content {
                display: none;
            }
            
            .user-tab-content.active {
                display: block;
            }
            
            .status-badge {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 5px;
            }
            
            .status-active {
                background-color: #5cb85c;
            }
            
            .status-inactive {
                background-color: #d9534f;
            }
            
            table.data-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            
            table.data-table th {
                text-align: left;
                padding: 10px;
                background-color: #f2f8fd;
                color: #0078d7;
                border: 1px solid #eee;
                font-weight: 600;
            }
            
            table.data-table td {
                padding: 10px;
                border: 1px solid #eee;
                vertical-align: top;
            }
            
            table.data-table tr:hover {
                background-color: #f5f9ff;
            }
            
            .small-text {
                font-size: 12px;
                color: #777;
            }
            
            .tag-list {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
            }
            
            .tag {
                background-color: #e0e0e0;
                border-radius: 20px;
                padding: 2px 8px;
                font-size: 12px;
                display: inline-block;
            }
            
            .group-tag {
                background-color: #d0e8ff;
                color: #0078d7;
            }
            
            .domain-tag {
                background-color: #d8f0d8;
                color: #3c763d;
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
        
        <!-- Tab Navigation -->
        <div class="tab-nav">
            <button class="tab-button active" onclick="openTab('inventory')">Inventory</button>
            <button class="tab-button" onclick="openTab('attributes')">Attributes</button>
            <button class="tab-button" onclick="openTab('users')">Users & Groups</button>
            <button class="tab-button" onclick="openTab('domains')">Domains</button>
        </div>
        
        <!-- Inventory Tab Content -->
        <div id="inventory" class="tab-content active">
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
        </div>
        
        <!-- Attributes Tab Content -->
        <div id="attributes" class="tab-content">
            <div class="empty-tab">
                <div class="empty-tab-icon">🔍</div>
                <h2 class="coming-soon">Attribute Management Coming Soon</h2>
                <p>This tab will provide functionality to view and manage CloudShell resource attributes, including:</p>
                <ul>
                    <li>Global attribute definitions</li>
                    <li>Resource family attributes</li>
                    <li>Resource model attributes</li>
                    <li>Attribute rules and constraints</li>
                </ul>
            </div>
        </div>
        
        <!-- Users & Groups Tab Content -->
        <div id="users" class="tab-content">
            <div class="tabs-container">
                <div class="user-panel">
                    <div id="user-notification" style="display: none;"></div>
                    
                    <div class="user-tabs">
                        <div class="user-tab active" onclick="switchUserTab('users-management')">Users</div>
                        <div class="user-tab" onclick="switchUserTab('groups-management')">Groups</div>
                    </div>
                    
                    <!-- Users Management Tab -->
                    <div id="users-management" class="user-tab-content active">
                        <h2>User Management</h2>
                        <p>Manage CloudShell users, their permissions and group memberships.</p>
                        
                        <div class="action-buttons">
                            <button class="btn btn-primary" onclick="showAddUserModal()">Add User</button>
                            <button class="btn" onclick="refreshUsers()">Refresh</button>
                        </div>
                        
                        <div class="tab-section">
                            <table class="data-table" id="users-table">
                                <thead>
                                    <tr>
                                        <th>Username</th>
                                        <th>Email</th>
                                        <th>Status</th>
                                        <th>Admin</th>
                                        <th>Groups</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="users-table-body">
                                    <tr>
                                        <td colspan="6">Loading users...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <!-- Groups Management Tab -->
                    <div id="groups-management" class="user-tab-content">
                        <h2>Group Management</h2>
                        <p>Manage CloudShell groups, their members and domain permissions.</p>
                        
                        <div class="action-buttons">
                            <button class="btn btn-primary" onclick="showAddGroupModal()">Add Group</button>
                            <button class="btn" onclick="refreshGroups()">Refresh</button>
                        </div>
                        
                        <div class="tab-section">
                            <table class="data-table" id="groups-table">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Description</th>
                                        <th>Role</th>
                                        <th>Members</th>
                                        <th>Domains</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="groups-table-body">
                                    <tr>
                                        <td colspan="6">Loading groups...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Add User Modal -->
            <div id="add-user-modal" class="modal">
                <div class="modal-content">
                    <span class="close-modal" onclick="closeModal('add-user-modal')">&times;</span>
                    <h2>Add New User</h2>
                    
                    <form id="add-user-form" onsubmit="addNewUser(event)">
                        <div class="form-row">
                            <label for="username">Username *</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        
                        <div class="form-row">
                            <label for="password">Password *</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        
                        <div class="form-row">
                            <label for="email">Email</label>
                            <input type="email" id="email" name="email">
                        </div>
                        
                        <div class="form-row">
                            <label>Status & Permissions</label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="is-active" name="is-active" checked>
                                Active
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="is-admin" name="is-admin">
                                Administrator
                            </label>
                        </div>
                        
                        <div class="form-row">
                            <label for="user-groups">Groups</label>
                            <select id="user-groups" name="user-groups" multiple>
                                <!-- Will be populated dynamically -->
                            </select>
                            <div class="small-text">Hold Ctrl/Cmd to select multiple groups</div>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" class="btn" onclick="closeModal('add-user-modal')">Cancel</button>
                            <button type="submit" class="btn btn-primary">Add User</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Add Group Modal -->
            <div id="add-group-modal" class="modal">
                <div class="modal-content">
                    <span class="close-modal" onclick="closeModal('add-group-modal')">&times;</span>
                    <h2>Add New Group</h2>
                    
                    <form id="add-group-form" onsubmit="addNewGroup(event)">
                        <div class="form-row">
                            <label for="group-name">Group Name *</label>
                            <input type="text" id="group-name" name="group-name" required>
                        </div>
                        
                        <div class="form-row">
                            <label for="group-description">Description</label>
                            <textarea id="group-description" name="group-description" rows="3"></textarea>
                        </div>
                        
                        <div class="form-row">
                            <label for="group-role">Role</label>
                            <select id="group-role" name="group-role">
                                <option value="Regular">Regular</option>
                                <option value="DomainAdmin">Domain Admin</option>
                                <option value="External">External</option>
                            </select>
                        </div>
                        
                        <div class="form-row">
                            <label for="group-users">Users</label>
                            <select id="group-users" name="group-users" multiple>
                                <!-- Will be populated dynamically -->
                            </select>
                            <div class="small-text">Hold Ctrl/Cmd to select multiple users</div>
                        </div>
                        
                        <div class="form-row">
                            <label for="group-domains">Domains</label>
                            <select id="group-domains" name="group-domains" multiple>
                                <!-- Will be populated dynamically -->
                            </select>
                            <div class="small-text">Hold Ctrl/Cmd to select multiple domains</div>
                        </div>
                        
                        <div class="form-row">
                            <label class="checkbox-label">
                                <input type="checkbox" id="read-only" name="read-only">
                                View Only Access (for domains)
                            </label>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" class="btn" onclick="closeModal('add-group-modal')">Cancel</button>
                            <button type="submit" class="btn btn-primary">Add Group</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Domains Tab Content -->
        <div id="domains" class="tab-content">
            <div class="empty-tab">
                <div class="empty-tab-icon">🌐</div>
                <h2 class="coming-soon">Domain Management Coming Soon</h2>
                <p>This tab will provide functionality to manage CloudShell domains, including:</p>
                <ul>
                    <li>Domain creation and configuration</li>
                    <li>Resource assignment to domains</li>
                    <li>Domain-specific settings</li>
                    <li>Cross-domain operations</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            CloudShell Inventory Explorer v1.0 | © {{ current_year }} | Server time: {{ server_time }}
        </div>

        {% if not error_message %}
        <script>
            // Tab switching functionality
            function openTab(tabName) {
                // Hide all tab contents
                const tabContents = document.getElementsByClassName("tab-content");
                for (let i = 0; i < tabContents.length; i++) {
                    tabContents[i].classList.remove("active");
                }
                
                // Deactivate all tab buttons
                const tabButtons = document.getElementsByClassName("tab-button");
                for (let i = 0; i < tabButtons.length; i++) {
                    tabButtons[i].classList.remove("active");
                }
                
                // Show the selected tab content and activate the button
                document.getElementById(tabName).classList.add("active");
                document.querySelector(`.tab-button[onclick="openTab('${tabName}')"]`).classList.add("active");
            }
            
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
                    const folderSpan = document.createElement('span');
                    folderSpan.className = 'caret folder';
                    folderSpan.textContent = folderObj.name;
                    
                    // Add folder icon
                    const folderIcon = document.createElement('i');
                    folderIcon.className = 'folder-icon';
                    folderIcon.textContent = '📁';
                    folderSpan.prepend(folderIcon);
                    
                    folderLi.appendChild(folderSpan);
                    
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
                    
                    // Toggle folder expand/collapse
                    folderSpan.onclick = function(e) {
                        nestedUl.classList.toggle('active');
                        this.classList.toggle('caret-down');
                        e.stopPropagation();
                    };
                    
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
                const rootSpan = document.createElement('span');
                rootSpan.className = 'caret caret-down folder';
                
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
                rootLi.appendChild(rootSpan);
                
                // Make the root resource clickable to show its attributes
                rootLi.addEventListener('click', function(e) {
                    // Only handle click if it was directly on this element or its children
                    // but not on the expand/collapse caret
                    if (e.target === rootLi || 
                        e.target === deviceIcon ||
                        (e.target.nodeName === '#text' && e.target.parentNode === rootSpan)) {
                        
                        // Just load the resource details in the center panel
                        selectResourceDetailsOnly(resource);
                        
                        // Visual feedback - add selected class
                        document.querySelectorAll('#device-structure .tree-item').forEach(item => {
                            item.classList.remove('selected');
                        });
                        rootLi.classList.add('selected');
                        
                        e.stopPropagation();
                    }
                });
                
                if (data.subresources && data.subresources.length > 0) {
                    // Create container for subresources
                    const nestedUl = document.createElement('ul');
                    nestedUl.className = 'nested active';
                    
                    // Toggle root resource expand/collapse
                    rootSpan.onclick = function(e) {
                        nestedUl.classList.toggle('active');
                        this.classList.toggle('caret-down');
                        e.stopPropagation(); // Prevent triggering parent clicks
                    };
                    
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
            function buildStructureTree(subresources, container, resource) {
                subresources.forEach(sub => {
                    const li = document.createElement('li');
                    
                    if (sub.subresources && sub.subresources.length > 0) {
                        // This is a folder/component with children
                        const span = document.createElement('span');
                        span.className = 'caret folder';
                        
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
                        
                        span.textContent = sub.name;
                        span.prepend(subIcon);
                        li.appendChild(span);
                        li.className = 'tree-item'; // Make it clickable and selectable
                        
                        // Create container for children
                        const childUl = document.createElement('ul');
                        childUl.className = 'nested';
                        
                        // Add click handler for expand/collapse ONLY on the caret itself
                        span.onclick = function(e) {
                            childUl.classList.toggle('active');
                            this.classList.toggle('caret-down');
                            e.stopPropagation(); // Prevent triggering parent clicks
                        };
                        
                        // Make component itself clickable to show attributes
                        li.onclick = function(e) {
                            // Don't handle clicks on the caret or folder icon - those are just for expanding
                            if (e.target.classList.contains('caret') || 
                                e.target.classList.contains('folder-icon')) {
                                return; // Let the caret's own click handler manage expansion
                            }
                            
                            showSubresourceDetails(sub.name, resource.Name);
                            
                            // Remove selected class from all items
                            document.querySelectorAll('#device-structure .tree-item').forEach(item => {
                                item.classList.remove('selected');
                            });
                            
                            // Add selected class to this item
                            li.classList.add('selected');
                            
                            // Don't let the click propagate to parent elements
                            e.stopPropagation();
                        };
                        
                        // Recursively build children
                        buildStructureTree(sub.subresources, childUl, resource);
                        li.appendChild(childUl);
                    } else {
                        // This is a leaf node (port/endpoint)
                        const span = document.createElement('span');
                        li.className = 'tree-item';
                        
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
                        
                        span.textContent = sub.name;
                        span.prepend(subIcon);
                        li.appendChild(span);
                        
                        // Make the leaf node clickable
                        li.onclick = function(e) {
                            showSubresourceDetails(sub.name, resource.Name);
                            
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
            function showSubresourceDetails(subresourceName, parentName) {
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
            
            // User Management Scripts
            function switchUserTab(tabId) {
                // Hide all tab contents
                document.querySelectorAll('.user-tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Show selected tab
                document.getElementById(tabId).classList.add('active');
                
                // Update tab buttons
                document.querySelectorAll('.user-tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Find the button that opens this tab
                document.querySelector(`.user-tab[onclick*='${tabId}']`).classList.add('active');
            }
            
            let allUsers = [];
            let allGroups = [];
            let allDomains = [];
            
            // Fetch all users
            function fetchUsers() {
                return fetch('/get_users')
                    .then(response => response.json())
                    .then(data => {
                        allUsers = data;
                        return data;
                    })
                    .catch(error => {
                        showNotification('error', 'Error fetching users: ' + error.message);
                    });
            }
            
            // Fetch all groups
            function fetchGroups() {
                return fetch('/get_groups')
                    .then(response => response.json())
                    .then(data => {
                        allGroups = data;
                        return data;
                    })
                    .catch(error => {
                        showNotification('error', 'Error fetching groups: ' + error.message);
                    });
            }
            
            // Fetch all domains
            function fetchDomains() {
                return fetch('/get_domains')
                    .then(response => response.json())
                    .then(data => {
                        allDomains = data;
                        return data;
                    })
                    .catch(error => {
                        showNotification('error', 'Error fetching domains: ' + error.message);
                    });
            }
            
            // Display users in table
            function displayUsers(users) {
                const tableBody = document.getElementById('users-table-body');
                
                if (!users || users.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="6">No users found</td></tr>';
                    return;
                }
                
                tableBody.innerHTML = '';
                
                users.forEach(user => {
                    const row = document.createElement('tr');
                    
                    // Username
                    const usernameCell = document.createElement('td');
                    usernameCell.textContent = user.Username;
                    row.appendChild(usernameCell);
                    
                    // Email
                    const emailCell = document.createElement('td');
                    emailCell.textContent = user.Email || '-';
                    row.appendChild(emailCell);
                    
                    // Status
                    const statusCell = document.createElement('td');
                    const statusBadge = document.createElement('span');
                    statusBadge.className = `status-badge ${user.IsActive ? 'status-active' : 'status-inactive'}`;
                    statusCell.appendChild(statusBadge);
                    statusCell.appendChild(document.createTextNode(user.IsActive ? 'Active' : 'Inactive'));
                    row.appendChild(statusCell);
                    
                    // Admin
                    const adminCell = document.createElement('td');
                    adminCell.textContent = user.IsAdmin ? 'Yes' : 'No';
                    row.appendChild(adminCell);
                    
                    // Groups
                    const groupsCell = document.createElement('td');
                    if (user.Groups && user.Groups.length > 0) {
                        const tagList = document.createElement('div');
                        tagList.className = 'tag-list';
                        
                        user.Groups.forEach(group => {
                            const tag = document.createElement('span');
                            tag.className = 'tag group-tag';
                            tag.textContent = group;
                            tagList.appendChild(tag);
                        });
                        
                        groupsCell.appendChild(tagList);
                    } else {
                        groupsCell.textContent = '-';
                    }
                    row.appendChild(groupsCell);
                    
                    // Actions
                    const actionsCell = document.createElement('td');
                    
                    const deleteButton = document.createElement('button');
                    deleteButton.className = 'btn btn-danger';
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = () => confirmDeleteUser(user.Username);
                    
                    actionsCell.appendChild(deleteButton);
                    row.appendChild(actionsCell);
                    
                    tableBody.appendChild(row);
                });
            }
            
            // Display groups in table
            function displayGroups(groups) {
                const tableBody = document.getElementById('groups-table-body');
                
                if (!groups || groups.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="6">No groups found</td></tr>';
                    return;
                }
                
                tableBody.innerHTML = '';
                
                groups.forEach(group => {
                    const row = document.createElement('tr');
                    
                    // Name
                    const nameCell = document.createElement('td');
                    nameCell.textContent = group.Name;
                    row.appendChild(nameCell);
                    
                    // Description
                    const descriptionCell = document.createElement('td');
                    descriptionCell.textContent = group.Description || '-';
                    row.appendChild(descriptionCell);
                    
                    // Role
                    const roleCell = document.createElement('td');
                    roleCell.textContent = group.Role || 'Regular';
                    row.appendChild(roleCell);
                    
                    // Members
                    const membersCell = document.createElement('td');
                    if (group.Users && group.Users.length > 0) {
                        const tagList = document.createElement('div');
                        tagList.className = 'tag-list';
                        
                        group.Users.forEach(user => {
                            const tag = document.createElement('span');
                            tag.className = 'tag';
                            tag.textContent = user;
                            tagList.appendChild(tag);
                        });
                        
                        membersCell.appendChild(tagList);
                    } else {
                        membersCell.textContent = '-';
                    }
                    row.appendChild(membersCell);
                    
                    // Domains
                    const domainsCell = document.createElement('td');
                    if (group.Domains && group.Domains.length > 0) {
                        const tagList = document.createElement('div');
                        tagList.className = 'tag-list';
                        
                        group.Domains.forEach(domain => {
                            const tag = document.createElement('span');
                            tag.className = 'tag domain-tag';
                            tag.textContent = domain;
                            tagList.appendChild(tag);
                        });
                        
                        domainsCell.appendChild(tagList);
                    } else {
                        domainsCell.textContent = '-';
                    }
                    row.appendChild(domainsCell);
                    
                    // Actions
                    const actionsCell = document.createElement('td');
                    
                    const deleteButton = document.createElement('button');
                    deleteButton.className = 'btn btn-danger';
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = () => confirmDeleteGroup(group.Name);
                    
                    actionsCell.appendChild(deleteButton);
                    row.appendChild(actionsCell);
                    
                    tableBody.appendChild(row);
                });
            }
            
            // Populate dropdown options
            function populateDropdowns() {
                // Populate user groups dropdown
                const userGroupsSelect = document.getElementById('user-groups');
                userGroupsSelect.innerHTML = '';
                
                allGroups.forEach(group => {
                    const option = document.createElement('option');
                    option.value = group.Name;
                    option.textContent = group.Name;
                    userGroupsSelect.appendChild(option);
                });
                
                // Populate group users dropdown
                const groupUsersSelect = document.getElementById('group-users');
                groupUsersSelect.innerHTML = '';
                
                allUsers.forEach(user => {
                    const option = document.createElement('option');
                    option.value = user.Username;
                    option.textContent = user.Username;
                    groupUsersSelect.appendChild(option);
                });
                
                // Populate domains dropdown
                const groupDomainsSelect = document.getElementById('group-domains');
                groupDomainsSelect.innerHTML = '';
                
                allDomains.forEach(domain => {
                    const option = document.createElement('option');
                    option.value = domain;
                    option.textContent = domain;
                    groupDomainsSelect.appendChild(option);
                });
            }
            
            // Show notification
            function showNotification(type, message) {
                const notification = document.getElementById('user-notification');
                notification.className = type === 'error' ? 'error-message' : 'success-message';
                notification.textContent = message;
                notification.style.display = 'block';
                
                // Auto-hide after 5 seconds
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 5000);
            }
            
            // Modal functions
            function showAddUserModal() {
                document.getElementById('add-user-modal').style.display = 'block';
            }
            
            function showAddGroupModal() {
                document.getElementById('add-group-modal').style.display = 'block';
            }
            
            function closeModal(modalId) {
                document.getElementById(modalId).style.display = 'none';
            }
            
            // Reset form fields
            function resetForms() {
                document.getElementById('add-user-form').reset();
                document.getElementById('add-group-form').reset();
            }
            
            // Add new user
            function addNewUser(event) {
                event.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const email = document.getElementById('email').value;
                const isActive = document.getElementById('is-active').checked;
                const isAdmin = document.getElementById('is-admin').checked;
                
                // Get selected groups
                const groupsSelect = document.getElementById('user-groups');
                const selectedGroups = Array.from(groupsSelect.selectedOptions).map(option => option.value);
                
                const userData = {
                    username: username,
                    password: password,
                    email: email,
                    isActive: isActive,
                    isAdmin: isAdmin,
                    groups: selectedGroups
                };
                
                fetch('/add_user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('success', data.message);
                        closeModal('add-user-modal');
                        resetForms();
                        refreshUsers();
                    } else {
                        showNotification('error', data.error || 'Failed to add user');
                    }
                })
                .catch(error => {
                    showNotification('error', 'Error adding user: ' + error.message);
                });
            }
            
            // Add new group
            function addNewGroup(event) {
                event.preventDefault();
                
                const groupName = document.getElementById('group-name').value;
                const description = document.getElementById('group-description').value;
                const role = document.getElementById('group-role').value;
                const readOnly = document.getElementById('read-only').checked;
                
                // Get selected users
                const usersSelect = document.getElementById('group-users');
                const selectedUsers = Array.from(usersSelect.selectedOptions).map(option => option.value);
                
                // Get selected domains
                const domainsSelect = document.getElementById('group-domains');
                const selectedDomains = Array.from(domainsSelect.selectedOptions).map(option => option.value);
                
                const groupData = {
                    groupName: groupName,
                    description: description,
                    role: role,
                    users: selectedUsers,
                    domains: selectedDomains,
                    readOnly: readOnly
                };
                
                fetch('/add_group', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(groupData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('success', data.message);
                        closeModal('add-group-modal');
                        resetForms();
                        refreshGroups();
                    } else {
                        showNotification('error', data.error || 'Failed to add group');
                    }
                })
                .catch(error => {
                    showNotification('error', 'Error adding group: ' + error.message);
                });
            }
            
            // Confirm delete user
            function confirmDeleteUser(username) {
                if (confirm(`Are you sure you want to delete user "${username}"?`)) {
                    deleteUser(username);
                }
            }
            
            // Delete user
            function deleteUser(username) {
                fetch('/delete_user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username: username })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('success', data.message);
                        refreshUsers();
                    } else {
                        showNotification('error', data.error || 'Failed to delete user');
                    }
                })
                .catch(error => {
                    showNotification('error', 'Error deleting user: ' + error.message);
                });
            }
            
            // Confirm delete group
            function confirmDeleteGroup(groupName) {
                if (confirm(`Are you sure you want to delete group "${groupName}"?`)) {
                    deleteGroup(groupName);
                }
            }
            
            // Delete group
            function deleteGroup(groupName) {
                fetch('/delete_group', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ groupName: groupName })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('success', data.message);
                        refreshGroups();
                    } else {
                        showNotification('error', data.error || 'Failed to delete group');
                    }
                })
                .catch(error => {
                    showNotification('error', 'Error deleting group: ' + error.message);
                });
            }
            
            // Refresh users data
            function refreshUsers() {
                fetchUsers().then(users => {
                    displayUsers(users);
                    populateDropdowns();
                });
            }
            
            // Refresh groups data
            function refreshGroups() {
                fetchGroups().then(groups => {
                    displayGroups(groups);
                    populateDropdowns();
                });
            }
            
            // Initialize user management when Users tab is clicked
            document.querySelector('.tab-button[onclick="openTab(\'users\')"]').addEventListener('click', initUserManagement);
            
            // Initialize user management
            function initUserManagement() {
                // Only initialize once
                if (!window.userManagementInitialized) {
                    // Fetch all data
                    Promise.all([fetchUsers(), fetchGroups(), fetchDomains()])
                    .then(([users, groups, domains]) => {
                        displayUsers(users);
                        displayGroups(groups);
                        populateDropdowns();
                    })
                    .catch(error => {
                        showNotification('error', 'Error initializing user management: ' + error.message);
                    });
                    
                    window.userManagementInitialized = true;
                }
            }
            
            // Close modals when clicking outside
            window.addEventListener('click', function(event) {
                const modals = document.getElementsByClassName('modal');
                for (let i = 0; i < modals.length; i++) {
                    if (event.target === modals[i]) {
                        modals[i].style.display = 'none';
                    }
                }
            });
        </script>
        {% else %}
        <script>
            // Basic initialization for error state
            const allResources = [];
            const allFolders = [];
            
            document.getElementById('resourceSearch').addEventListener('input', function(e) {
                alert('Search functionality is not available when disconnected from CloudShell.');
            });
            
            // Tab switching functionality
            function openTab(tabName) {
                // Hide all tab contents
                const tabContents = document.getElementsByClassName("tab-content");
                for (let i = 0; i < tabContents.length; i++) {
                    tabContents[i].classList.remove("active");
                }
                
                // Deactivate all tab buttons
                const tabButtons = document.getElementsByClassName("tab-button");
                for (let i = 0; i < tabButtons.length; i++) {
                    tabButtons[i].classList.remove("active");
                }
                
                // Show the selected tab content and activate the button
                document.getElementById(tabName).classList.add("active");
                document.querySelector(`.tab-button[onclick="openTab('${tabName}')"]`).classList.add("active");
            }
        </script>
        {% endif %}
    </body>
    </html>
    """
