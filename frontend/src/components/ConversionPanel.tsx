import React from 'react';

export function ConversionPanel({ mode, setMode, onConvert }: { mode: string; setMode: (m: string) => void; onConvert: () => void }) {
  return (
    <section className="card row">
      <label>Mode
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="rule">rule</option>
          <option value="ai">ai</option>
          <option value="hybrid">hybrid</option>
        </select>
      </label>
      <label>Audience <select><option>general</option><option>students</option><option>executives</option></select></label>
      <label>Tone <select><option>neutral</option><option>friendly</option><option>professional</option></select></label>
      <label>Strength <input type="range" min={0} max={1} step={0.05} defaultValue={0.6} /></label>
      <button onClick={onConvert}>Humanize</button>
    </section>
  );
}
