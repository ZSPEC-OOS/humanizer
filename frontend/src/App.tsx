import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles/globals.css';
import { TextEditor } from './components/TextEditor';
import { ConversionPanel } from './components/ConversionPanel';
import { ScoreCard } from './components/ScoreCard';
import { RuleTrace } from './components/RuleTrace';
import { SettingsPanel } from './components/SettingsPanel';
import { ExampleTrainer } from './components/ExampleTrainer';

function App() {
  const [tab, setTab] = useState<'convert' | 'train' | 'rules' | 'settings'>('convert');
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [trace, setTrace] = useState<string[]>([]);
  const [scores, setScores] = useState<any>(null);
  const [mode, setMode] = useState('hybrid');

  const diff = useMemo(() => {
    const a = input.split('\n');
    const b = output.split('\n');
    return [...new Set([...a, ...b])].map((line) => ({ line, state: a.includes(line) ? (b.includes(line) ? 'same' : 'removed') : 'added' }));
  }, [input, output]);

  async function runConvert() {
    const res = await fetch('/api/humanize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input, mode }),
    });
    const data = await res.json();
    setOutput(data.rewritten_text || '');
    setTrace(data.change_log || []);
    setScores({ before: data.score_before, after: data.score_after });
  }

  return (
    <div className="app">
      <header><h1>Humanizer Lab</h1></header>
      <nav className="tabs">
        {['convert', 'train', 'rules', 'settings'].map((t) => (
          <button key={t} className={tab === t ? 'active' : ''} onClick={() => setTab(t as any)}>{t}</button>
        ))}
      </nav>

      {tab === 'convert' && (
        <>
          <ConversionPanel mode={mode} setMode={setMode} onConvert={runConvert} />
          <div className="grid">
            <TextEditor value={input} onChange={setInput} label="AI Input" />
            <TextEditor value={output} onChange={setOutput} label="Humanized Output" readOnly />
          </div>
          <ScoreCard scores={scores} />
          <RuleTrace trace={trace} diff={diff} />
        </>
      )}
      {tab === 'train' && <ExampleTrainer />}
      {tab === 'rules' && <RuleTrace trace={trace} diff={diff} />}
      {tab === 'settings' && <SettingsPanel />}
    </div>
  );
}

const rootEl = document.getElementById('root');
if (rootEl) createRoot(rootEl).render(<App />);

export default App;
