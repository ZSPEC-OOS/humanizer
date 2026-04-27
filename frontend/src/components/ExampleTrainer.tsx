import React, { useState } from 'react';

export function ExampleTrainer() {
  const [aiText, setAi] = useState('');
  const [humanText, setHuman] = useState('');
  const [result, setResult] = useState<any>(null);

  async function analyze() {
    const res = await fetch('/api/analyze-pair', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ai_text: aiText, human_text: humanText }),
    });
    setResult(await res.json());
  }

  return (
    <section className="card">
      <h3>Train Framework</h3>
      <div className="grid">
        <textarea placeholder="Paste 1: AI text" value={aiText} onChange={(e) => setAi(e.target.value)} rows={10} />
        <textarea placeholder="Paste 2: Humanized text" value={humanText} onChange={(e) => setHuman(e.target.value)} rows={10} />
      </div>
      <button onClick={analyze}>Analyze Pair</button>
      <pre>{result ? JSON.stringify(result, null, 2) : ''}</pre>
    </section>
  );
}
