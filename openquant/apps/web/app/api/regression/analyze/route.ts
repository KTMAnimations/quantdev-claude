import { proxyPostJson } from "@/app/api/_utils/proxy";

export async function POST(req: Request) {
  return proxyPostJson(req, "/regression/analyze");
}

