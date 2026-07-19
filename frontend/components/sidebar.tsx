import React from 'react';
import { LayoutDashboard, Globe, Settings, BarChart2, Zap } from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
}

export function Sidebar({ currentTab, setCurrentTab }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', name: 'Dashboard', icon: LayoutDashboard },
    { id: 'projects', name: 'Projects', icon: Globe },
    { id: 'audits', name: 'Audit Reports', icon: BarChart2 },
    { id: 'settings', name: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-white/10 bg-slate-950/80 p-6 flex flex-col justify-between h-screen sticky top-0 backdrop-blur-md">
      <div>
        {/* Brand Logo */}
        <div className="flex items-center gap-2 mb-10">
          <Zap className="h-8 w-8 text-neon-cyan drop-shadow-[0_0_10px_#00F2FF]" />
          <span className="text-xl font-bold tracking-wider text-white">
            AERO<span className="text-neon-cyan">TECH</span>
          </span>
        </div>

        {/* Navigation Menu */}
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-neon-cyan/15 text-neon-cyan border border-neon-cyan/30 shadow-[0_0_15px_rgba(0,242,255,0.15)]'
                    : 'text-slate-400 hover:text-white hover:bg-white/5 border border-transparent'
                }`}
              >
                <Icon className={`h-5 w-5 ${isActive ? 'text-neon-cyan' : 'text-slate-400'}`} />
                {item.name}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="text-xs text-slate-500 text-center">
        AeroTech SEO Suite v1.0.0
      </div>
    </aside>
  );
}
