// frontend/app/page.tsx
'use client';
import { useEffect, useState } from 'react';
import { checkApiHealth } from '../lib/api';

export default function Home() {
  const [status, setStatus] = useState('Connecting...');

  useEffect(() => {
    checkApiHealth()
      .then((data) => setStatus(data.message))
      .catch(() => setStatus('API Disconnected'));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-slate-950 text-white">
      <h1 className="text-4xl font-bold mb-4">AeroTech Initialized</h1>
      <p className="text-xl text-cyan-400">Status: {status}</p>
    </main>
  );
}