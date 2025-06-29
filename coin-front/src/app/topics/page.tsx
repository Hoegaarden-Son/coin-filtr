// src/app/topics/page.tsx
'use client';

import useSWR from 'swr';
import { fetcher } from '@/lib/api';
import Link from 'next/link';


// const fetcher = (url: string) => fetch(url).then(res => res.json());

type Topic = {
  id: number;
  name: string;
  slug: string;
  description?: string;
};

export default function TopicListPage() {
  const { data, error, isLoading } = useSWR<Topic[]>('/topics/', fetcher);

  if (isLoading) return <div>로딩 중...</div>;
  if (error) return <div>에러 발생!</div>;

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">🔥 토픽 리스트</h1>

      {data?.map((topic) => (
        <div key={topic.id} className="p-4 bg-white rounded shadow">
          {/* ✅ 요기요기! name을 <Link>로 감싸줘! */}
          <Link href={`/topics/${topic.slug}`}>
            <h2 className="text-lg font-semibold hover:underline">{topic.name}</h2>
          </Link>
          <p className="text-sm text-gray-600">{topic.description}</p>
        </div>
      ))}
    </div>
  );
}