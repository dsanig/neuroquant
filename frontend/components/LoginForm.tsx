'use client';

import { FormEvent, KeyboardEvent, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';

import { login } from '@/lib/api';

export default function LoginForm() {
  const router = useRouter();
  const formRef = useRef<HTMLFormElement>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    console.debug('[LoginForm] submit triggered');
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      router.push('/dashboard');
      router.refresh();
    } catch (submitError) {
      console.error('[LoginForm] login failed', submitError);
      setError('Authentication failed. Check credentials or contact operations support.');
    } finally {
      setLoading(false);
    }
  }

  function onInputKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter' && !loading) {
      formRef.current?.requestSubmit();
    }
  }

  return (
    <form ref={formRef} onSubmit={onSubmit} className="card auth-card">
      <h1>Investment Control Center</h1>
      <p className="subtle">Internal authenticated access only.</p>
      <label>
        <span className="subtle">Email</span>
        <input value={email} onChange={(e) => setEmail(e.target.value)} onKeyDown={onInputKeyDown} type="email" required />
      </label>
      <label>
        <span className="subtle">Password</span>
        <input value={password} onChange={(e) => setPassword(e.target.value)} onKeyDown={onInputKeyDown} type="password" required />
      </label>
      {error ? <p className="state-error">{error}</p> : null}
      <button type="button" disabled={loading} onClick={() => formRef.current?.requestSubmit()}>{loading ? 'Signing in…' : 'Sign In'}</button>
    </form>
  );
}
