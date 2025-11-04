import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ConceptCloud from './ConceptCloud';
import QuestionList from './QuestionList';

function App() {
  const [questions, setQuestions] = useState([]);
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
    // Determine backend URL based on current protocol
    const isHttps = window.location.protocol === 'https:';
    const backendPort = isHttps ? '8443' : '8000';
    const backendProtocol = isHttps ? 'https:' : 'http:';
    const baseUrl = `${backendProtocol}//localhost:${backendPort}`;

    axios.get(`${baseUrl}/questions`).then(res => setQuestions(res.data));
    axios.get(`${baseUrl}/categories`).then(res => setCategories(res.data));
  }, []);

  const filteredQuestions = selectedCategory ? questions.filter(q => q.category === selectedCategory) : questions;

  return (
    <div style={{ padding: '20px' }}>
      <h1>Question Tracker</h1>
      <ConceptCloud categories={categories} onSelectCategory={setSelectedCategory} />
      <QuestionList questions={filteredQuestions} />
    </div>
  );
}

export default App;