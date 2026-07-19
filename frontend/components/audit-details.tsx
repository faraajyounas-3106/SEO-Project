'use client';

import React, { useState } from 'react';
import { GlassCard } from './ui/glass-card';
import { useAudit } from '../hooks/use-audit';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { RefreshCw, Check, X, ShieldAlert, Cpu, Award } from 'lucide-react';

interface AuditDetailsProps {
  projectId: string;
}

export function AuditDetails({ projectId }: AuditDetailsProps) {
  const [activeTaskId, setActiveTaskId] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  // Custom polling hook for background celery task
  const { status, progress, error: pollingError } = useAudit(activeTaskId, () => {
    // Audit completed callback
    setSuccessMessage('Audit complete! Real-time metrics refreshed.');
    setActiveTaskId(null);
    setTimeout(() => setSuccessMessage(null), 5000);
  });

  // Mock historical performance data for the Recharts graph
  const historyData = [
    { name: 'June 01', Score: 62 },
    { name: 'June 15', Score: 68 },
    { name: 'July 01', Score: 78 },
    { name: 'July 10', Score: 85 },
    { name: 'July 19', Score: 94 },
  ];

  // Mock optimizations list
  const [optimizations, setOptimizations] = useState([
    {
      id: 'opt-1',
      path: '/gaming-news/starfield-review',
      type: 'Metadata',
      original: { title: 'Starfield Game Review', desc: 'Read our review of starfield game.' },
      optimized: {
        title: 'Starfield Review: An Epic Sci-Fi Space Adventure',
        desc: 'Starfield delivers an ambitious cosmic sandbox. Read our deep-dive review on gameplay, performance, and features to see if it lives up to the hype.'
      },
      status: 'pending'
    },
    {
      id: 'opt-2',
      path: '/tech/cpu-benchmarks-2026',
      type: 'Metadata',
      original: { title: 'New CPU Benchmarks 2026', desc: 'Benchmarks for new CPUs.' },
      optimized: {
        title: 'Top CPU Benchmarks 2026: Intel vs AMD performance',
        desc: 'Compare the fastest CPUs of 2026. Explore detailed synthetic benchmarks, thermal benchmarks, and gaming performance results inside.'
      },
      status: 'pending'
    }
  ]);

  const handleRunAudit = async () => {
    try {
      setSuccessMessage(null);
      // Trigger backend celery audit task
      const response = await fetch('http://localhost:8000/api/v1/audits', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_id: projectId,
          url: 'https://newstigo.com', // target project url
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to trigger audit');
      }

      const data = await response.json();
      // Start polling
      setActiveTaskId(data.task_id);
    } catch (err: any) {
      alert(`Error starting audit: ${err.message}`);
    }
  };

  const handleApplyOpt = (id: string, statusType: 'applied' | 'skipped') => {
    setOptimizations((prev) =>
      prev.map((opt) => (opt.id === id ? { ...opt, status: statusType } : opt))
    );
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header Panel */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Newstigo Portal Audit</h1>
          <p className="text-slate-400 mt-1">Domain: https://newstigo.com</p>
        </div>

        <button
          onClick={handleRunAudit}
          disabled={!!activeTaskId}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-semibold shadow-lg transition-all duration-300 ${
            activeTaskId
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-white/5'
              : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-[0_0_15px_rgba(0,242,255,0.3)] transform hover:scale-[1.02]'
          }`}
        >
          <RefreshCw className={`h-5 w-5 ${activeTaskId ? 'animate-spin' : ''}`} />
          {activeTaskId ? 'Auditing Site...' : 'Run New Audit'}
        </button>
      </div>

      {/* Real-time Task Status Progress Panel */}
      {(activeTaskId || pollingError) && (
        <GlassCard className="border-neon-cyan/20">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-bold text-white flex items-center gap-2">
              <Cpu className="h-4 w-4 text-neon-cyan animate-pulse" />
              Status: <span className="text-neon-cyan capitalize">{status}</span>
            </span>
            <span className="text-sm font-bold text-neon-cyan">{progress}%</span>
          </div>
          
          <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-white/5">
            <div
              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-2 rounded-full transition-all duration-500 shadow-[0_0_10px_#00F2FF]"
              style={{ width: `${progress}%` }}
            />
          </div>
          
          {pollingError && (
            <div className="mt-3 flex items-center gap-2 text-sm text-neon-magenta">
              <ShieldAlert className="h-4 w-4" />
              <span>Failed to fetch status: {pollingError}</span>
            </div>
          )}
        </GlassCard>
      )}

      {successMessage && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg text-sm font-medium animate-pulse flex items-center gap-2">
          <Award className="h-5 w-5" />
          {successMessage}
        </div>
      )}

      {/* KPI Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <GlassCard hoverGlow>
          <h4 className="text-sm text-slate-400 font-medium">LCP (Speed)</h4>
          <p className="text-3xl font-extrabold text-white mt-2">1.8s</p>
          <span className="text-xs text-emerald-400 font-medium bg-emerald-400/10 px-2 py-0.5 rounded-full mt-2 inline-block">Good</span>
        </GlassCard>
        <GlassCard hoverGlow>
          <h4 className="text-sm text-slate-400 font-medium">CLS (Layout)</h4>
          <p className="text-3xl font-extrabold text-white mt-2">0.05</p>
          <span className="text-xs text-emerald-400 font-medium bg-emerald-400/10 px-2 py-0.5 rounded-full mt-2 inline-block">Stable</span>
        </GlassCard>
        <GlassCard hoverGlow>
          <h4 className="text-sm text-slate-400 font-medium">Mobile Score</h4>
          <p className="text-3xl font-extrabold text-yellow-400 mt-2">88</p>
          <span className="text-xs text-yellow-400 font-medium bg-yellow-400/10 px-2 py-0.5 rounded-full mt-2 inline-block">Needs Imp.</span>
        </GlassCard>
        <GlassCard hoverGlow>
          <h4 className="text-sm text-slate-400 font-medium">Desktop Score</h4>
          <p className="text-3xl font-extrabold text-neon-cyan mt-2">100</p>
          <span className="text-xs text-emerald-400 font-medium bg-emerald-400/10 px-2 py-0.5 rounded-full mt-2 inline-block">Perfect</span>
        </GlassCard>
      </div>

      {/* Historical line chart using Recharts */}
      <GlassCard className="h-[320px]">
        <h3 className="text-lg font-bold text-white mb-4">Historical Audit Performance</h3>
        <ResponsiveContainer width="100%" height="90%">
          <LineChart data={historyData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="name" stroke="#64748B" fontSize={12} tickLine={false} />
            <YAxis stroke="#64748B" fontSize={12} domain={[50, 100]} tickLine={false} />
            <Tooltip
              contentStyle={{ background: '#0F172A', borderColor: 'rgba(255,255,255,0.1)', color: '#FFF' }}
            />
            <Line
              type="monotone"
              dataKey="Score"
              stroke="#00F2FF"
              strokeWidth={3}
              activeDot={{ r: 8 }}
              dot={{ stroke: '#00F2FF', strokeWidth: 2, r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* Optimizations panel with glassmorphic cards */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white">AI Meta Optimizations</h3>
        <div className="space-y-4">
          {optimizations.map((opt) => (
            <GlassCard key={opt.id} className="relative overflow-hidden">
              {opt.status !== 'pending' && (
                <div className={`absolute top-0 right-0 px-4 py-1 text-xs font-bold capitalize ${
                  opt.status === 'applied'
                    ? 'bg-emerald-500/20 text-emerald-400 border-l border-b border-emerald-500/20'
                    : 'bg-slate-800 text-slate-400 border-l border-b border-white/5'
                }`}>
                  {opt.status}
                </div>
              )}

              <div className="flex flex-col md:flex-row justify-between gap-6">
                <div className="flex-1 space-y-4">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-semibold px-2 py-0.5 bg-neon-cyan/15 text-neon-cyan border border-neon-cyan/20 rounded">
                      {opt.type}
                    </span>
                    <span className="text-sm font-medium text-slate-500">{opt.path}</span>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left: Original */}
                    <div className="p-4 bg-slate-950/40 rounded-lg border border-white/5 space-y-2">
                      <p className="text-xs font-bold text-slate-500 uppercase">Original Elements</p>
                      <h4 className="text-sm font-semibold text-slate-300">{opt.original.title}</h4>
                      <p className="text-xs text-slate-400 leading-relaxed">{opt.original.desc}</p>
                    </div>

                    {/* Right: AI-Optimized */}
                    <div className="p-4 bg-slate-900/40 rounded-lg border border-neon-cyan/10 space-y-2">
                      <p className="text-xs font-bold text-neon-cyan uppercase">AI Recommendation</p>
                      <h4 className="text-sm font-bold text-white">{opt.optimized.title}</h4>
                      <p className="text-xs text-slate-200 leading-relaxed">{opt.optimized.desc}</p>
                    </div>
                  </div>
                </div>

                {/* Apply/Ignore Controls */}
                <div className="flex md:flex-col justify-end gap-3 self-center">
                  <button
                    onClick={() => handleApplyOpt(opt.id, 'applied')}
                    disabled={opt.status !== 'pending'}
                    className={`p-2.5 rounded-lg border ${
                      opt.status === 'applied'
                        ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                        : opt.status === 'pending'
                        ? 'border-neon-cyan/30 hover:border-neon-cyan bg-neon-cyan/10 hover:bg-neon-cyan text-neon-cyan hover:text-slate-950 transition-all cursor-pointer'
                        : 'border-white/5 text-slate-600 cursor-not-allowed'
                    }`}
                    title="Apply Recommendation"
                  >
                    <Check className="h-5 w-5" />
                  </button>
                  
                  <button
                    onClick={() => handleApplyOpt(opt.id, 'skipped')}
                    disabled={opt.status !== 'pending'}
                    className={`p-2.5 rounded-lg border ${
                      opt.status === 'skipped'
                        ? 'bg-slate-800 border-white/5 text-slate-400'
                        : opt.status === 'pending'
                        ? 'border-white/10 hover:border-neon-magenta bg-white/5 hover:bg-neon-magenta/20 text-slate-300 hover:text-neon-magenta transition-all cursor-pointer'
                        : 'border-white/5 text-slate-600 cursor-not-allowed'
                    }`}
                    title="Ignore Recommendation"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </div>
  );
}
