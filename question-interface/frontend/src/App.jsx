import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ConceptCloud from './ConceptCloud';
import QuestionList from './QuestionList';
import TaskList from './TaskList';
import NoteList from './NoteList';
import GoogleSheetsIntegration from './GoogleSheetsIntegration';

function App() {
  const [questions, setQuestions] = useState([]);
  const [notes, setNotes] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [repositories, setRepositories] = useState([]);
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [llmAnalysis, setLlmAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [viewMode, setViewMode] = useState('manual'); // 'manual' or 'ai'
  const [selectedModel, setSelectedModel] = useState(0); // Index of selected model analysis
  const [activeTab, setActiveTab] = useState('tasks'); // 'tasks' or 'notes' or 'all'

  // Determine backend URL based on current protocol
  const isHttps = window.location.protocol === 'https:';
  const backendPort = isHttps ? '8443' : '8000';
  const backendProtocol = isHttps ? 'https:' : 'http:';
  const baseUrl = `${backendProtocol}//localhost:${backendPort}`;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    // Load all questions
    axios.get(`${baseUrl}/questions`).then(res => {
      const questionsData = res.data;
      setQuestions(questionsData);

      // Load answers for all questions
      questionsData.forEach(question => {
        axios.get(`${baseUrl}/questions/${question.id}/answer`)
          .then(answerRes => {
            if (answerRes.data.has_answer) {
              // Update the question with its answer
              setQuestions(prev => prev.map(q =>
                q.id === question.id
                  ? { ...q, answer: answerRes.data.answer }
                  : q
              ));
            }
          })
          .catch(err => console.error(`Failed to load answer for ${question.id}:`, err));
      });
    });

    // Load notes
    axios.get(`${baseUrl}/notes`).then(res => {
      const notesData = res.data;
      setNotes(notesData);

      // Load answers for notes
      notesData.forEach(note => {
        axios.get(`${baseUrl}/questions/${note.id}/answer`)
          .then(answerRes => {
            if (answerRes.data.has_answer) {
              setNotes(prev => prev.map(n =>
                n.id === note.id
                  ? { ...n, answer: answerRes.data.answer }
                  : n
              ));
            }
          })
          .catch(err => console.error(`Failed to load answer for ${note.id}:`, err));
      });
    });

    // Load tasks
    axios.get(`${baseUrl}/tasks`).then(res => {
      const tasksData = res.data;
      setTasks(tasksData);

      // Load answers for tasks
      tasksData.forEach(task => {
        axios.get(`${baseUrl}/questions/${task.id}/answer`)
          .then(answerRes => {
            if (answerRes.data.has_answer) {
              setTasks(prev => prev.map(t =>
                t.id === task.id
                  ? { ...t, answer: answerRes.data.answer }
                  : t
              ));
            }
          })
          .catch(err => console.error(`Failed to load answer for ${task.id}:`, err));
      });
    });

    // Load repositories
    axios.get(`${baseUrl}/repositories`).then(res => {
      setRepositories(res.data);
    });

    axios.get(`${baseUrl}/categories`).then(res => setCategories(res.data));
  };

  const handleAnalyzeWithAI = async () => {
    setIsAnalyzing(true);
    try {
      // Prepare questions with answers for analysis
      const questionsForAnalysis = questions.map(q => ({
        id: q.id,
        question: q.question,
        answer: q.answer || '',
        category: q.category
      }));

      const response = await axios.post(`${baseUrl}/analyze/concepts`, {
        questions: questionsForAnalysis
      });

      setLlmAnalysis(response.data);
      setSelectedModel(0); // Start with first model analysis
      setViewMode('ai');
    } catch (error) {
      console.error('AI analysis failed:', error);
      // Fallback to basic category-based clusters
      const basicClusters = Object.keys(categories).map(cat => ({
        name: cat,
        description: `Questions in ${cat} category`,
        question_ids: questions.filter(q => q.category === cat).map(q => q.id)
      }));

      setLlmAnalysis({
        analyses: [{
          model_name: "Fallback Analysis",
          concepts: questions.map(q => ({ question_id: q.id, concepts: [q.category] })),
          relationships: [],
          suggested_clusters: basicClusters
        }],
        fallback_used: true
      });
      setSelectedModel(0);
      setViewMode('ai');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleAssignRepository = async (taskId, repoName) => {
    // In a real implementation, this would make an API call to update the task
    console.log(`Assigning repository ${repoName} to task ${taskId}`);

    // Update local state
    setTasks(prev => prev.map(t =>
      t.id === taskId ? { ...t, repository: repoName } : t
    ));

    // Also update in all questions
    setQuestions(prev => prev.map(q =>
      q.id === taskId ? { ...q, repository: repoName } : q
    ));
  };

  const handleImportComplete = () => {
    // Reload data after import
    loadData();
  };

  const filteredQuestions = selectedCategory ? questions.filter(q => q.category === selectedCategory) : questions;
  const filteredTasks = selectedCategory ? tasks.filter(t => t.category === selectedCategory) : tasks;
  const filteredNotes = selectedCategory ? notes.filter(n => n.category === selectedCategory) : notes;

  return (
    <div style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
      <h1 style={{ color: '#212529', marginBottom: '10px' }}>
        Metaproject - Notes & Tasks Manager
      </h1>
      <p style={{ color: '#6c757d', marginBottom: '30px' }}>
        Track your notes and tasks with AI-powered insights and repository integration
      </p>

      {/* AI Analysis Controls */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', alignItems: 'center' }}>
        <button
          onClick={handleAnalyzeWithAI}
          disabled={isAnalyzing}
          style={{
            backgroundColor: isAnalyzing ? '#6c757d' : '#28a745',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: isAnalyzing ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
          }}
        >
          {isAnalyzing ? '🤖 Analyzing...' : '🧠 Analyze with AI'}
        </button>

        {llmAnalysis && (
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={() => setViewMode('manual')}
              style={{
                backgroundColor: viewMode === 'manual' ? '#007bff' : '#6c757d',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Manual Categories
            </button>

            {llmAnalysis.analyses && llmAnalysis.analyses.length > 0 && (
              <>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(parseInt(e.target.value))}
                  style={{
                    padding: '8px 12px',
                    borderRadius: '4px',
                    border: '1px solid #ccc',
                    backgroundColor: 'white',
                  }}
                >
                  {llmAnalysis.analyses.map((analysis, index) => (
                    <option key={index} value={index}>
                      {analysis.model_name} ({analysis.suggested_clusters?.length || 0} clusters)
                      {analysis.error ? ' ⚠️' : ''}
                    </option>
                  ))}
                </select>

                <button
                  onClick={() => setViewMode('ai')}
                  style={{
                    backgroundColor: viewMode === 'ai' ? '#007bff' : '#6c757d',
                    color: 'white',
                    border: 'none',
                    padding: '8px 16px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  }}
                >
                  AI Clusters
                </button>

                {llmAnalysis.fallback_used && (
                  <span style={{ color: '#856404', backgroundColor: '#fff3cd', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>
                    ⚠️ Fallback analysis used
                  </span>
                )}
              </>
            )}
          </div>
        )}
      </div>

      {/* Google Sheets Integration */}
      <GoogleSheetsIntegration baseUrl={baseUrl} onImportComplete={handleImportComplete} />

      {/* Tabs for Notes/Tasks/All */}
      <div style={{ marginBottom: '20px', borderBottom: '2px solid #dee2e6' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setActiveTab('tasks')}
            style={{
              backgroundColor: activeTab === 'tasks' ? '#007bff' : 'transparent',
              color: activeTab === 'tasks' ? 'white' : '#495057',
              border: 'none',
              borderBottom: activeTab === 'tasks' ? '3px solid #007bff' : '3px solid transparent',
              padding: '12px 24px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: activeTab === 'tasks' ? 'bold' : 'normal',
              transition: 'all 0.3s ease',
            }}
          >
            Tasks ({tasks.length})
          </button>
          <button
            onClick={() => setActiveTab('notes')}
            style={{
              backgroundColor: activeTab === 'notes' ? '#28a745' : 'transparent',
              color: activeTab === 'notes' ? 'white' : '#495057',
              border: 'none',
              borderBottom: activeTab === 'notes' ? '3px solid #28a745' : '3px solid transparent',
              padding: '12px 24px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: activeTab === 'notes' ? 'bold' : 'normal',
              transition: 'all 0.3s ease',
            }}
          >
            Notes ({notes.length})
          </button>
          <button
            onClick={() => setActiveTab('all')}
            style={{
              backgroundColor: activeTab === 'all' ? '#6c757d' : 'transparent',
              color: activeTab === 'all' ? 'white' : '#495057',
              border: 'none',
              borderBottom: activeTab === 'all' ? '3px solid #6c757d' : '3px solid transparent',
              padding: '12px 24px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: activeTab === 'all' ? 'bold' : 'normal',
              transition: 'all 0.3s ease',
            }}
          >
            All ({questions.length})
          </button>
        </div>
      </div>

      <ConceptCloud
        categories={categories}
        llmAnalysis={llmAnalysis?.analyses?.[selectedModel] || null}
        viewMode={viewMode}
        onSelectCategory={setSelectedCategory}
      />

      {/* Render content based on active tab */}
      {activeTab === 'tasks' && (
        <TaskList
          tasks={filteredTasks}
          repositories={repositories}
          onAssignRepository={handleAssignRepository}
        />
      )}
      {activeTab === 'notes' && (
        <NoteList notes={filteredNotes} />
      )}
      {activeTab === 'all' && (
        <QuestionList questions={filteredQuestions} />
      )}
    </div>
  );
}

export default App;