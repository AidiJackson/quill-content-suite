import { Card } from './ui/card';
import { Button } from './ui/button';
import { FileText, Mail, MessageSquare, Video, TrendingUp, Linkedin, Twitter, Music, Sparkles } from 'lucide-react';
import { Badge } from './ui/badge';

export function Dashboard() {
  const kpis = [
    { label: 'Active Projects', value: '12', change: '+3 this month' },
    { label: 'Pieces This Week', value: '38', change: '+14 vs last week' },
    { label: 'Avg. Virality Score', value: '87', change: '+5 points' },
    { label: 'Video Clips Generated', value: '156', change: '+42 this week' },
    { label: 'Tracks in Production', value: '8', change: '+3 new' },
  ];

  const quickActions = [
    { label: 'New Blog', icon: FileText, color: 'blue' },
    { label: 'New Social Post', icon: MessageSquare, color: 'green' },
    { label: 'New Newsletter', icon: Mail, color: 'purple' },
    { label: 'New Short Video', icon: Video, color: 'orange' },
    { label: 'New Track', icon: Music, color: 'pink' },
  ];

  const recentProjects = [
    {
      name: 'Q1 Product Launch',
      types: ['blog', 'video', 'social', 'track'],
      channels: ['LinkedIn', 'Twitter'],
      updated: '2 hours ago',
      viralityScore: 92,
    },
    {
      name: 'Personal Brand - Week 45',
      types: ['newsletter', 'social', 'video'],
      channels: ['LinkedIn'],
      updated: '5 hours ago',
      viralityScore: 78,
    },
    {
      name: 'Podcast Promotion',
      types: ['video', 'social', 'blog'],
      channels: ['Twitter', 'LinkedIn'],
      updated: '1 day ago',
      viralityScore: 85,
    },
    {
      name: 'Music Video Campaign',
      types: ['track', 'video', 'social'],
      channels: ['Twitter'],
      updated: '2 days ago',
      viralityScore: 89,
    },
  ];

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
          <div className="overflow-hidden">
            <table className="w-full">
              <thead className="border-b border-slate-200">
                <tr>
                  <th className="text-left p-4 text-sm text-slate-600">Project Name</th>
                  <th className="text-left p-4 text-sm text-slate-600">Type</th>
                  <th className="text-left p-4 text-sm text-slate-600">Channels</th>
                  <th className="text-left p-4 text-sm text-slate-600">Last Updated</th>
                  <th className="text-left p-4 text-sm text-slate-600">Virality Score</th>
                </tr>
              </thead>
              <tbody>
                {recentProjects.map((project, index) => (
                  <tr key={index} className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition-colors">
                    <td className="p-4">
                      <span className="text-slate-900">{project.name}</span>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        {project.types.map((type, i) => (
                          <div key={i} className="p-1.5 bg-slate-100 rounded text-slate-600">
                            {getTypeIcon(type)}
                          </div>
                        ))}
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        {project.channels.map((channel, i) => (
                          <Badge key={i} variant="secondary" className="text-xs bg-slate-100 text-slate-700">
                            {channel === 'LinkedIn' ? <Linkedin className="w-3 h-3 mr-1" /> : <Twitter className="w-3 h-3 mr-1" />}
                            {channel}
                          </Badge>
                        ))}
                      </div>
                    </td>
                    <td className="p-4 text-sm text-slate-600">{project.updated}</td>
                    <td className="p-4">
                      <Badge 
                        className={`
                          ${project.viralityScore >= 85 ? 'bg-green-50 text-green-700 border-green-200' : ''}
                          ${project.viralityScore >= 70 && project.viralityScore < 85 ? 'bg-blue-50 text-blue-700 border-blue-200' : ''}
                          ${project.viralityScore < 70 ? 'bg-slate-100 text-slate-700 border-slate-200' : ''}
                        `}
                      >
                        <TrendingUp className="w-3 h-3 mr-1" />
                        {project.viralityScore}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
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