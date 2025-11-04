import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ConceptCloud from './ConceptCloud';
import QuestionList from './QuestionList';

function App() {
  const [questions, setQuestions] = useState([]);
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [llmAnalysis, setLlmAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [viewMode, setViewMode] = useState('manual'); // 'manual' or 'ai'
  const [selectedModel, setSelectedModel] = useState(0); // Index of selected model analysis

  // Determine backend URL based on current protocol
  const isHttps = window.location.protocol === 'https:';
  const backendPort = isHttps ? '8443' : '8000';
  const backendProtocol = isHttps ? 'https:' : 'http:';
  const baseUrl = `${backendProtocol}//localhost:${backendPort}`;

  useEffect(() => {

    // Load questions
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

    axios.get(`${baseUrl}/categories`).then(res => setCategories(res.data));
  }, []);

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

  const filteredQuestions = selectedCategory ? questions.filter(q => q.category === selectedCategory) : questions;

  return (
    <div style={{ padding: '20px' }}>
      <h1>Question Tracker</h1>

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

      <ConceptCloud
        categories={categories}
        llmAnalysis={llmAnalysis?.analyses?.[selectedModel] || null}
        viewMode={viewMode}
        onSelectCategory={setSelectedCategory}
      />
      <QuestionList questions={filteredQuestions} />
    </div>
  );
}

export default App;