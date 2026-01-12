import { getPythonApiUrl } from "@/app/api/_utils/python";

export async function POST(req: Request) {
  const body = await req.json();
  const pythonUrl = getPythonApiUrl();

  try {
    const response = await fetch(`${pythonUrl}/chat/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.text();
      return new Response(
        JSON.stringify({ error: `Chat API error: ${error}` }),
        { status: response.status, headers: { "Content-Type": "application/json" } }
      );
    }

    // Check if streaming
    if (body.stream) {
      // Forward the SSE stream directly
      return new Response(response.body, {
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
        },
      });
    }

    // Non-streaming response
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error("Chat proxy error:", error);
    return Response.json(
      { error: "Failed to connect to chat service" },
      { status: 502 }
    );
  }
}

export async function GET() {
  const pythonUrl = getPythonApiUrl();

  try {
    const response = await fetch(`${pythonUrl}/chat/health`);
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    return Response.json(
      { status: "unhealthy", error: "Chat service unavailable" },
      { status: 503 }
    );
  }
}
