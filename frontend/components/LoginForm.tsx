'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

import { login } from '@/lib/api';

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const token = await login(email, password);
      document.cookie = `auth_token=${token.access_token}; path=/; SameSite=Lax`;
      router.push('/dashboard');
      router.refresh();
    } catch {
      setError('Authentication failed. Check credentials or contact operations support.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="card auth-card">
      <h1>Investment Control Center</h1>
      <p className="subtle">Internal authenticated access only.</p>
      <label>
        <span className="subtle">Email</span>
        <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
      </label>
      <label>
        <span className="subtle">Password</span>
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
      </label>
      {error ? <p className="state-error">{error}</p> : null}
      <button type="submit" disabled={loading}>{loading ? 'Signing in…' : 'Sign In'}</button>
    </form>
  );
}
