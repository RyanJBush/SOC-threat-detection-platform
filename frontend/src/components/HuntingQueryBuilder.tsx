import { useState } from 'react'
import { api } from '../services/api'

const defaultRule = `{
  "title": "Failed login from suspicious IP",
  "logsource": {"product": "auth"},
  "detection": {
    "selection": {"event_type": "login_failed", "source_ip": "203.0.113.9"}
  },
  "condition": "selection"
}`

export default function HuntingQueryBuilder() {
  const [rule, setRule] = useState(defaultRule)
  const [results, setResults] = useState([])
  const [error, setError] = useState('')

  async function runQuery() {
    setError('')
    try {
      const payload = JSON.parse(rule)
      const response = await api.runHuntingQuery(payload)
      setResults(response.items ?? [])
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="space-y-4">
      <textarea className="h-60 w-full rounded border border-slate-700 bg-slate-900 p-3" value={rule} onChange={(e) => setRule(e.target.value)} />
      <button onClick={runQuery} className="rounded bg-cyan-600 px-4 py-2">Run Hunt</button>
      {error && <p className="text-rose-400">{error}</p>}
      <table className="w-full text-left text-sm">
        <thead><tr><th>ID</th><th>Type</th><th>User</th><th>IP</th><th>Message</th></tr></thead>
        <tbody>
          {results.map((r) => <tr key={r.id}><td>{r.id}</td><td>{r.event_type}</td><td>{r.username}</td><td>{r.source_ip}</td><td>{r.message}</td></tr>)}
        </tbody>
      </table>
    </div>
  )
}
