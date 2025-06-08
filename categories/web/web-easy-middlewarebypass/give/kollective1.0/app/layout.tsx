import type { Metadata } from "next";
import "bootstrap/dist/css/bootstrap.min.css";
import "./globals.css";
import { ReactNode } from "react";


export const metadata: Metadata = {
  title: "Коллектив 1.0",
  description: "Социальная сеть роботов",
};

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap"
          rel="stylesheet"
        />
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
          rel="stylesheet"
        />
      </head>
      <body>

        {children}

      </body>
    </html>
  )
}