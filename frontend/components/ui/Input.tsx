import { HTMLInputTypeAttribute } from "react";

export default function Input({
  name,
  type,
  label,
  placeholder,
  value,
  onChange,
}: {
  name: string;
  type: HTMLInputTypeAttribute;
  label: string;
  placeholder: string;
  value: string;
  onChange: (e: any) => void;
}) {
  return (
    <div>
      <label
        htmlFor="email"
        className="block text-sm font-medium leading-6 text-gray-900"
      >
        {label}
      </label>
      <div className="mt-2">
        <input
          onChange={onChange}
          value={value}
          type={type}
          name={name}
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          placeholder={placeholder}
        />
      </div>
    </div>
  );
}
