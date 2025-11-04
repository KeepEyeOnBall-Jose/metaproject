import { render, screen } from '@testing-library/react';
import QuestionList from './QuestionList';

test('renders questions list', () => {
  const questions = [
    { id: '1', question: 'Test question', category: 'test', status: 'open', notes: 'test note' }
  ];
  render(<QuestionList questions={questions} />);
  expect(screen.getByText('Test question')).toBeInTheDocument();
});