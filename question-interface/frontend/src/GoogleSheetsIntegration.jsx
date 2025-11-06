import React, { useState, useEffect } from 'react';
import axios from 'axios';

function GoogleSheetsIntegration({ baseUrl, onImportComplete }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [availableSheets, setAvailableSheets] = useState([]);
  const [selectedSheet, setSelectedSheet] = useState('');
  const [isImporting, setIsImporting] = useState(false);
  const [importStatus, setImportStatus] = useState(null);

  const handleGoogleAuth = () => {
    // In a real implementation, this would open Google OAuth flow
    const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID';
    const REDIRECT_URI = window.location.origin + '/oauth2callback';
    const SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly https://www.googleapis.com/auth/drive.readonly';

    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=token&scope=${SCOPE}`;

    // Open OAuth window
    const authWindow = window.open(authUrl, 'Google Auth', 'width=500,height=600');

    // Listen for OAuth callback
    window.addEventListener('message', async (event) => {
      if (event.data.type === 'GOOGLE_AUTH_SUCCESS') {
        try {
          await axios.post(`${baseUrl}/google/auth`, {
            access_token: event.data.access_token
          });
          setIsAuthenticated(true);
          loadGoogleSheets();
        } catch (error) {
          console.error('Auth failed:', error);
        }
      }
    });
  };

  const loadGoogleSheets = async () => {
    try {
      const response = await axios.get(`${baseUrl}/google/sheets/list`);
      setAvailableSheets(response.data.sheets || []);
    } catch (error) {
      console.error('Failed to load Google Sheets:', error);
    }
  };

  const handleImport = async () => {
    if (!selectedSheet) {
      alert('Please select a Google Sheet to import');
      return;
    }

    setIsImporting(true);
    setImportStatus(null);

    try {
      const response = await axios.post(`${baseUrl}/google/sheets/import`, {
        spreadsheet_id: selectedSheet,
        range: 'A1:Z1000'
      });

      setImportStatus({
        type: 'success',
        message: `Successfully imported ${response.data.items_imported} tasks from Google Sheets`
      });

      if (onImportComplete) {
        onImportComplete();
      }
    } catch (error) {
      setImportStatus({
        type: 'error',
        message: 'Failed to import from Google Sheets: ' + error.message
      });
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <div
      style={{
        backgroundColor: '#fff',
        border: '2px solid #4285f4',
        borderRadius: '8px',
        padding: '20px',
        marginBottom: '20px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      }}
    >
      <h3 style={{ marginTop: 0, color: '#4285f4', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span>📊</span>
        Google Sheets Integration
      </h3>

      {!isAuthenticated ? (
        <div>
          <p style={{ color: '#6c757d' }}>
            Connect to Google Drive to import tasks from your Google Sheets documents.
          </p>
          <button
            onClick={handleGoogleAuth}
            style={{
              backgroundColor: '#4285f4',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
            }}
          >
            <svg width="18" height="18" viewBox="0 0 18 18">
              <path fill="white" d="M9 3.48c1.69 0 2.83.73 3.48 1.34l2.54-2.48C13.46.89 11.43 0 9 0 5.48 0 2.44 2.02.96 4.96l2.91 2.26C4.6 5.05 6.62 3.48 9 3.48z"/>
              <path fill="white" d="M17.64 9.2c0-.74-.06-1.28-.19-1.84H9v3.34h4.96c-.1.83-.64 2.08-1.84 2.92l2.84 2.2c1.7-1.57 2.68-3.88 2.68-6.62z"/>
              <path fill="white" d="M3.88 10.78A5.54 5.54 0 0 1 3.58 9c0-.62.11-1.22.29-1.78L.96 4.96A9.008 9.008 0 0 0 0 9c0 1.45.35 2.82.96 4.04l2.92-2.26z"/>
              <path fill="white" d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.84-2.2c-.76.53-1.78.9-3.12.9-2.38 0-4.4-1.57-5.12-3.74L.97 13.04C2.45 15.98 5.48 18 9 18z"/>
            </svg>
            Sign in with Google
          </button>

          {/* Development notice */}
          <div
            style={{
              marginTop: '15px',
              padding: '10px',
              backgroundColor: '#fff3cd',
              borderLeft: '4px solid #ffc107',
              borderRadius: '4px',
            }}
          >
            <p style={{ margin: 0, fontSize: '14px', color: '#856404' }}>
              <strong>Note:</strong> Google Sheets integration requires Google OAuth credentials.
              The placeholder endpoints are ready - you'll need to add your Google Cloud Project credentials.
            </p>
          </div>
        </div>
      ) : (
        <div>
          <p style={{ color: '#28a745', fontWeight: 'bold' }}>✓ Connected to Google Drive</p>

          <div style={{ marginTop: '15px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
              Select a Google Sheet to import:
            </label>
            <select
              value={selectedSheet}
              onChange={(e) => setSelectedSheet(e.target.value)}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ced4da',
                fontSize: '14px',
              }}
            >
              <option value="">Choose a spreadsheet...</option>
              {availableSheets.map((sheet) => (
                <option key={sheet.id} value={sheet.id}>
                  {sheet.name}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleImport}
            disabled={!selectedSheet || isImporting}
            style={{
              backgroundColor: selectedSheet && !isImporting ? '#28a745' : '#6c757d',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '4px',
              cursor: selectedSheet && !isImporting ? 'pointer' : 'not-allowed',
              fontSize: '16px',
              marginTop: '15px',
              fontWeight: 'bold',
            }}
          >
            {isImporting ? 'Importing...' : 'Import Tasks from Sheet'}
          </button>

          {importStatus && (
            <div
              style={{
                marginTop: '15px',
                padding: '10px',
                backgroundColor: importStatus.type === 'success' ? '#d4edda' : '#f8d7da',
                borderLeft: `4px solid ${importStatus.type === 'success' ? '#28a745' : '#dc3545'}`,
                borderRadius: '4px',
              }}
            >
              <p style={{ margin: 0, fontSize: '14px', color: importStatus.type === 'success' ? '#155724' : '#721c24' }}>
                {importStatus.message}
              </p>
            </div>
          )}

          {/* Instructions */}
          <div
            style={{
              marginTop: '15px',
              padding: '10px',
              backgroundColor: '#e7f3ff',
              borderLeft: '4px solid #007bff',
              borderRadius: '4px',
            }}
          >
            <p style={{ margin: 0, fontSize: '12px', color: '#004085' }}>
              <strong>Expected format:</strong> Your Google Sheet should have columns for: Task, Category, Priority, Repository, Assignee, Due Date
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default GoogleSheetsIntegration;
