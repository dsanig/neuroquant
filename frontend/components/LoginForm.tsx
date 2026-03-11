'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

import { login } from '@/lib/api';

export default function LoginForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading) {
      return;
    }

    const formData = new FormData(event.currentTarget);
    const email = String(formData.get('email') ?? '').trim();
    const password = String(formData.get('password') ?? '');

    setError('');
    setLoading(true);

    try {
      await login(email, password);
      router.push('/dashboard');
      router.refresh();
    } catch (submitError) {
      setError('Authentication failed. Check credentials or contact operations support.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="card auth-card">
      <h1>NeuroQuant</h1>
      <p className="subtle">Internal authenticated access only.</p>
      <label>
        <span className="subtle">Email</span>
        <input id="email" name="email" type="email" autoComplete="email" required />
      </label>
      <label>
        <span className="subtle">Password</span>
        <input id="password" name="password" type="password" autoComplete="current-password" required />
      </label>
      {error ? <p className="state-error">{error}</p> : null}
      <button type="submit" disabled={loading}>{loading ? 'Signing in…' : 'Sign In'}</button>
    </form>
  );
}
