import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ChevronLeft, ChevronRight, FileText, Video, Mail, MessageSquare, Music, TrendingUp } from 'lucide-react';

export function Calendar() {
  const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  
  const calendarDays = [
    { day: 1, items: [] },
    { day: 2, items: [{ type: 'blog', channel: 'Blog', time: '9 AM' }] },
    { day: 3, items: [] },
    { day: 4, items: [{ type: 'social', channel: 'LinkedIn', time: '2 PM' }] },
    { day: 5, items: [{ type: 'video', channel: 'TikTok', time: '5 PM' }] },
    { day: 6, items: [] },
    { day: 7, items: [] },
    { day: 8, items: [{ type: 'newsletter', channel: 'Email', time: '10 AM' }] },
    { day: 9, items: [{ type: 'social', channel: 'Twitter', time: '3 PM' }, { type: 'video', channel: 'Reel', time: '6 PM' }] },
    { day: 10, items: [] },
    { day: 11, items: [{ type: 'music', channel: 'Release', time: '12 PM' }] },
    { day: 12, items: [{ type: 'blog', channel: 'Blog', time: '9 AM' }] },
    { day: 13, items: [] },
    { day: 14, items: [] },
    { day: 15, items: [{ type: 'social', channel: 'LinkedIn', time: '11 AM' }] },
    { day: 16, items: [{ type: 'video', channel: 'YouTube', time: '4 PM' }] },
    { day: 17, items: [] },
    { day: 18, items: [{ type: 'newsletter', channel: 'Email', time: '10 AM' }] },
    { day: 19, items: [{ type: 'social', channel: 'Twitter', time: '1 PM' }] },
    { day: 20, items: [] },
    { day: 21, items: [] },
    { day: 22, items: [{ type: 'video', channel: 'TikTok', time: '5 PM' }] },
    { day: 23, items: [{ type: 'blog', channel: 'Blog', time: '9 AM' }, { type: 'music', channel: 'Track', time: '2 PM' }] },
    { day: 24, items: [] },
    { day: 25, items: [{ type: 'social', channel: 'LinkedIn', time: '10 AM' }] },
    { day: 26, items: [] },
    { day: 27, items: [{ type: 'video', channel: 'Short', time: '6 PM' }] },
    { day: 28, items: [] },
    { day: 29, items: [{ type: 'newsletter', channel: 'Email', time: '10 AM' }] },
    { day: 30, items: [] },
  ];

  const upcomingItems = [
    { title: 'Q1 Launch Announcement', channel: 'LinkedIn', date: 'Today, 2 PM', viralityScore: 92, type: 'social' },
    { title: 'TikTok Product Teaser', channel: 'TikTok', date: 'Today, 5 PM', viralityScore: 88, type: 'video' },
    { title: 'Weekly Newsletter #46', channel: 'Email', date: 'Tomorrow, 10 AM', viralityScore: 78, type: 'newsletter' },
    { title: 'Behind-the-scenes Track', channel: 'Music Release', date: 'Nov 11, 12 PM', viralityScore: 85, type: 'music' },
    { title: 'Feature Tutorial Blog', channel: 'Blog', date: 'Nov 12, 9 AM', viralityScore: 81, type: 'blog' },
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'blog': return <FileText className="w-3 h-3" />;
      case 'video': return <Video className="w-3 h-3" />;
      case 'social': return <MessageSquare className="w-3 h-3" />;
      case 'newsletter': return <Mail className="w-3 h-3" />;
      case 'music': return <Music className="w-3 h-3" />;
      default: return <FileText className="w-3 h-3" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'blog': return 'bg-blue-500';
      case 'video': return 'bg-purple-500';
      case 'social': return 'bg-green-500';
      case 'newsletter': return 'bg-orange-500';
      case 'music': return 'bg-pink-500';
      default: return 'bg-slate-500';
    }
  };

  return (
    <div className="p-8">
      <div className="grid grid-cols-3 gap-8">
        {/* Calendar View */}
        <div className="col-span-2 space-y-6">
          {/* Calendar Header */}
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-slate-900">November 2024</h4>
              <p className="text-sm text-slate-600 mt-1">Your content schedule at a glance</p>
            </div>
            <div className="flex items-center gap-2">
              <Button size="sm" variant="outline">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="outline">Today</Button>
              <Button size="sm" variant="outline">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Calendar Grid */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            {/* Day Headers */}
            <div className="grid grid-cols-7 gap-2 mb-4">
              {daysOfWeek.map((day) => (
                <div key={day} className="text-center text-sm text-slate-600 py-2">
                  {day}
                </div>
              ))}
            </div>

            {/* Calendar Days */}
            <div className="grid grid-cols-7 gap-2">
              {calendarDays.map((dayData, index) => (
                <div
                  key={index}
                  className={`
                    min-h-24 p-2 border border-slate-200 rounded-lg hover:border-slate-300 transition-colors
                    ${dayData.day === 4 ? 'bg-blue-50 border-blue-200' : 'bg-white'}
                  `}
                >
                  <span className={`text-sm ${dayData.day === 4 ? 'text-blue-900' : 'text-slate-900'}`}>
                    {dayData.day}
                  </span>
                  <div className="mt-2 space-y-1">
                    {dayData.items.map((item, itemIndex) => (
                      <div
                        key={itemIndex}
                        className={`w-full h-1.5 rounded-full ${getTypeColor(item.type)}`}
                        title={`${item.channel} - ${item.time}`}
                      />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Legend */}
          <div className="flex items-center gap-6 text-sm">
            <span className="text-slate-600">Legend:</span>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500" />
              <span className="text-slate-700">Blog</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-purple-500" />
              <span className="text-slate-700">Video</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-slate-700">Social</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-500" />
              <span className="text-slate-700">Newsletter</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-pink-500" />
              <span className="text-slate-700">Music</span>
            </div>
          </div>
        </div>

        {/* Upcoming This Week */}
        <div className="space-y-6">
          <div>
            <h4 className="text-slate-900 mb-4">Upcoming This Week</h4>
            <div className="space-y-3">
              {upcomingItems.map((item, index) => (
                <Card
                  key={index}
                  className="p-4 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer"
                >
                  <div className="flex items-start gap-3 mb-3">
                    <div className={`p-2 rounded-lg ${
                      item.type === 'blog' ? 'bg-blue-50' :
                      item.type === 'video' ? 'bg-purple-50' :
                      item.type === 'social' ? 'bg-green-50' :
                      item.type === 'newsletter' ? 'bg-orange-50' :
                      'bg-pink-50'
                    }`}>
                      {getTypeIcon(item.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h6 className="text-sm text-slate-900 truncate">{item.title}</h6>
                      <p className="text-xs text-slate-600 mt-1">{item.channel}</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-500">{item.date}</span>
                    <Badge 
                      className={`
                        ${item.viralityScore >= 85 ? 'bg-green-50 text-green-700 border-green-200' : ''}
                        ${item.viralityScore >= 70 && item.viralityScore < 85 ? 'bg-blue-50 text-blue-700 border-blue-200' : ''}
                        ${item.viralityScore < 70 ? 'bg-slate-100 text-slate-700 border-slate-200' : ''}
                      `}
                    >
                      <TrendingUp className="w-3 h-3 mr-1" />
                      {item.viralityScore}
                    </Badge>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          <Button className="w-full bg-slate-900 hover:bg-slate-800">
            Schedule New Content
          </Button>

          <Card className="p-5 bg-gradient-to-br from-blue-50 to-purple-50 border-slate-200">
            <h6 className="text-sm text-slate-900 mb-2">Weekly Stats</h6>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-600">Posts scheduled</span>
                <span className="text-slate-900">14</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-600">Channels covered</span>
                <span className="text-slate-900">6</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-600">Avg. virality</span>
                <span className="text-green-700">85</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
