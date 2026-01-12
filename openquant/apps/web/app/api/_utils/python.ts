export function getPythonApiUrl(): string {
  return (
    process.env.PYTHON_API_URL ||
    process.env.NEXT_PUBLIC_PYTHON_API_URL ||
    "http://localhost:8000"
  );
}

