import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { FileText, Video, Mail, MessageSquare, Image, Music, Plus, TrendingUp, CheckCircle2, Clock } from 'lucide-react';

export function ProjectDetail() {
  const timelineItems = [
    {
      title: 'Product Launch Blog Post',
      type: 'blog',
      status: 'published',
      date: '2 hours ago',
      virality: 92,
    },
    {
      title: 'Weekly Newsletter #45',
      type: 'newsletter',
      status: 'draft',
      date: '5 hours ago',
      virality: 78,
    },
    {
      title: 'LinkedIn Announcement',
      type: 'social',
      status: 'published',
      date: '1 day ago',
      virality: 88,
    },
    {
      title: 'TikTok Teaser Clip',
      type: 'video',
      status: 'draft',
      date: '2 days ago',
      virality: 85,
    },
    {
      title: 'Promo Music Track',
      type: 'track',
      status: 'published',
      date: '3 days ago',
      virality: 89,
    },
    {
      title: 'YouTube Full Demo',
      type: 'video',
      status: 'scheduled',
      date: 'Scheduled for tomorrow',
      virality: 91,
    },
  ];

  const mediaFiles = [
    { name: 'product-demo-final.mp4', type: 'video', size: '124 MB' },
    { name: 'promo-track.mp3', type: 'audio', size: '8.5 MB' },
    { name: 'hero-image.png', type: 'image', size: '2.1 MB' },
    { name: 'logo-variations.svg', type: 'image', size: '340 KB' },
    { name: 'background-music.mp3', type: 'audio', size: '4.2 MB' },
    { name: 'testimonial-clip.mp4', type: 'video', size: '45 MB' },
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'blog': return <FileText className="w-4 h-4" />;
      case 'newsletter': return <Mail className="w-4 h-4" />;
      case 'social': return <MessageSquare className="w-4 h-4" />;
      case 'video': return <Video className="w-4 h-4" />;
      case 'track': return <Music className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'published':
        return <Badge className="bg-green-50 text-green-700 border-green-200"><CheckCircle2 className="w-3 h-3 mr-1" />Published</Badge>;
      case 'draft':
        return <Badge variant="secondary" className="bg-slate-100 text-slate-700"><Clock className="w-3 h-3 mr-1" />Draft</Badge>;
      case 'scheduled':
        return <Badge className="bg-blue-50 text-blue-700 border-blue-200"><Clock className="w-3 h-3 mr-1" />Scheduled</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const getMediaIcon = (type: string) => {
    switch (type) {
      case 'video': return <Video className="w-4 h-4 text-purple-600" />;
      case 'audio': return <Music className="w-4 h-4 text-blue-600" />;
      case 'image': return <Image className="w-4 h-4 text-green-600" />;
      default: return <FileText className="w-4 h-4 text-slate-600" />;
    }
  };

  return (
    <div className="p-8">
      {/* Project Header */}
      <div className="mb-8">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-slate-900 mb-2">Q1 Product Launch</h3>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-purple-50 text-purple-700">Launch</Badge>
              <Badge variant="secondary" className="bg-blue-50 text-blue-700">B2B SaaS</Badge>
              <Badge variant="secondary" className="bg-green-50 text-green-700">Multi-channel</Badge>
            </div>
          </div>
          <Badge className="bg-green-50 text-green-700 border-green-200 px-4 py-2">
            <TrendingUp className="w-4 h-4 mr-2" />
            Avg Virality: 87
          </Badge>
        </div>
        <p className="text-slate-600">
          Coordinated content campaign for the Q1 product launch across blog, social media, email, video, and music platforms.
        </p>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Left Column - Project Timeline */}
        <div className="col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h4 className="text-slate-900">Content Timeline</h4>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              Add Content
            </Button>
          </div>

          <div className="space-y-3">
            {timelineItems.map((item, index) => (
              <Card key={index} className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                <div className="flex items-start gap-4">
                  <div className={`p-2.5 rounded-lg ${
                    item.type === 'blog' ? 'bg-blue-50' :
                    item.type === 'newsletter' ? 'bg-purple-50' :
                    item.type === 'social' ? 'bg-green-50' :
                    item.type === 'track' ? 'bg-pink-50' :
                    'bg-orange-50'
                  }`}>
                    {getTypeIcon(item.type)}
                  </div>

                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h5 className="text-slate-900">{item.title}</h5>
                        <p className="text-sm text-slate-500 mt-1">{item.date}</p>
                      </div>
                      {getStatusBadge(item.status)}
                    </div>

                    <div className="flex items-center gap-4 mt-3">
                      <div className="flex items-center gap-2">
                        <TrendingUp className="w-4 h-4 text-slate-400" />
                        <span className="text-sm text-slate-600">Virality: {item.virality}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Right Column - Project Resources */}
        <div className="space-y-6">
          {/* Project Health */}
          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
            <h5 className="text-slate-900 mb-4">Project Health</h5>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-700">Content Created</span>
                  <span className="text-sm text-slate-900">6 / 8</span>
                </div>
                <div className="h-2 bg-white rounded-full overflow-hidden">
                  <div className="h-full bg-green-500" style={{ width: '75%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-700">Published</span>
                  <span className="text-sm text-slate-900">3 / 6</span>
                </div>
                <div className="h-2 bg-white rounded-full overflow-hidden">
                  <div className="h-full bg-green-500" style={{ width: '50%' }}></div>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-700">Launch Readiness</span>
                  <span className="text-sm text-slate-900">88%</span>
                </div>
                <div className="h-2 bg-white rounded-full overflow-hidden">
                  <div className="h-full bg-green-500" style={{ width: '88%' }}></div>
                </div>
              </div>

              <div className="pt-4 border-t border-green-200">
                <div className="flex items-center justify-between text-sm mb-1">
                  <span className="text-slate-700">Channels Covered</span>
                  <span className="text-slate-900">6</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-700">Assets Created</span>
                  <span className="text-slate-900">12</span>
                </div>
              </div>
            </div>

            <Badge className="w-full justify-center mt-4 bg-green-600 text-white">
              <CheckCircle2 className="w-3 h-3 mr-1" />
              On Track
            </Badge>
          </Card>

          {/* Media Resources */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h5 className="text-slate-900">Resources & Media</h5>
              <Button size="sm" variant="outline">Upload</Button>
            </div>

            <div className="space-y-2">
              {mediaFiles.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer"
                >
                  <div className="p-2 bg-slate-100 rounded">
                    {getMediaIcon(file.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-900 truncate">{file.name}</p>
                    <p className="text-xs text-slate-500">{file.size}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Quick Actions */}
          <div className="space-y-2">
            <Button className="w-full bg-slate-900 hover:bg-slate-800">
              <Plus className="w-4 h-4 mr-2" />
              Add Content Item
            </Button>
            <Button variant="outline" className="w-full">
              Export Project Report
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}