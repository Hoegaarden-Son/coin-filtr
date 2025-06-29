// src/app/topics/[slug]/page.tsx
import { fetcher } from '@/lib/api';

type Topic = {
  id: number;
  name: string;
  slug: string;
  description?: string;
};

type Props = {
  params: { slug: string };
};

export default async function TopicDetailPage({ params }: Props) {
//   const topic: Topic = await fetcher(`/topics/slug/${params.slug}`);
    const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;
    // const topic: Topic = await fetch(`${API_BASE}/topics/slug/${params.slug}`).then(res => res.json());
    // console.log('API_BASE →', API_BASE);

    console.log('🔥 slug:', params.slug);  // params가 잘 들어오는지
    console.log('🔥 요청 주소:', `${API_BASE}/topics/slug/${params.slug}`);

    const res = await fetch(`${API_BASE}/topics/slug/${params.slug}`);
    console.log('status:', res.status);
    const topic: Topic = await res.json();
    
  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">{topic.name}</h1>
      <p className="text-gray-600">{topic.description}</p>
      <p className="text-sm text-gray-400">slug: {topic.slug}</p>
    </div>
  );
}
