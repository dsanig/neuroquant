import { ReactNode } from 'react';
import { redirect } from 'next/navigation';
import { headers } from 'next/headers';

import AppShell from '@/components/AppShell';
import { api, ApiError } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function ProtectedLayout({ children }: { children: ReactNode }) {
  const token = getServerToken();
  if (!token) redirect('/login');

  try {
    const user = await api.me(token);
    const pathname = headers().get('x-pathname') || '/dashboard';
    return <AppShell pathname={pathname} user={user}>{children}</AppShell>;
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      redirect('/login');
    }
    throw error;
  }
}
