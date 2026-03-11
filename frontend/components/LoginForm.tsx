'use client';

import { KeyboardEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

import { login } from '@/lib/api';

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleLogin() {
    if (loading) {
      return;
    }

    setError('');
    setLoading(true);

    try {
      await login(email.trim(), password);
      router.push('/dashboard');
      router.refresh();
    } catch {
      setError('Authentication failed. Check credentials or contact operations support.');
    } finally {
      setLoading(false);
    }
  }

  function onEnterPress(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key !== 'Enter') {
      return;
    }

    event.preventDefault();
    void handleLogin();
  }

  return (
    <div className="card auth-card" role="form" aria-busy={loading}>
      <h1>NeuroQuant</h1>
      <p className="subtle">Internal authenticated access only.</p>
      <label htmlFor="email">
        <span className="subtle">Email</span>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          onKeyDown={onEnterPress}
          required
        />
      </label>
      <label htmlFor="password">
        <span className="subtle">Password</span>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          onKeyDown={onEnterPress}
          required
        />
      </label>
      {error ? <p className="state-error">{error}</p> : null}
      <button
        type="button"
        onClick={() => void handleLogin()}
        aria-disabled={loading}
      >
        {loading ? 'Signing in…' : 'Sign In'}
      </button>
    </div>
  );
}
