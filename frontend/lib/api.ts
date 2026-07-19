// frontend/lib/api.ts
const API_BASE_URL = 'http://localhost:8000';

export async function checkApiHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('API is unreachable');
  }
  return response.json();
}