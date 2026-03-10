export type NavItem = {
  label: string;
  href: string;
};

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Positions', href: '/positions' },
  { label: 'Trades', href: '/trades' },
  { label: 'Strategies', href: '/strategies' },
  { label: 'Risk', href: '/risk' },
  { label: 'Margin', href: '/margin' },
  { label: 'Performance', href: '/performance' },
  { label: 'Income', href: '/income' },
  { label: 'Imports', href: '/imports' },
  { label: 'Reports', href: '/reports' },
  { label: 'Audit Log', href: '/audit-log' },
  { label: 'Settings', href: '/settings' },
];
