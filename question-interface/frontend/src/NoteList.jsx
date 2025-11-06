import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function NoteList({ notes }) {
  const [expandedNotes, setExpandedNotes] = useState(new Set());

  const toggleNote = (noteId) => {
    const newExpanded = new Set(expandedNotes);
    if (newExpanded.has(noteId)) {
      newExpanded.delete(noteId);
    } else {
      newExpanded.add(noteId);
    }
    setExpandedNotes(newExpanded);
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Notes ({notes.length})</h2>
      {notes.length === 0 ? (
        <p style={{ color: '#6c757d', fontStyle: 'italic' }}>No notes found</p>
      ) : (
        notes.map((note) => (
          <div
            key={note.id}
            style={{
              border: '2px solid #28a745',
              borderRadius: '8px',
              padding: '15px',
              marginBottom: '15px',
              backgroundColor: '#f8f9fa',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#212529' }}>{note.question}</h3>

                {/* Note metadata */}
                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '10px' }}>
                  {/* Category */}
                  <span
                    style={{
                      backgroundColor: '#6c757d',
                      color: 'white',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '12px',
                    }}
                  >
                    {note.category}
                  </span>

                  {/* Status */}
                  <span
                    style={{
                      backgroundColor: note.status === 'open' ? '#17a2b8' : '#28a745',
                      color: 'white',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '12px',
                    }}
                  >
                    {note.status}
                  </span>

                  {/* Created date */}
                  <span
                    style={{
                      backgroundColor: '#e9ecef',
                      color: '#495057',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '12px',
                    }}
                  >
                    📅 {new Date(note.created_at).toLocaleDateString()}
                  </span>
                </div>

                {/* Action button */}
                <button
                  onClick={() => toggleNote(note.id)}
                  style={{
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    padding: '6px 12px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    marginTop: '8px',
                  }}
                >
                  {expandedNotes.has(note.id) ? 'Hide Content' : 'Show Content'}
                </button>
              </div>
            </div>

            {/* Expanded content */}
            {expandedNotes.has(note.id) && note.answer && (
              <div
                style={{
                  marginTop: '15px',
                  padding: '15px',
                  backgroundColor: 'white',
                  borderRadius: '6px',
                  borderLeft: '4px solid #28a745',
                  animation: 'fadeIn 0.3s ease-in',
                }}
              >
                <h4 style={{ marginTop: 0, color: '#495057' }}>Content:</h4>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {note.answer}
                </ReactMarkdown>
              </div>
            )}

            {/* Note metadata footer */}
            <div style={{ marginTop: '10px', fontSize: '12px', color: '#6c757d' }}>
              <span>ID: {note.id}</span>
            </div>
          </div>
        ))
      )}

      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}

export default NoteList;
