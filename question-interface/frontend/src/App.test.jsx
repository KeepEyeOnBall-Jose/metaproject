import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import App from './App';

// Mock axios
jest.mock('axios');
const mockedAxios = axios;

// Mock the ConceptCloud component to avoid Three.js issues in tests
jest.mock('./ConceptCloud', () => {
  return function MockConceptCloud({ categories, onSelectCategory }) {
    return (
      <div data-testid="concept-cloud">
        <button onClick={() => onSelectCategory('test-category')}>
          Select Test Category
        </button>
        <div>Categories: {Object.keys(categories || {}).join(', ')}</div>
      </div>
    );
  };
});

describe('App', () => {
  const mockQuestions = [
    {
      id: '1',
      question: 'How do I take a lovable/bolt.new prototype and make it go online?',
      category: 'todo',
      created_at: '2025-08-23T11:30:45.151304Z',
      status: 'open',
      notes: 'answer:answers/1755941445151.md'
    },
    {
      id: '2',
      question: 'Another test question',
      category: 'done',
      created_at: '2025-08-24T10:00:00.000000Z',
      status: 'closed',
      notes: 'completed'
    }
  ];

  const mockCategories = {
    'todo': 1,
    'done': 1
  };

  beforeEach(() => {
    // Reset mocks
    mockedAxios.get.mockClear();

    // Mock the API calls
    mockedAxios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/questions') {
        return Promise.resolve({ data: mockQuestions });
      } else if (url === 'http://localhost:8000/categories') {
        return Promise.resolve({ data: mockCategories });
      }
      return Promise.reject(new Error('Unknown URL'));
    });
  });

  test('renders the app title', () => {
    render(<App />);
    expect(screen.getByText('Question Tracker')).toBeInTheDocument();
  });

  test('loads and displays questions from API', async () => {
    render(<App />);

    // Wait for the questions to be loaded and displayed
    await waitFor(() => {
      expect(screen.getByText('How do I take a lovable/bolt.new prototype and make it go online?')).toBeInTheDocument();
    });

    expect(screen.getByText('Another test question')).toBeInTheDocument();
  });

  test('loads categories from API', async () => {
    render(<App />);

    // Wait for categories to be loaded (they're passed to ConceptCloud)
    await waitFor(() => {
      expect(mockedAxios.get).toHaveBeenCalledWith('http://localhost:8000/categories');
    });

    expect(mockedAxios.get).toHaveBeenCalledWith('http://localhost:8000/questions');
  });

  test('makes correct API calls on mount', async () => {
    render(<App />);

    await waitFor(() => {
      expect(mockedAxios.get).toHaveBeenCalledTimes(2);
    });

    expect(mockedAxios.get).toHaveBeenCalledWith('http://localhost:8000/questions');
    expect(mockedAxios.get).toHaveBeenCalledWith('http://localhost:8000/categories');
  });
});