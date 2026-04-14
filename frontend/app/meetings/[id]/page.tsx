import { getMeetingDetail } from "../../../components/api";
import { Shell } from "../../../components/Shell";

export default async function MeetingDetailPage({ params }: { params: { id: string } }) {
  const meeting = await getMeetingDetail(params.id);

  if (!meeting) {
    return (
      <Shell>
        <section className="card p-6">Meeting not found.</section>
      </Shell>
    );
  }

  return (
    <Shell>
      <section className="card p-6">
        <h2 className="font-display text-2xl">{meeting.title || "Meeting detail"}</h2>
        <p className="mt-1 text-sm uppercase tracking-wider text-black/50">Status: {meeting.status}</p>

        <div className="mt-6 grid gap-6">
          <article>
            <h3 className="font-display text-lg">Summary</h3>
            <p className="mt-2 text-black/80">{meeting.summary_text || "No summary generated yet."}</p>
          </article>

          <article>
            <h3 className="font-display text-lg">Decisions</h3>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-black/80">
              {meeting.decisions?.map((d: any, idx: number) => <li key={idx}>{d.text}</li>)}
            </ul>
          </article>

          <article>
            <h3 className="font-display text-lg">Action Items</h3>
            <ul className="mt-2 space-y-1 text-black/80">
              {meeting.action_items?.map((a: any, idx: number) => (
                <li key={idx}>• {a.task_text} - {a.owner_name_raw || "Unassigned"} ({a.status})</li>
              ))}
            </ul>
          </article>

          <article>
            <h3 className="font-display text-lg">Topics</h3>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-black/80">
              {meeting.topics?.map((t: any, idx: number) => <li key={idx}>{t.name}</li>)}
            </ul>
          </article>

          <details>
            <summary className="cursor-pointer font-display text-lg">Transcript</summary>
            <p className="mt-3 whitespace-pre-wrap text-sm text-black/70">{meeting.transcript || "No transcript available."}</p>
          </details>
        </div>
      </section>
    </Shell>
  );
}
