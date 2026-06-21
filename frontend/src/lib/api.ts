import type { AnalysisResponse, HistoryList } from "@/types/api"
import { supabase } from "@/lib/supabase"

const BASE = "/api"

async function authHeaders(): Promise<HeadersInit> {
  const { data } = await supabase.auth.getSession()
  const token = data.session?.access_token
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = res.statusText
    try {
      const data = await res.json()
      detail = data.detail || detail
    } catch {}
    throw new Error(detail)
  }
  return res.json() as Promise<T>
}

export async function analyze(
  cvFile: File,
  jobText: string,
  baslik: string
): Promise<AnalysisResponse> {
  const formData = new FormData()
  formData.append("cv_file", cvFile)
  formData.append("job_text", jobText)
  formData.append("baslik", baslik)

  const res = await fetch(`${BASE}/analyze`, {
    method: "POST",
    body: formData,
    headers: await authHeaders(),
  })
  return handle<AnalysisResponse>(res)
}

export async function fetchHistory(): Promise<HistoryList> {
  const res = await fetch(`${BASE}/history`, { headers: await authHeaders() })
  return handle<HistoryList>(res)
}

export async function fetchHistoryDetail(id: string): Promise<AnalysisResponse> {
  const res = await fetch(`${BASE}/history/${id}`, {
    headers: await authHeaders(),
  })
  return handle<AnalysisResponse>(res)
}

export async function deleteHistory(id: string): Promise<void> {
  const res = await fetch(`${BASE}/history/${id}`, {
    method: "DELETE",
    headers: await authHeaders(),
  })
  if (!res.ok) throw new Error("Silinemedi")
}
