import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

async function proxy(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params;
  const base = (process.env.BACKEND_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
  const incoming = new URL(request.url);
  const destination = `${base}/${path.map(encodeURIComponent).join("/")}${incoming.search}`;
  try {
    const headers = new Headers();
    const contentType = request.headers.get("content-type");
    if (contentType) headers.set("content-type", contentType);
    headers.set("accept", request.headers.get("accept") || "application/json");
    const body = request.method === "GET" || request.method === "HEAD" ? undefined : await request.arrayBuffer();
    const upstream = await fetch(destination, { method: request.method, headers, body, cache: "no-store" });
    const responseHeaders = new Headers();
    const upstreamType = upstream.headers.get("content-type");
    if (upstreamType) responseHeaders.set("content-type", upstreamType);
    return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers: responseHeaders });
  } catch {
    return NextResponse.json(
      { detail: "Could not reach the SkillForge API. Start FastAPI on port 8000 and check BACKEND_API_URL." },
      { status: 502 }
    );
  }
}

export const GET = proxy;
export const POST = proxy;