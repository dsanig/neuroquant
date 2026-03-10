import { api } from '@/lib/api';
import { getServerToken } from '@/lib/auth';

export default async function SettingsPage() {
  const token = await getServerToken();
  const user = await api.me(token);

  return (
    <>
      <h1>Settings</h1>
      <section className="card section">
        <h2>User / Account</h2>
        <p><strong>Name:</strong> {user.full_name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Roles:</strong> {user.roles.join(', ')}</p>
      </section>
      <section className="card section">
        <h2>System</h2>
        <p className="subtle">Role-based system settings panels can be attached here as backend permissions expand.</p>
      </section>
    </>
  );
}
