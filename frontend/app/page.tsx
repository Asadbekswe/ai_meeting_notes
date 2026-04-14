import Link from "next/link";

import { getActionItems, getHomeStats, getMeetings } from "../components/api";
import { Shell } from "../components/Shell";

export default async function HomePage() {
  const [meetings, tasks, stats] = await Promise.all([getMeetings(), getActionItems(), getHomeStats()]);

  return (
    <Shell>
      <section className="mb-6 card p-6">
        <p className="mb-2 text-sm uppercase tracking-wider text-black/60">Start Here</p>
        <h2 className="font-display text-2xl">Send your first meeting recording via Telegram</h2>
        <p className="mt-2 max-w-3xl text-black/70">
          Upload voice or audio in Telegram. The bot transcribes, extracts decisions and tasks, then syncs here in near real-time.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="card p-5">
          <h3 className="font-display text-xl">Recent meetings</h3>
          <p className="mt-2 text-sm text-black/70">This week: {stats.total_meetings_this_week}</p>
          {meetings.length === 0 ? <p className="mt-4 text-black/60">No meetings yet.</p> : null}
          <div className="mt-4">
            <Link className="text-accent underline" href="/meetings">Open meetings list</Link>
          </div>
        </div>

        <div className="card p-5">
          <h3 className="font-display text-xl">Open action items</h3>
          <p className="mt-2 text-sm text-black/70">Pending tasks: {stats.pending_tasks}</p>
          {tasks.length === 0 ? <p className="mt-4 text-black/60">No tasks yet.</p> : null}
          <div className="mt-4">
            <Link className="text-accent underline" href="/action-items">Open task board</Link>
          </div>
        </div>
      </section>
    </Shell>
  );
}
