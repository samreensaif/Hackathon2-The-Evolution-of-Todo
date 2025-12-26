'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';
import { fetchApi } from '@/lib/api';
import {
  Plus,
  Trash2,
  CheckCircle,
  Circle,
  LogOut,
  Loader2,
  Search,
} from 'lucide-react';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
}

export default function TasksPage() {
  const { user, logout, isLoading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');

  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    try {
      let query = `?q=${encodeURIComponent(search)}`;
      if (filter === 'completed') query += '&completed=true';
      if (filter === 'pending') query += '&completed=false';

      const response = await fetchApi(`/tasks${query}`);
      if (response.ok) {
        const data = await response.json();
        setTasks(data.items);
        setTotal(data.total);
      }
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    } finally {
      setIsLoading(false);
    }
  }, [search, filter]);

  useEffect(() => {
    if (!authLoading && !user) return;
    fetchTasks();
  }, [authLoading, user, fetchTasks]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const response = await fetchApi('/tasks', {
        method: 'POST',
        body: JSON.stringify({ title: newTaskTitle }),
      });

      if (response.ok) {
        setNewTaskTitle('');
        fetchTasks();
      }
    } catch (err) {
      console.error('Failed to create task', err);
    }
  };

  const handleToggleTask = async (task: Task) => {
    try {
      const response = await fetchApi(`/tasks/${task.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ completed: !task.completed }),
      });

      if (response.ok) {
        fetchTasks();
      }
    } catch (err) {
      console.error('Failed to update task', err);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
      const response = await fetchApi(`/tasks/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        fetchTasks();
      }
    } catch (err) {
      console.error('Failed to delete task', err);
    }
  };

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="animate-spin text-indigo-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 pb-12">
      {/* Navbar */}
      <nav className="bg-blue-300 shadow-sm">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          
          <div className="flex h-16 items-center justify-between">
            
            <h1 className="text-xl font-bold text-gray-900">
              My Tasks ({total})
            </h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">{user?.email}</span>
              <button
                onClick={logout}
                className="p-2 text-gray-400 hover:text-gray-600"
              >
                <LogOut size={20} />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main */}
      <main className="mx-auto  max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Create Task */}
        <form onSubmit={handleCreateTask} className="mb-8 flex gap-2">
          <input
            type="text"
            placeholder="Add a new task..."
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            className="w-full rounded-md border-0 py-2 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600"
          />
          <button
            type="submit"
            className="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
          >
            <Plus size={18} />
            Add
          </button>
        </form>

        {/* Filters */}
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative w-full sm:w-64">
            <Search
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              placeholder="Search tasks..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded-md border-0 py-2 pl-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"
            />
          </div>

          <div className="flex gap-2">
            {(['all', 'pending', 'completed'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`rounded-full px-3 py-1 text-sm capitalize ${
                  filter === f
                    ? 'bg-indigo-100 font-medium text-indigo-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {/* Tasks */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="animate-spin text-indigo-600" />
          </div>
        ) : tasks.length === 0 ? (
          <p className="py-12 text-center text-gray-500">
            No tasks found. Start by adding one ✨
          </p>
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="group flex items-center justify-between rounded-lg border border-gray-100 bg-white p-4 shadow-sm"
              >
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleToggleTask(task)}
                    className={
                      task.completed
                        ? 'text-green-500'
                        : 'text-gray-300 hover:text-gray-400'
                    }
                  >
                    {task.completed ? (
                      <CheckCircle size={22} />
                    ) : (
                      <Circle size={22} />
                    )}
                  </button>
                  <span
                    className={`text-gray-900 ${
                      task.completed ? 'line-through text-gray-400' : ''
                    }`}
                  >
                    {task.title}
                  </span>
                </div>

                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="opacity-0 transition-opacity group-hover:opacity-100 text-gray-300 hover:text-red-500"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
