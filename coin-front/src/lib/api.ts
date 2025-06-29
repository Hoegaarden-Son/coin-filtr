const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export const fetcher = async (path: string) => {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error('API 요청 실패');
  }
  return res.json();
};

export async function post(path: string, body: any) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res;
}