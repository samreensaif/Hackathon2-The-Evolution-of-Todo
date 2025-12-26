'use client';

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Loader2 } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user) {
      router.push('/tasks');
    }
  }, [user, isLoading, router]);

  if (isLoading || user) {
    return <div className="flex min-h-screen items-center justify-center"><Loader2 className="animate-spin text-indigo-600" /></div>;
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4 text-center">
      <h1 className="mb-6 text-5xl font-extrabold tracking-tight text-gray-900">
        Simple <span className="text-indigo-600">Todo</span> App
      </h1>
      <p className="mb-10 max-w-md text-lg text-gray-600">
        Organize your work and life, finally. Phase II of the Hackathon Todo project.
      </p>
      <div className="flex gap-4">
        <Link
          href="/login"
          className="rounded-md bg-indigo-600 px-6 py-3 text-lg font-semibold text-white shadow-sm hover:bg-indigo-500"
        >
          Get Started
        </Link>
        <Link
          href="/register"
          className="rounded-md bg-white px-6 py-3 text-lg font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
        >
          Register
        </Link>
      </div>
    </div>
  );
}
