import { cookies } from 'next/headers';

export const AUTH_COOKIE = 'auth_token';

export function getServerToken(): string | undefined {
  return cookies().get(AUTH_COOKIE)?.value;
}
