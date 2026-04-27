import React from 'react';

export function TextEditor({ value, onChange, label, readOnly = false }: { value: string; onChange: (v: string) => void; label: string; readOnly?: boolean }) {
  const wc = value.trim() ? value.trim().split(/\s+/).length : 0;

  function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => onChange(String(reader.result || ''));
    reader.readAsText(file);
  }

  return (
    <section className="card">
      <h3>{label}</h3>
      <div className="row">
        <span>Words: {wc}</span>
        {!readOnly && <button onClick={() => onChange('')}>Clear</button>}
        {!readOnly && <input type="file" accept=".txt" onChange={onFile} />}
      </div>
      <textarea value={value} onChange={(e) => onChange(e.target.value)} readOnly={readOnly} rows={14} />
      {readOnly && (
        <div className="row">
          <button onClick={() => navigator.clipboard.writeText(value)}>Copy</button>
          <button onClick={() => {
            const blob = new Blob([value], { type: 'text/plain' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'humanized.txt';
            a.click();
          }}>Download</button>
        </div>
      )}
    </section>
  );
}
