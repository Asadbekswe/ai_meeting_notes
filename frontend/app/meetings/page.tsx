import Link from "next/link";

import { getMeetings } from "../../components/api";
import { Shell } from "../../components/Shell";

export default async function MeetingsPage() {
  const meetings = await getMeetings();

  return (
    <Shell>
      <section className="card p-6">
        <h2 className="font-display text-2xl">Meetings</h2>
        <p className="mt-1 text-sm text-black/70">Search and date filters are handled by API params in production mode.</p>
        <div className="mt-4 grid gap-3">
          {meetings.map((meeting: any) => (
            <Link key={meeting.id} href={`/meetings/${meeting.id}`} className="rounded-xl border border-black/10 bg-white p-4 hover:border-black/30">
              <div className="text-xs uppercase tracking-wider text-black/50">{new Date(meeting.created_at).toLocaleString()}</div>
              <div className="mt-2 font-medium">{meeting.title || "Untitled meeting"}</div>
              <div className="mt-1 line-clamp-2 text-sm text-black/70">{meeting.summary_text || "No summary yet"}</div>
            </Link>
          ))}
          {meetings.length === 0 ? <p className="text-black/60">No meetings found.</p> : null}
        </div>
      </section>
    </Shell>
  );
}
