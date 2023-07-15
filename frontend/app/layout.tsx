'use client'
import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Menu } from "../components/Menu";
import Head from "next/head";
import { QueryClient, QueryClientProvider } from "react-query";

const inter = Inter({ subsets: ["latin"] });

// export const metadata: Metadata = {
//   title: "Code Design Copilot",
//   description: "Your design helper",
// };

const queryClient = new QueryClient();

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" style={{ height: "100%" }}>
      <Head>
        <link rel="stylesheet" href="https://rsms.me/inter/inter.css"></link>
      </Head>
      <body className="min-h-full h-full bg-gray-100">
        <QueryClientProvider client={queryClient}>
          <div className=" min-h-full h-full flex flex-col">
            <Menu />
            {children}
            <footer>
              <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
                <div className="border-t border-gray-200 py-8 text-center text-sm text-gray-500 sm:text-left"></div>
              </div>
            </footer>
          </div>
        </QueryClientProvider>
      </body>
    </html>
  );
}
