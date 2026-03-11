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
  const [debugState, setDebugState] = useState('idle');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    console.debug('[LoginForm] submit triggered');
    setDebugState('submit start');
    setError('');
    setLoading(true);

    try {
      console.debug('[LoginForm] calling login()');
      setDebugState('calling login()');
      await login(email, password);
      console.debug('[LoginForm] login success; navigating to /dashboard');
      setDebugState('login success');
      router.push('/dashboard');
      router.refresh();
    } catch (submitError) {
      console.error('[LoginForm] login failed', submitError);
      setDebugState('login catch');
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
      <h1>NeuroQuant</h1>
      <p className="subtle">Internal authenticated access only.</p>
      <label>
        <span className="subtle">Email</span>
        <input value={email} onChange={(e) => setEmail(e.target.value)} onKeyDown={onInputKeyDown} type="email" required />
      </label>
      <label>
        <span className="subtle">Password</span>
        <input value={password} onChange={(e) => setPassword(e.target.value)} onKeyDown={onInputKeyDown} type="password" required />
      </label>
      <p className="subtle" aria-live="polite">Debug: {debugState}</p>
      {error ? <p className="state-error">{error}</p> : null}
      <button type="submit" disabled={loading}>{loading ? 'Signing in…' : 'Sign In'}</button>
    </form>
  );
}
