import { render, screen } from '@testing-library/react';
import App from './App';
import Register from './Register';
import Login from './Login';

test('renders learn react link', () => {
  render(<App />);
  render(<Register />);
  render(<Login />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
