import { cookies } from 'next/headers';

export const AUTH_COOKIE = 'auth_token';

export async function getServerToken(): Promise<string | undefined> {
  const cookieStore = await cookies();
  return cookieStore.get(AUTH_COOKIE)?.value;
}
