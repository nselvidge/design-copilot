"use client";
import Image from "next/image";
import Input from "../components/ui/Input";
import { useEffect, useState } from "react";
import { useMutation, useQuery } from "react-query";
import { useRouter } from "next/navigation";

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const router = useRouter();
  const {
    mutate,
    data,
    error: requestError,
    isLoading,
  } = useMutation("createModel", async (url: string) => {
    console.log(url);
    console.log(repoUrl);
    const response = await fetch(`http://127.0.0.1:5001/v1/generate_schema`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        repo_url: url,
        branch_name: "main",
      }),
    });

    return response.json();
  });

  useEffect(() => {
    if (data && data.id) {
      router.push(`/model/${data.id}`);
    }
  }, [data]);

  return (
    <main className="-mt-24 pb-8 grow">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
        <h1 className="sr-only">Design Copilot</h1>
        {/* Main 3 column grid */}
        <div className="grid grid-cols-1 items-start gap-4 lg:grid-cols-4 lg:gap-8">
          <div className="grid col-start-2 grid-cols-1 gap-4 col-span-2">
            <section aria-labelledby="section-1-title">
              <h2 className="sr-only" id="section-1-title">
                Enter a github Repo
              </h2>
              <div className="overflow-hidden rounded-lg bg-white shadow">
                <div className="p-6">
                  <Input
                    name="repo"
                    type="text"
                    label="Enter a github repo"
                    placeholder="https://github.com/nselvidge/design-copilot"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={() => mutate(repoUrl)}
                    className="mt-2 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    Submit
                  </button>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
