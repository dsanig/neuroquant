import { redirect } from 'next/navigation';

import LoginForm from '@/components/LoginForm';
import { isDevAuthBypassEnabled } from '@/lib/auth';

export default function LoginPage() {
  if (isDevAuthBypassEnabled()) {
    redirect('/dashboard');
  }

  return (
    <div className="auth-layout">
      <LoginForm />
    </div>
  );
}
