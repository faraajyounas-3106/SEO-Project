// frontend/app/page.tsx
'use client';

import { useState } from 'react';
import { Sidebar } from '../components/sidebar';
import { DashboardView } from '../components/dashboard-view';
import { AuditDetails } from '../components/audit-details';
import { GlassCard } from '../components/ui/glass-card';
import { Sliders, HelpCircle } from 'lucide-react';

export default function Home() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(
    'f87a8b3e-e24c-4c60-84e9-270830db9df2' // Default project ID to view details
  );

  const renderContent = () => {
    switch (currentTab) {
      case 'dashboard':
        return (
          <DashboardView
            onSelectProject={setSelectedProjectId}
            setCurrentTab={setCurrentTab}
          />
        );
      case 'audits':
        return selectedProjectId ? (
          <AuditDetails projectId={selectedProjectId} />
        ) : (
          <div className="text-center py-20 text-slate-400">
            Please select a project from the Dashboard tab first.
          </div>
        );
      case 'settings':
        return (
          <div className="space-y-6 animate-fade-in">
            <h1 className="text-3xl font-extrabold text-white">General Settings</h1>
            <p className="text-slate-400">Configure PageSpeed API credentials and subscription limits.</p>
            <GlassCard>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-400 mb-2">
                    Google PageSpeed API Key
                  </label>
                  <input
                    type="password"
                    placeholder="AIzaSy..."
                    className="w-full bg-slate-900/60 border border-white/10 rounded-lg p-3 text-white placeholder-slate-600 focus:outline-none focus:border-neon-cyan"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-400 mb-2">
                    Gemini API Key
                  </label>
                  <input
                    type="password"
                    placeholder="AIzaSy..."
                    className="w-full bg-slate-900/60 border border-white/10 rounded-lg p-3 text-white placeholder-slate-600 focus:outline-none focus:border-neon-cyan"
                  />
                </div>
              </div>
            </GlassCard>
          </div>
        );
      default:
        return (
          <div className="text-center py-20 text-slate-400">
            Tab in development...
          </div>
        );
    }
  };

  return (
    <div className="flex bg-slate-950 text-slate-100 min-h-screen">
      {/* Sidebar Navigation */}
      <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      {/* Main Content Workspace Area */}
      <main className="flex-1 p-10 overflow-y-auto max-w-7xl mx-auto space-y-8">
        {/* Top bar info */}
        <header className="flex justify-end gap-4 text-sm text-slate-500">
          <span className="flex items-center gap-1 cursor-pointer hover:text-white transition-colors">
            <Sliders className="h-4 w-4" /> Config Logs
          </span>
          <span className="flex items-center gap-1 cursor-pointer hover:text-white transition-colors">
            <HelpCircle className="h-4 w-4" /> Support
          </span>
        </header>

        {renderContent()}
      </main>
    </div>
  );
}