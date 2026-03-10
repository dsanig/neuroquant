import Link from 'next/link';
import { ReactNode } from 'react';

const navItems = ['Dashboard', 'Positions', 'Trades', 'Strategies', 'Risk', 'Margin', 'Performance', 'Income', 'Reports', 'Settings', 'Audit Log'];

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">INVESTMENT CONTROL CENTER</div>
        {navItems.map((item) => (
          <Link key={item} className="nav-item" href="#">{item}</Link>
        ))}
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}
