import { NextResponse } from "next/server";
import { getPythonApiUrl } from "@/app/api/_utils/python";

export async function proxyPostJson(req: Request, path: string) {
  const body = await req.json().catch(() => null);

  const pythonUrl = getPythonApiUrl();
  let upstream: Response;
  try {
    upstream = await fetch(`${pythonUrl}${path}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body ?? {}),
      cache: "no-store",
    });
  } catch (err) {
    console.error("Python API proxy error:", err);
    return NextResponse.json(
      {
        error: "Unable to reach Python API",
        python_api_url: pythonUrl,
      },
      { status: 502 }
    );
  }

  const contentType = upstream.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    const data = await upstream.json().catch(() => ({
      error: "Upstream returned invalid JSON",
    }));
    return NextResponse.json(data, { status: upstream.status });
  }

  const text = await upstream.text();
  return new NextResponse(text, {
    status: upstream.status,
    headers: { "content-type": contentType || "text/plain" },
  });
}
