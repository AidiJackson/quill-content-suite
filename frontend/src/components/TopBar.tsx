import { Bell } from 'lucide-react';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Badge } from './ui/badge';

interface TopBarProps {
  pageTitle: string;
}

export function TopBar({ pageTitle }: TopBarProps) {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8">
      <h2 className="text-slate-900">{pageTitle}</h2>
      
      <div className="flex items-center gap-4">
        <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
          Pro
        </Badge>
        
        <button className="relative p-2 text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full"></span>
        </button>
        
        <Avatar className="w-9 h-9">
          <AvatarFallback className="bg-slate-900 text-white text-sm">JD</AvatarFallback>
        </Avatar>
      </div>
    </header>
  );
}
