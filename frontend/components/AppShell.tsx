import Link from 'next/link';
import { ReactNode } from 'react';

import { NAV_ITEMS } from '@/lib/navigation';
import { UserMe } from '@/lib/types';

type Props = {
  pathname: string;
  user: UserMe;
  children: ReactNode;
};

export default function AppShell({ pathname, user, children }: Props) {
  return (
    <div className="layout">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <aside className="sidebar" aria-label="Primary">
        <div className="brand">NEUROQUANT</div>
        <nav>
          {NAV_ITEMS.map((item) => (
            <Link key={item.href} className={`nav-item ${pathname === item.href ? 'active' : ''}`} href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <div>
        <header className="header card">
          <div>
            <p className="subtle">Authenticated Session</p>
            <strong>{user.full_name}</strong>
          </div>
          <div className="subtle">{user.email}</div>
        </header>
        <main id="main-content" className="main">
          {children}
        </main>
      </div>
    </div>
  );
}
