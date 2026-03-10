'use client';

export default function ProtectedError({ error }: { error: Error }) {
  return (
    <div className="card state-error-block">
      <h2>Unable to load this module</h2>
      <p className="subtle">{error.message}</p>
      <p className="subtle">Try refreshing. If this persists, check backend availability and authorization scope.</p>
    </div>
  );
}
