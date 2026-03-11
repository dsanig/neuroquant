import { NextRequest, NextResponse } from 'next/server';

const PUBLIC_PATHS = ['/login'];

function isDevAuthBypassEnabled(): boolean {
  return process.env.DEV_AUTH_BYPASS === 'true';
}

export function proxy(request: NextRequest) {
  const devAuthBypass = isDevAuthBypassEnabled();
  const token = request.cookies.get('auth_token')?.value;
  const { pathname } = request.nextUrl;

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-pathname', pathname);

  if (!devAuthBypass && !token && !PUBLIC_PATHS.includes(pathname)) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if ((devAuthBypass || token) && pathname === '/login') {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next({ request: { headers: requestHeaders } });
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|api).*)'],
};
