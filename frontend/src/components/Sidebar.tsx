import { Home, FileText, TrendingUp, Film, Folder, Settings, Music, Sparkles, Zap, CalendarDays } from 'lucide-react';

type View = 'dashboard' | 'written' | 'virality' | 'media' | 'music' | 'aivideo' | 'viralfactory' | 'calendar' | 'projects' | 'settings';

interface SidebarProps {
  currentView: View;
  onNavigate: (view: View) => void;
}

export function Sidebar({ currentView, onNavigate }: SidebarProps) {
  const navItems = [
    { id: 'dashboard' as View, label: 'Dashboard', icon: Home },
    { id: 'written' as View, label: 'Written Studio', icon: FileText },
    { id: 'virality' as View, label: 'Virality Lab', icon: TrendingUp },
    { id: 'media' as View, label: 'Media Studio', icon: Film },
    { id: 'music' as View, label: 'Music Studio', icon: Music },
    { id: 'aivideo' as View, label: 'AI Video Creator', icon: Sparkles },
    { id: 'viralfactory' as View, label: 'Viral Factory', icon: Zap },
    { id: 'calendar' as View, label: 'Calendar', icon: CalendarDays },
    { id: 'projects' as View, label: 'Projects', icon: Folder },
    { id: 'settings' as View, label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
      {/* Logo/Brand */}
      <div className="p-6 border-b border-slate-200">
        <h1 className="text-slate-900">Quillography</h1>
        <p className="text-sm text-slate-500 mt-0.5">Content Suite</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`
                w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all
                ${isActive 
                  ? 'bg-slate-900 text-white shadow-sm' 
                  : 'text-slate-600 hover:bg-slate-100'
                }
              `}
            >
              <Icon className="w-5 h-5" />
              <span className="text-sm">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}