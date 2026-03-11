import { cookies } from 'next/headers';

export const AUTH_COOKIE = 'auth_token';

export function isDevAuthBypassEnabled(): boolean {
  return process.env.DEV_AUTH_BYPASS === 'true';
}

export async function getServerToken(): Promise<string | undefined> {
  if (isDevAuthBypassEnabled()) {
    return 'dev-auth-bypass';
  }

  const cookieStore = await cookies();
  return cookieStore.get(AUTH_COOKIE)?.value;
}
