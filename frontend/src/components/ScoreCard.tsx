import React from 'react';

export function ScoreCard({ scores }: { scores: any }) {
  if (!scores) return null;
  return (
    <section className="card">
      <h3>Scoring Dashboard</h3>
      <div className="grid3">
        <div>AI-likeness: {scores.after.ai_likeness} (before {scores.before.ai_likeness})</div>
        <div>Readability: {scores.after.readability}</div>
        <div>Humanization Strength: {scores.after.humanization_strength}</div>
      </div>
    </section>
  );
}
