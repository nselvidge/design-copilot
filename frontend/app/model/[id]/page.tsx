"use client";
import { useQuery } from "react-query";
import { InferType, boolean, object, string } from "yup";

const modelValidator = object({
  id: string().required(),
  isProcessing: boolean().required(),
  plantUml: string(),
  imageUrl: string(),
});

export default function Model({ id }: { id: string }) {
  const { data, isLoading, error } = useQuery("model", async () => {
    const response = await fetch(`https://localhost:3001/model/${id}`);
    const data = await response.json();

    if (!modelValidator.isValidSync(data)) {
      throw new Error("Invalid data");
    }

    return data;
  });

  return (
    <main className="-mt-24 pb-8 grow">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
        <h1 className="sr-only">Design Copilot</h1>
        {/* Main 3 column grid */}
        <div className="grid grid-cols-1 items-start gap-4 lg:grid-cols-3 lg:gap-8">
          {/* Left column */}
          <div className="grid grid-cols-1 gap-4">
            <section aria-labelledby="section-1-title">
              <h2 className="sr-only" id="section-1-title">
                Chat Interface goes here
              </h2>
              <div className="overflow-hidden rounded-lg bg-white shadow">
                <div className="p-6"></div>
              </div>
            </section>
          </div>

          {/* Right column */}
          <div className="grid grid-cols-1 gap-4  lg:col-span-2">
            <section aria-labelledby="section-2-title">
              <h2 className="sr-only" id="section-2-title">
                Design Diagram
              </h2>
              <div className="overflow-hidden rounded-lg bg-white shadow">
                <div className="p-6">
                  <img src={data?.imageUrl} />
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
