import React, { useEffect, useState } from 'react';

export function SettingsPanel() {
  const [cfg, setCfg] = useState<any>({});
  const [msg, setMsg] = useState('');

  useEffect(() => {
    fetch('/api/config').then((r) => r.json()).then(setCfg).catch(() => setMsg('Failed to load config'));
  }, []);

  async function save() {
    const res = await fetch('/api/config', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cfg) });
    setMsg(res.ok ? 'Saved' : 'Save failed');
  }

  async function testConnection() {
    const res = await fetch('/api/test-model', { method: 'POST' });
    const data = await res.json();
    setMsg(data.status === 'ok' ? 'Model connection works' : 'Connection failed');
  }

  return (
    <section className="card">
      <h3>AI Settings</h3>
      {['base_url', 'model_id', 'api_key', 'temperature', 'max_tokens', 'timeout', 'provider'].map((k) => (
        <label key={k}>{k}<input value={cfg[k] ?? ''} onChange={(e) => setCfg({ ...cfg, [k]: e.target.value })} /></label>
      ))}
      <div className="row"><button onClick={save}>Save</button><button onClick={testConnection}>Test Connection</button></div>
      <p>{msg}</p>
    </section>
  );
}
