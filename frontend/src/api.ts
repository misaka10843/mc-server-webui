export function apiFetch(input: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers)
  const method = (init.method ?? "GET").toUpperCase()
  if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
    const cookie = document.cookie.split("; ").find(item => item.startsWith("mc_csrf="))
    if (cookie) headers.set("X-CSRF-Token", decodeURIComponent(cookie.slice("mc_csrf=".length)))
  }
  return fetch(input, { ...init, headers })
}

export async function apiRequest<T = unknown>(input: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
  const response = await apiFetch(input, { ...init, headers })
  const value = await response.json()
  if (!response.ok) throw new Error(typeof value.detail === 'string' ? value.detail : '请检查填写的内容后重试')
  return value as T
}
