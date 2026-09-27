import type { DataStatus } from "@/lib/types";

export function DataBadge({ status }: { status: DataStatus }) {
  return <span className={`badge badge-${status.toLowerCase().replaceAll(" ", "-")}`}>{status}</span>;
}
