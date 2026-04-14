import Link from "next/link";
import { ReactNode } from "react";

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto max-w-6xl px-4 py-8 md:px-8">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <h1 className="font-display text-3xl">AI Meeting Notes</h1>
        <nav className="flex gap-2 text-sm">
          <Link className="rounded-full border border-black/20 px-4 py-2 hover:bg-black hover:text-white" href="/">Home</Link>
          <Link className="rounded-full border border-black/20 px-4 py-2 hover:bg-black hover:text-white" href="/meetings">Meetings</Link>
          <Link className="rounded-full border border-black/20 px-4 py-2 hover:bg-black hover:text-white" href="/action-items">Action Items</Link>
        </nav>
      </header>
      {children}
    </div>
  );
}
