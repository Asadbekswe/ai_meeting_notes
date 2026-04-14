import "./globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "AI Meeting Notes",
  description: "Meeting insights and action tracking",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
