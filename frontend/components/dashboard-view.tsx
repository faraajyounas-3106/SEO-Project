import React, { useState, useEffect } from 'react';
import { GlassCard } from './ui/glass-card';
import { ArrowRight, Plus, Search, ExternalLink, X } from 'lucide-react';

interface Project {
  id: string;
  name: string;
  domain_url: string;
  latest_score: number | null;
  status: string;
  latest_audit_date: string | null;
}

interface DashboardViewProps {
  onSelectProject: (id: string) => void;
  setCurrentTab: (tab: string) => void;
}

export function DashboardView({ onSelectProject, setCurrentTab }: DashboardViewProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProjectUrl, setNewProjectUrl] = useState('');
  const [newProjectName, setNewProjectName] = useState('');

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const apiHost = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1';
      const res = await fetch(`http://${apiHost}:8000/api/v1/projects`);
      if (res.ok) {
        const data = await res.json();
        setProjects(data);
      }
    } catch (err) {
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleAddProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectUrl) return;

    try {
      const apiHost = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1';
      const res = await fetch(`http://${apiHost}:8000/api/v1/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: newProjectName || 'New Project',
          domain_url: newProjectUrl,
        }),
      });

      if (res.ok) {
        setIsModalOpen(false);
        setNewProjectUrl('');
        setNewProjectName('');
        fetchProjects(); // Refresh project list
      } else {
        const errorData = await res.json();
        alert(`Error: ${errorData.detail || 'Failed to create project'}`);
      }
    } catch (err) {
      alert('Error connecting to backend database.');
    }
  };

  const filteredProjects = projects.filter((p) =>
    (p.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.domain_url.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const averageScore = projects.length
    ? Math.round(
        projects.reduce((acc, curr) => acc + (curr.latest_score || 0), 0) /
          projects.filter((p) => p.latest_score !== null).length || 0
      )
    : 0;

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
        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-lg font-medium shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all duration-300 transform hover:scale-[1.02]"
        >
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
          <p className="text-4xl font-extrabold text-neon-cyan mt-2">{averageScore || '--'}%</p>
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

        {loading ? (
          <div className="text-center py-20 text-slate-400 animate-pulse">
            Connecting to PostgreSQL database...
          </div>
        ) : filteredProjects.length === 0 ? (
          <div className="text-center py-20 text-slate-500 border border-white/5 rounded-2xl bg-white/5">
            No projects found. Click "Add Project" to register your first domain.
          </div>
        ) : (
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
                        {project.name || 'Project'}
                      </h3>
                      <a
                        href={project.domain_url}
                        target="_blank"
                        rel="noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="text-sm text-slate-400 flex items-center gap-1 mt-1 hover:text-white"
                      >
                        {project.domain_url} <ExternalLink className="h-3 w-3" />
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
                          stroke={
                            project.latest_score && project.latest_score > 80
                              ? "#00F2FF"
                              : project.latest_score && project.latest_score > 60
                              ? "#EAB308"
                              : "#FF007A"
                          }
                          strokeWidth="4"
                          fill="transparent"
                          strokeDasharray={163.3}
                          strokeDashoffset={
                            163.3 - (163.3 * (project.latest_score || 0)) / 100
                          }
                          className="transition-all duration-1000 ease-out"
                        />
                      </svg>
                      <span className="absolute text-xs font-bold text-white">
                        {project.latest_score !== null ? project.latest_score : '--'}
                      </span>
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
                    <span className="text-xs text-slate-500">
                      Last scanned: {project.latest_audit_date || 'Never'}
                    </span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between text-neon-cyan text-sm font-semibold group-hover:translate-x-1 transition-transform">
                  <span>View Full Audit Details</span>
                  <ArrowRight className="h-4 w-4" />
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </div>

      {/* Add Project Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
          <GlassCard className="w-full max-w-md border border-neon-cyan/20 p-6 relative">
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
            >
              <X className="h-5 w-5" />
            </button>

            <h2 className="text-2xl font-bold text-white mb-6">Add New Project</h2>

            <form onSubmit={handleAddProject} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-slate-400 mb-2">
                  Project Domain URL
                </label>
                <input
                  type="url"
                  placeholder="https://example.com"
                  value={newProjectUrl}
                  onChange={(e) => setNewProjectUrl(e.target.value)}
                  required
                  className="w-full bg-slate-900 border border-white/10 rounded-lg p-3 text-white placeholder-slate-600 focus:outline-none focus:border-neon-cyan"
                />
              </div>

              <div className="pt-4 flex gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 py-3 border border-white/10 rounded-lg text-slate-300 hover:bg-white/5 transition-all text-sm font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-lg text-sm font-bold shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all"
                >
                  Create Project
                </button>
              </div>
            </form>
          </GlassCard>
        </div>
      )}
    </div>
  );
}
