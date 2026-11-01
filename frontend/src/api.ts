export function apiFetch(input: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers)
  const method = (init.method ?? "GET").toUpperCase()
  if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
    const cookie = document.cookie.split("; ").find(item => item.startsWith("mc_csrf="))
    if (cookie) headers.set("X-CSRF-Token", decodeURIComponent(cookie.slice("mc_csrf=".length)))
  }
  return fetch(input, { ...init, headers })
}
