import { getActionItems } from "../../components/api";
import { Shell } from "../../components/Shell";

function groupByOwner(items: any[]) {
  return items.reduce((acc: Record<string, any[]>, item) => {
    const key = item.owner_name_raw || "Unassigned";
    if (!acc[key]) acc[key] = [];
    acc[key].push(item);
    return acc;
  }, {});
}

export default async function ActionItemsPage() {
  const items = await getActionItems();
  const grouped = groupByOwner(items);

  return (
    <Shell>
      <section className="card p-6">
        <h2 className="font-display text-2xl">Action Items</h2>
        <p className="mt-1 text-sm text-black/70">Grouped by person. Statuses: pending, in progress, done.</p>
        <div className="mt-6 grid gap-4">
          {Object.entries(grouped).map(([owner, ownerItems]) => (
            <div key={owner} className="rounded-xl border border-black/10 bg-white p-4">
              <h3 className="font-display text-lg">{owner}</h3>
              <ul className="mt-2 space-y-2">
                {(ownerItems as any[]).map((item) => (
                  <li key={item.id} className="text-sm">
                    <span className="font-medium">{item.task_text}</span>
                    <span className="ml-2 rounded bg-black/5 px-2 py-0.5 text-xs uppercase">{item.status}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
          {items.length === 0 ? <p className="text-black/60">No action items yet.</p> : null}
        </div>
      </section>
    </Shell>
  );
}
