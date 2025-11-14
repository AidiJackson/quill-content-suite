import { useEffect, useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { FileText, Mail, MessageSquare, Video, TrendingUp, Linkedin, Twitter, Music, Sparkles, Loader2 } from 'lucide-react';
import { Badge } from './ui/badge';
import { toast } from 'sonner';
import apiClient from '@/lib/apiClient';
import type { DashboardSummary, Project } from '@/lib/types';

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Fetch dashboard summary and recent projects in parallel
        const [summaryData, projectsData] = await Promise.all([
          apiClient.dashboard.getSummary(),
          apiClient.projects.list({ limit: 4 }),
        ]);

        setSummary(summaryData);
        setProjects(projectsData);
      } catch (error: any) {
        console.error('Failed to fetch dashboard data:', error);
        toast.error('Failed to load dashboard data', {
          description: error.detail || error.message || 'Please try again',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const kpis = summary
    ? [
        { label: 'Active Projects', value: summary.active_projects.toString(), change: 'Total projects' },
        { label: 'Pieces This Week', value: summary.items_created_this_week.toString(), change: 'Last 7 days' },
        { label: 'Avg. Virality Score', value: summary.avg_virality_score.toFixed(1), change: 'All content' },
        { label: 'Video Clips Generated', value: summary.video_clips_generated.toString(), change: 'Total clips' },
        { label: 'Tracks in Production', value: summary.tracks_in_production.toString(), change: 'Total tracks' },
      ]
    : [
        { label: 'Active Projects', value: '—', change: 'Loading...' },
        { label: 'Pieces This Week', value: '—', change: 'Loading...' },
        { label: 'Avg. Virality Score', value: '—', change: 'Loading...' },
        { label: 'Video Clips Generated', value: '—', change: 'Loading...' },
        { label: 'Tracks in Production', value: '—', change: 'Loading...' },
      ];

  const quickActions = [
    { label: 'New Blog', icon: FileText, color: 'blue' },
    { label: 'New Social Post', icon: MessageSquare, color: 'green' },
    { label: 'New Newsletter', icon: Mail, color: 'purple' },
    { label: 'New Short Video', icon: Video, color: 'orange' },
    { label: 'New Track', icon: Music, color: 'pink' },
  ];

  // Helper function to format relative time
  const formatRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins} min${diffMins !== 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  };

  const todaySuggestions = [
    {
      topic: 'AI in Creative Workflows',
      format: 'LinkedIn Article',
      time: 'Post at 9 AM',
    },
    {
      topic: 'Behind-the-scenes Music Creation',
      format: 'TikTok Video',
      time: 'Post at 2 PM',
    },
    {
      topic: 'Productivity Tips for Creators',
      format: 'Twitter Thread',
      time: 'Post at 5 PM',
    },
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'blog': return <FileText className="w-4 h-4" />;
      case 'video': return <Video className="w-4 h-4" />;
      case 'social': return <MessageSquare className="w-4 h-4" />;
      case 'newsletter': return <Mail className="w-4 h-4" />;
      case 'track': return <Music className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  return (
    <div className="p-8 space-y-8">
      {/* Welcome Section */}
      <div>
        <h3 className="text-slate-900">Welcome back, Jordan</h3>
        <p className="text-slate-600 mt-1">Here's your content universe at a glance.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-5 gap-6">
        {kpis.map((kpi, index) => (
          <Card key={index} className="p-6 bg-white border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <p className="text-sm text-slate-600">{kpi.label}</p>
            <p className="text-slate-900 mt-2">{kpi.value}</p>
            <p className="text-xs text-slate-500 mt-1">{kpi.change}</p>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h4 className="text-slate-900 mb-4">Quick Actions</h4>
        <div className="grid grid-cols-5 gap-4">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <Button
                key={index}
                variant="outline"
                className="h-auto py-6 flex flex-col gap-3 bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50"
              >
                <div className={`p-3 rounded-lg bg-${action.color}-50`}>
                  <Icon className={`w-6 h-6 text-${action.color}-600`} />
                </div>
                <span className="text-slate-700">{action.label}</span>
              </Button>
            );
          })}
        </div>
      </div>

      {/* Recent Projects */}
      <div>
        <h4 className="text-slate-900 mb-4">Recent Projects</h4>
        <Card className="bg-white border-slate-200 shadow-sm">
          {loading ? (
            <div className="p-12 flex items-center justify-center">
              <Loader2 className="w-6 h-6 text-slate-400 animate-spin" />
              <span className="ml-2 text-slate-600">Loading projects...</span>
            </div>
          ) : projects.length === 0 ? (
            <div className="p-12 text-center">
              <FileText className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p className="text-slate-600">No projects yet</p>
              <p className="text-sm text-slate-500 mt-1">Create your first project to get started</p>
            </div>
          ) : (
            <div className="overflow-hidden">
              <table className="w-full">
                <thead className="border-b border-slate-200">
                  <tr>
                    <th className="text-left p-4 text-sm text-slate-600">Project Name</th>
                    <th className="text-left p-4 text-sm text-slate-600">Description</th>
                    <th className="text-left p-4 text-sm text-slate-600">Last Updated</th>
                  </tr>
                </thead>
                <tbody>
                  {projects.map((project) => (
                    <tr key={project.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors cursor-pointer">
                      <td className="p-4">
                        <span className="text-slate-900 font-medium">{project.title}</span>
                      </td>
                      <td className="p-4">
                        <span className="text-sm text-slate-600">
                          {project.description || 'No description'}
                        </span>
                      </td>
                      <td className="p-4 text-sm text-slate-600">
                        {formatRelativeTime(project.updated_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>

      {/* Today's Suggestions */}
      <div>
        <h4 className="text-slate-900 mb-4">Today's Suggestions</h4>
        <div className="grid grid-cols-3 gap-4">
          {todaySuggestions.map((suggestion, index) => (
            <Card key={index} className="p-5 bg-gradient-to-br from-blue-50 to-purple-50 border-slate-200 hover:shadow-md transition-shadow">
              <div className="flex items-start gap-3">
                <div className="p-2 bg-white rounded-lg shadow-sm">
                  <Sparkles className="w-5 h-5 text-blue-600" />
                </div>
                <div className="flex-1">
                  <h5 className="text-slate-900 text-sm mb-1">{suggestion.topic}</h5>
                  <p className="text-xs text-slate-600">{suggestion.format}</p>
                  <p className="text-xs text-blue-600 mt-2">{suggestion.time}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}