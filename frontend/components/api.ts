const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export async function getMeetings() {
  const res = await fetch(`${API_BASE}/meetings`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function getMeeting(id: string) {
  const res = await fetch(`${API_BASE}/meetings/${id}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export async function getMeetingDetail(id: string) {
  const res = await fetch(`${API_BASE}/meetings/${id}/detail`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export async function getActionItems() {
  const res = await fetch(`${API_BASE}/action-items`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function getHomeStats() {
  const res = await fetch(`${API_BASE}/stats/home`, { cache: "no-store" });
  if (!res.ok) {
    return {
      total_meetings_this_week: 0,
      pending_tasks: 0,
    };
  }
  return res.json();
}
