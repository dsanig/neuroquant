import { NextRequest, NextResponse } from 'next/server';

const backendBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://backend:8000/api/v1';

export async function POST(request: NextRequest) {
  const payload = await request.json();

  const response = await fetch(`${backendBaseUrl}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    cache: 'no-store',
  });

  if (!response.ok) {
    const text = await response.text();
    return NextResponse.json({ detail: text || 'Authentication failed' }, { status: response.status });
  }

  const token = await response.json();
  const result = NextResponse.json({ ok: true });
  result.cookies.set('auth_token', token.access_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60,
  });
  return result;
}
