function QuestionList({ questions }) {
  return (
    <ul>
      {questions.map((q, index) => (
        <li key={`${q.id}-${index}`}>
          <strong>{q.question}</strong> - {q.category} - {q.status}
          {q.notes && <p>{q.notes}</p>}
        </li>
      ))}
    </ul>
  );
}

export default QuestionList;