import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// Add fade-in animation CSS
const fadeInKeyframes = `
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
`;

// Inject the keyframes into the document head
if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.textContent = fadeInKeyframes;
  document.head.appendChild(style);
}

function QuestionList({ questions }) {
  const [expandedAnswers, setExpandedAnswers] = useState(new Set());

  const toggleAnswer = (questionId) => {
    const newExpanded = new Set(expandedAnswers);
    if (newExpanded.has(questionId)) {
      newExpanded.delete(questionId);
    } else {
      newExpanded.add(questionId);
    }
    setExpandedAnswers(newExpanded);
  };

  return (
    <div style={{ marginTop: '20px' }}>
      {questions.map((q, index) => {
        const hasAnswer = q.answer && q.answer.trim().length > 0;
        const isExpanded = expandedAnswers.has(q.id);

        return (
          <div
            key={`${q.id}-${index}`}
            style={{
              marginBottom: '30px',
              padding: '20px',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
              backgroundColor: '#fff',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            }}
          >
            <div style={{ marginBottom: '10px' }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#2c3e50' }}>
                {hasAnswer ? '📝 ' : '❓ '}
                {q.question}
              </h3>
              <div style={{ fontSize: '14px', color: '#7f8c8d' }}>
                <span style={{ marginRight: '15px' }}>
                  <strong>Category:</strong> {q.category}
                </span>
                <span style={{ marginRight: '15px' }}>
                  <strong>Status:</strong> {q.status}
                </span>
                <span>
                  <strong>ID:</strong> {q.id}
                </span>
              </div>
            </div>

            {hasAnswer && (
              <div style={{ marginTop: '15px' }}>
                <button
                  onClick={() => toggleAnswer(q.id)}
                  style={{
                    backgroundColor: isExpanded ? '#6c757d' : '#667eea',
                    color: 'white',
                    border: 'none',
                    padding: '8px 16px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    transition: 'background-color 0.2s',
                  }}
                  onMouseOver={(e) => {
                    e.target.style.backgroundColor = isExpanded ? '#5a6268' : '#5a67d8';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.backgroundColor = isExpanded ? '#6c757d' : '#667eea';
                  }}
                >
                  {isExpanded ? 'Hide Answer' : 'Show Answer'}
                </button>

                {isExpanded && (
                  <div
                    style={{
                      marginTop: '15px',
                      padding: '15px',
                      backgroundColor: '#f8f9fa',
                      borderRadius: '4px',
                      borderLeft: '4px solid #667eea',
                      animation: 'fadeIn 0.3s ease-in',
                    }}
                  >
                    <h4 style={{ marginTop: 0, color: '#667eea' }}>Answer:</h4>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {q.answer}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default QuestionList;