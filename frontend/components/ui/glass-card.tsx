import React from 'react';

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  hoverGlow?: boolean;
}

export function GlassCard({ children, className = '', hoverGlow = false, ...props }: GlassCardProps) {
  const glowClass = hoverGlow ? 'glow-cyan-hover' : '';
  return (
    <div
      className={`bg-glass rounded-xl p-6 shadow-2xl transition-all duration-300 ${glowClass} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
