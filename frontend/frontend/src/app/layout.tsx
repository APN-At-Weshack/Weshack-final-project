import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SpeakEasy",
  description: "Learn A New Language",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
