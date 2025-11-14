import { useState } from 'react';
import { Toaster } from 'sonner';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { Dashboard } from './components/Dashboard';
import { WrittenStudio } from './components/WrittenStudio';
import { ViralityLab } from './components/ViralityLab';
import { MediaStudio } from './components/MediaStudio';
import { MusicStudio } from './components/MusicStudio';
import { AIVideoCreator } from './components/AIVideoCreator';
import { ViralFactory } from './components/ViralFactory';
import { Calendar } from './components/Calendar';
import { ProjectDetail } from './components/ProjectDetail';

type View = 'dashboard' | 'written' | 'virality' | 'media' | 'music' | 'aivideo' | 'viralfactory' | 'calendar' | 'projects' | 'settings';

export default function App() {
  const [currentView, setCurrentView] = useState<View>('dashboard');

  const getPageTitle = () => {
    switch (currentView) {
      case 'dashboard': return 'Dashboard';
      case 'written': return 'Written Content Studio';
      case 'virality': return 'Virality & Trends Lab';
      case 'media': return 'Media Studio — Video & Audio';
      case 'music': return 'Music Studio — AI Music Creation';
      case 'aivideo': return 'AI Short Video Creator';
      case 'viralfactory': return 'Viral Factory';
      case 'calendar': return 'Content Calendar';
      case 'projects': return 'Project Detail';
      case 'settings': return 'Settings';
      default: return 'Dashboard';
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'dashboard': return <Dashboard />;
      case 'written': return <WrittenStudio />;
      case 'virality': return <ViralityLab />;
      case 'media': return <MediaStudio />;
      case 'music': return <MusicStudio />;
      case 'aivideo': return <AIVideoCreator />;
      case 'viralfactory': return <ViralFactory />;
      case 'calendar': return <Calendar />;
      case 'projects': return <ProjectDetail />;
      case 'settings': return <div className="p-8">Settings view coming soon...</div>;
      default: return <Dashboard />;
    }
  };

  return (
    <>
      <Toaster position="top-right" richColors />
      <div className="flex h-screen bg-slate-50">
        <Sidebar currentView={currentView} onNavigate={setCurrentView} />

        <div className="flex-1 flex flex-col overflow-hidden">
          <TopBar pageTitle={getPageTitle()} />

          <main className="flex-1 overflow-y-auto">
            {renderView()}
          </main>
        </div>
      </div>
    </>
  );
}