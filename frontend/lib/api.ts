const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

const shouldSetJsonContentType = (body: BodyInit | null | undefined) => {
  if (!body) {
    return false;
  }
  if (typeof body === 'string') {
    return true;
  }
  if (typeof Blob !== 'undefined' && body instanceof Blob) {
    return false;
  }
  if (body instanceof ArrayBuffer || ArrayBuffer.isView(body)) {
    return false;
  }
  if (typeof FormData !== 'undefined' && body instanceof FormData) {
    return false;
  }
  if (typeof URLSearchParams !== 'undefined' && body instanceof URLSearchParams) {
    return false;
  }
  return true;
};

export const apiFetch = async <T = any>(path: string, init: RequestInit = {}): Promise<T> => {
  const headers = new Headers(init.headers ?? {});

  if (!headers.has('Content-Type') && shouldSetJsonContentType(init.body)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers
  });

  if (!response.ok) {
    const bodyText = await response.text();
    throw new Error(`API ${response.status} ${response.statusText}: ${bodyText}`);
  }

  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json() as Promise<T>;
  }

  return response.text() as unknown as Promise<T>;
};
