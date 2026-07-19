import React, { useState } from 'react';
import { GlassCard } from './ui/glass-card';
import { ArrowRight, Plus, Search, ExternalLink } from 'lucide-react';

interface Project {
  id: string;
  name: string;
  url: string;
  score: number;
  status: 'active' | 'queued' | 'error';
  lastAudit: string;
}

interface DashboardViewProps {
  onSelectProject: (id: string) => void;
  setCurrentTab: (tab: string) => void;
}

export function DashboardView({ onSelectProject, setCurrentTab }: DashboardViewProps) {
  const [searchTerm, setSearchTerm] = useState('');
  
  const [projects] = useState<Project[]>([
    {
      id: 'f87a8b3e-e24c-4c60-84e9-270830db9df2',
      name: 'Newstigo Portal',
      url: 'https://newstigo.com',
      score: 94,
      status: 'active',
      lastAudit: '2026-07-19',
    },
    {
      id: '3b2d6a5d-4f7b-40fa-ba41-d8a4f6b216c8',
      name: 'Tech Blog Pro',
      url: 'https://techblogpro.io',
      score: 88,
      status: 'active',
      lastAudit: '2026-07-18',
    },
    {
      id: '8a8b2c4d-612a-4b7b-891a-f12a3d4e5f6a',
      name: 'E-Commerce Hub',
      url: 'https://myshophub.com',
      score: 72,
      status: 'error',
      lastAudit: '2026-07-15',
    },
  ]);

  const filteredProjects = projects.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.url.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Top Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">
            Workspace Dashboard
          </h1>
          <p className="text-slate-400 mt-1">
            Monitor technical core web vitals and run automated SEO audits.
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-lg font-medium shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all duration-300 transform hover:scale-[1.02]">
          <Plus className="h-5 w-5" />
          Add Project
        </button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlassCard hoverGlow>
          <p className="text-sm font-semibold text-slate-400">Total Projects</p>
          <p className="text-4xl font-extrabold text-white mt-2">{projects.length}</p>
        </GlassCard>
        <GlassCard hoverGlow>
          <p className="text-sm font-semibold text-slate-400">Average SEO Score</p>
          <p className="text-4xl font-extrabold text-neon-cyan mt-2">84.6%</p>
        </GlassCard>
        <GlassCard hoverGlow>
          <p className="text-sm font-semibold text-slate-400">API Health Status</p>
          <div className="flex items-center gap-2 mt-4">
            <span className="h-3.5 w-3.5 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-lg font-bold text-slate-200">Database Connected</span>
          </div>
        </GlassCard>
      </div>

      {/* Projects Search and Grid */}
      <div className="space-y-4">
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-900/50 border border-white/10 rounded-lg py-3 pl-11 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-neon-cyan transition-all"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredProjects.map((project) => (
            <GlassCard
              key={project.id}
              hoverGlow
              onClick={() => {
                onSelectProject(project.id);
                setCurrentTab('audits');
              }}
              className="cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-white group-hover:text-neon-cyan transition-colors">
                      {project.name}
                    </h3>
                    <a
                      href={project.url}
                      target="_blank"
                      rel="noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="text-sm text-slate-400 flex items-center gap-1 mt-1 hover:text-white"
                    >
                      {project.url} <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                  
                  {/* Gauge score circle */}
                  <div className="relative flex items-center justify-center">
                    <svg className="w-16 h-16 transform -rotate-90">
                      <circle
                        cx="32"
                        cy="32"
                        r="26"
                        stroke="rgba(255,255,255,0.05)"
                        strokeWidth="4"
                        fill="transparent"
                      />
                      <circle
                        cx="32"
                        cy="32"
                        r="26"
                        stroke={project.score > 80 ? "#00F2FF" : project.score > 60 ? "#EAB308" : "#FF007A"}
                        strokeWidth="4"
                        fill="transparent"
                        strokeDasharray={163.3}
                        strokeDashoffset={163.3 - (163.3 * project.score) / 100}
                        className="transition-all duration-1000 ease-out"
                      />
                    </svg>
                    <span className="absolute text-xs font-bold text-white">{project.score}</span>
                  </div>
                </div>

                <div className="mt-6 flex items-center gap-3">
                  <span
                    className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                      project.status === 'active'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : project.status === 'queued'
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    }`}
                  >
                    {project.status.toUpperCase()}
                  </span>
                  <span className="text-xs text-slate-500">Last scanned: {project.lastAudit}</span>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-neon-cyan text-sm font-semibold group-hover:translate-x-1 transition-transform">
                <span>View Full Audit Details</span>
                <ArrowRight className="h-4 w-4" />
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </div>
  );
}
