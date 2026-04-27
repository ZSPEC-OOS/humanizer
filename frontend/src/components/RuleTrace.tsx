import React from 'react';

export function RuleTrace({ trace, diff }: { trace: string[]; diff: Array<{ line: string; state: string }> }) {
  return (
    <section className="card">
      <h3>Rule Trace & Diff</h3>
      <ul>{trace.map((t, i) => <li key={i}><code>{t}</code></li>)}</ul>
      <pre className="diff">
        {diff.map((d, i) => `${d.state === 'added' ? '+' : d.state === 'removed' ? '-' : ' '} ${d.line}`).join('\n')}
      </pre>
    </section>
  );
}
