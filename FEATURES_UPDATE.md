# Metaproject - Notes & Tasks Split Feature Update

## Overview
This update transforms the Metaproject from a simple question tracker into a comprehensive **Notes & Tasks Manager** with advanced features for organizing, prioritizing, and actioning items across your company's software surface.

## Key Changes

### 1. Notes vs Tasks Separation
- **Notes**: Knowledge items, questions, learnings, and reference material
- **Tasks**: Actionable items that can be assigned to repositories, team members, and tracked with priorities and due dates

### 2. Enhanced Data Model

#### New Fields Added to Questions Model:
```python
type: str = "note" | "task"  # Item classification
repository: str              # Target repository for tasks
priority: str                # "low" | "medium" | "high" | "urgent"
assignee: str                # Person assigned to the task
due_date: str                # ISO date string
google_sheet_id: str         # For synced items from Google Sheets
```

### 3. New UI Components

#### TaskList Component (`TaskList.jsx`)
- **Priority-based color coding**: Visual indicators for task urgency
- **Repository assignment**: Dropdown selector for company repositories
- **Action buttons**:
  - Create GitHub issues directly
  - View repository links
  - Show/hide task details
- **Rich metadata display**: Priority, assignee, due date, status
- **Expandable details**: Full task description with markdown support

#### NoteList Component (`NoteList.jsx`)
- Clean, focused display for knowledge items
- Simplified metadata (category, status, date)
- Expandable content with markdown rendering
- Green color scheme to differentiate from tasks

#### GoogleSheetsIntegration Component (`GoogleSheetsIntegration.jsx`)
- Google OAuth authentication flow
- Browse and select from your Google Sheets
- Import tasks directly from spreadsheets
- Status feedback for imports
- Expected format instructions

### 4. New Backend API Endpoints

#### Separation Endpoints:
```
GET /notes        # Returns only items with type="note"
GET /tasks        # Returns only items with type="task"
```

#### Repository Management:
```
GET /repositories # Returns list of available repositories
```

#### Google Drive/Sheets Integration:
```
POST /google/auth              # Handle Google OAuth
GET  /google/sheets/list       # List available spreadsheets
POST /google/sheets/import     # Import tasks from a sheet
```

### 5. Enhanced User Interface

#### Tab Navigation:
- **Tasks Tab**: View all actionable items with repository assignment
- **Notes Tab**: Browse knowledge base and reference material
- **All Tab**: Combined view of everything (legacy view)

#### Visual Design:
- Color-coded priorities (Red: Urgent, Orange: High, Yellow: Medium, Green: Low)
- Distinct border colors (Blue: Tasks, Green: Notes)
- Clean, modern card-based layout
- Responsive design for various screen sizes

### 6. Repository Integration
Predefined company repositories:
- `metaproject` - Main metaproject repository
- `question-interface` - Question tracking interface
- `backend-api` - Backend API services
- `frontend-app` - Frontend application

Tasks can be:
1. Assigned to specific repositories
2. Converted to GitHub issues (placeholder for full integration)
3. Tracked by repository ownership

### 7. Google Sheets Integration (Framework Ready)

The application now includes placeholder endpoints and UI for:
- Google OAuth authentication
- Browsing Google Drive spreadsheets
- Importing task lists from Google Sheets
- Syncing updates (marked with google_sheet_id)

**Note**: Full implementation requires:
- Google Cloud Project credentials
- OAuth client ID and secret
- Google Sheets API enabled

### 8. Updated Sample Data

The `questions.csv` now includes:
- 11 tasks with varied priorities, repositories, and due dates
- 14 notes for reference and learning
- All items properly tagged with the new fields

## Technical Implementation

### Dependencies Added:
```
Backend:
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client

Frontend:
- (No new dependencies - using existing React, Axios, Markdown)
```

### File Structure:
```
question-interface/
├── backend/
│   ├── main.py                    # Updated with new models & endpoints
│   └── requirements.txt           # Added Google API dependencies
├── frontend/
│   └── src/
│       ├── App.jsx                # Updated with tabs & new state
│       ├── TaskList.jsx           # NEW - Task-specific UI
│       ├── NoteList.jsx           # NEW - Note-specific UI
│       └── GoogleSheetsIntegration.jsx  # NEW - Google integration
└── metaproject-life/
    └── data/
        └── questions.csv          # Updated with new columns
```

## Usage Guide

### Viewing Tasks vs Notes
1. Start the application
2. Click the **Tasks** tab to view actionable items
3. Click the **Notes** tab to browse knowledge items
4. Use the **All** tab for the complete view

### Assigning a Task to a Repository
1. Navigate to the **Tasks** tab
2. Select a repository from the dropdown in any task card
3. The task is now associated with that repo
4. Action buttons appear to create issues or view the repo

### Importing from Google Sheets
1. Click "Sign in with Google" in the integration panel
2. Authenticate with your Google account
3. Select a spreadsheet from the dropdown
4. Click "Import Tasks from Sheet"
5. Tasks are automatically added to your list

### Task Priority System
- **Urgent** (Red): Critical, needs immediate attention
- **High** (Orange): Important, high priority
- **Medium** (Yellow): Normal priority
- **Low** (Green): Nice to have, low priority

## Future Enhancements

Potential additions based on this foundation:
1. Full GitHub integration for issue creation
2. Real-time Google Sheets sync (two-way)
3. Task status transitions (to-do → in-progress → done)
4. Team collaboration features
5. Task dependencies and sub-tasks
6. Calendar view for due dates
7. Email notifications for upcoming tasks
8. Export to various formats (JSON, PDF, CSV)

## Breaking Changes

None. The update is backward compatible:
- Old data without new fields defaults to `type="note"`
- All existing endpoints continue to work
- The `/questions` endpoint returns all items (notes + tasks)

## Migration Guide

If you have existing data:
1. Backup your current `questions.csv`
2. Add new columns: `type,repository,priority,assignee,due_date,google_sheet_id`
3. Set `type` to "note" or "task" for each row
4. Leave task-specific fields empty for notes
5. Restart the backend to load the new schema

## Development Notes

### Testing the Features:
```bash
# Backend
cd question-interface/backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd question-interface/frontend
npm install
npm run dev
```

### Adding More Repositories:
Edit the `/repositories` endpoint in `backend/main.py` to add your company's actual repositories.

### Customizing Priorities:
Modify the `getPriorityColor()` function in `TaskList.jsx` to use your team's priority system.

## Summary

This update transforms Metaproject into a powerful dual-purpose tool:
- **Note-taking** for capturing knowledge and learning
- **Task management** for actionable items across your software surface

The separation allows for better organization, clearer priorities, and seamless integration with your development workflow through repository assignments and Google Sheets imports.
