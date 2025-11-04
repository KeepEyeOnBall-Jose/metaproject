import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function TaskList({ tasks, repositories, onAssignRepository }) {
  const [expandedTasks, setExpandedTasks] = useState(new Set());

  const toggleTask = (taskId) => {
    const newExpanded = new Set(expandedTasks);
    if (newExpanded.has(taskId)) {
      newExpanded.delete(taskId);
    } else {
      newExpanded.add(taskId);
    }
    setExpandedTasks(newExpanded);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return '#dc3545';
      case 'high': return '#fd7e14';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getPriorityLabel = (priority) => {
    if (!priority) return 'No Priority';
    return priority.charAt(0).toUpperCase() + priority.slice(1);
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Tasks ({tasks.length})</h2>
      {tasks.length === 0 ? (
        <p style={{ color: '#6c757d', fontStyle: 'italic' }}>No tasks found</p>
      ) : (
        tasks.map((task) => (
          <div
            key={task.id}
            style={{
              border: '2px solid #007bff',
              borderRadius: '8px',
              padding: '15px',
              marginBottom: '15px',
              backgroundColor: '#f8f9fa',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#212529' }}>{task.question}</h3>

                {/* Task metadata */}
                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '10px' }}>
                  {/* Priority badge */}
                  <span
                    style={{
                      backgroundColor: getPriorityColor(task.priority),
                      color: 'white',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: 'bold',
                    }}
                  >
                    {getPriorityLabel(task.priority)}
                  </span>

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
                    {task.category}
                  </span>

                  {/* Status */}
                  <span
                    style={{
                      backgroundColor: task.status === 'open' ? '#17a2b8' : '#28a745',
                      color: 'white',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '12px',
                    }}
                  >
                    {task.status}
                  </span>

                  {/* Due date */}
                  {task.due_date && (
                    <span
                      style={{
                        backgroundColor: '#e9ecef',
                        color: '#495057',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '12px',
                      }}
                    >
                      📅 {new Date(task.due_date).toLocaleDateString()}
                    </span>
                  )}

                  {/* Assignee */}
                  {task.assignee && (
                    <span
                      style={{
                        backgroundColor: '#e9ecef',
                        color: '#495057',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '12px',
                      }}
                    >
                      👤 {task.assignee}
                    </span>
                  )}
                </div>

                {/* Repository assignment */}
                <div style={{ marginTop: '10px', display: 'flex', gap: '10px', alignItems: 'center' }}>
                  <label style={{ fontSize: '14px', fontWeight: 'bold' }}>Repository:</label>
                  <select
                    value={task.repository || ''}
                    onChange={(e) => onAssignRepository && onAssignRepository(task.id, e.target.value)}
                    style={{
                      padding: '6px 12px',
                      borderRadius: '4px',
                      border: '1px solid #ced4da',
                      fontSize: '14px',
                      backgroundColor: 'white',
                    }}
                  >
                    <option value="">Select repository...</option>
                    {repositories.map((repo) => (
                      <option key={repo.name} value={repo.name}>
                        {repo.name} - {repo.description}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Action buttons */}
                <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => toggleTask(task.id)}
                    style={{
                      backgroundColor: '#007bff',
                      color: 'white',
                      border: 'none',
                      padding: '6px 12px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '14px',
                    }}
                  >
                    {expandedTasks.has(task.id) ? 'Hide Details' : 'Show Details'}
                  </button>

                  {task.repository && (
                    <>
                      <button
                        style={{
                          backgroundColor: '#28a745',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '14px',
                        }}
                      >
                        Create Issue in {task.repository}
                      </button>
                      <button
                        style={{
                          backgroundColor: '#17a2b8',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '14px',
                        }}
                      >
                        View Repo
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>

            {/* Expanded details */}
            {expandedTasks.has(task.id) && task.answer && (
              <div
                style={{
                  marginTop: '15px',
                  padding: '15px',
                  backgroundColor: 'white',
                  borderRadius: '6px',
                  borderLeft: '4px solid #007bff',
                  animation: 'fadeIn 0.3s ease-in',
                }}
              >
                <h4 style={{ marginTop: 0, color: '#495057' }}>Details:</h4>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {task.answer}
                </ReactMarkdown>
              </div>
            )}

            {/* Task metadata footer */}
            <div style={{ marginTop: '10px', fontSize: '12px', color: '#6c757d' }}>
              <span>ID: {task.id}</span>
              {task.google_sheet_id && (
                <span style={{ marginLeft: '15px' }}>
                  📊 Synced from Google Sheets
                </span>
              )}
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

export default TaskList;
