'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    fetch('http://localhost:8000/')
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage('백엔드 연결 실패'));
  }, []);

  return (
    <main style={{ padding: '2rem', fontSize: '1.5rem' }}>
      <h1>{message}</h1>
    </main>
  );
}
