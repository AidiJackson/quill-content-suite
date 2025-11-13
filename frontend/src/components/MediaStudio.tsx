import { Card } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Video, Music, Scissors, Type, Maximize2, Sparkles, Volume2, Zap } from 'lucide-react';

export function MediaStudio() {
  const mediaItems = [
    { name: 'Product Demo Recording', type: 'Video', duration: '12:34', project: 'Q1 Launch', thumbnail: '🎥' },
    { name: 'Podcast Episode 45', type: 'Audio', duration: '45:12', project: 'Weekly Show', thumbnail: '🎙️' },
    { name: 'TikTok Highlights', type: 'Video', duration: '0:58', project: 'Social Campaign', thumbnail: '📱' },
    { name: 'Interview Recording', type: 'Video', duration: '28:41', project: 'Content Series', thumbnail: '🎬' },
    { name: 'Background Music Track', type: 'Audio', duration: '3:24', project: 'Media Assets', thumbnail: '🎵' },
  ];

  return (
    <div className="p-8">
      <div className="grid grid-cols-3 gap-8">
        {/* Left Column - Media Library */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-slate-900">Media Library</h4>
            <Button size="sm" variant="outline">Upload</Button>
          </div>

          <div className="space-y-3">
            {mediaItems.map((item, index) => (
              <Card 
                key={index}
                className="p-4 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer"
              >
                <div className="flex items-start gap-3">
                  <div className="w-16 h-16 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0 text-2xl">
                    {item.thumbnail}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h6 className="text-slate-900 text-sm truncate">{item.name}</h6>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge variant="secondary" className="text-xs bg-slate-100 text-slate-700">
                        {item.type === 'Video' ? <Video className="w-3 h-3 mr-1" /> : <Music className="w-3 h-3 mr-1" />}
                        {item.type}
                      </Badge>
                      <span className="text-xs text-slate-500">{item.duration}</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">{item.project}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Right Column - Editing Panel */}
        <div className="col-span-2 space-y-6">
          <Tabs defaultValue="video" className="w-full">
            <TabsList className="bg-slate-100 p-1">
              <TabsTrigger value="video">
                <Video className="w-4 h-4 mr-2" />
                Video
              </TabsTrigger>
              <TabsTrigger value="audio">
                <Music className="w-4 h-4 mr-2" />
                Audio
              </TabsTrigger>
            </TabsList>

            <TabsContent value="video" className="mt-6 space-y-6">
              {/* Video Preview */}
              <Card className="p-6 bg-slate-900 border-slate-700">
                <div className="aspect-video bg-slate-800 rounded-lg flex items-center justify-center">
                  <div className="text-center text-slate-400">
                    <Video className="w-12 h-12 mx-auto mb-3 opacity-50" />
                    <p className="text-sm">Video Preview</p>
                    <p className="text-xs mt-1 opacity-75">Select a video to start editing</p>
                  </div>
                </div>
              </Card>

              {/* Video Timeline */}
              <Card className="p-4 bg-white border-slate-200">
                <p className="text-sm text-slate-600 mb-3">Timeline</p>
                <div className="h-20 bg-slate-100 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300">
                  <p className="text-xs text-slate-500">Video timeline will appear here</p>
                </div>
              </Card>

              {/* Video Controls */}
              <div className="grid grid-cols-2 gap-4">
                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-blue-50 rounded-lg">
                      <Scissors className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Trim Clip</h5>
                      <p className="text-xs text-slate-600">Cut and trim video segments</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-purple-50 rounded-lg">
                      <Type className="w-5 h-5 text-purple-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Add Captions</h5>
                      <p className="text-xs text-slate-600">Auto-generate subtitles</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-green-50 rounded-lg">
                      <Maximize2 className="w-5 h-5 text-green-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Resize Format</h5>
                      <p className="text-xs text-slate-600">TikTok / Shorts / Reels</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-orange-50 rounded-lg">
                      <Sparkles className="w-5 h-5 text-orange-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Auto-cut Highlights</h5>
                      <p className="text-xs text-slate-600">AI-powered best moments</p>
                    </div>
                  </div>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="audio" className="mt-6 space-y-6">
              {/* Audio Waveform */}
              <Card className="p-6 bg-slate-900 border-slate-700">
                <div className="h-48 bg-slate-800 rounded-lg flex items-center justify-center relative overflow-hidden">
                  <div className="absolute inset-0 flex items-center justify-center gap-1 px-8">
                    {Array.from({ length: 60 }).map((_, i) => (
                      <div
                        key={i}
                        className="flex-1 bg-blue-500/30 rounded-full"
                        style={{ height: `${Math.random() * 100 + 20}%` }}
                      />
                    ))}
                  </div>
                  <div className="relative text-center text-slate-400">
                    <Music className="w-12 h-12 mx-auto mb-3 opacity-50" />
                    <p className="text-sm">Audio Waveform</p>
                  </div>
                </div>
              </Card>

              {/* Audio Controls */}
              <div className="grid grid-cols-2 gap-4">
                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-blue-50 rounded-lg">
                      <Volume2 className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Cleanup Noise</h5>
                      <p className="text-xs text-slate-600">Remove background noise</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-purple-50 rounded-lg">
                      <Music className="w-5 h-5 text-purple-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Pitch Shift</h5>
                      <p className="text-xs text-slate-600">Adjust audio pitch</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-green-50 rounded-lg">
                      <Zap className="w-5 h-5 text-green-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Tempo Change</h5>
                      <p className="text-xs text-slate-600">Speed up or slow down</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-orange-50 rounded-lg">
                      <Video className="w-5 h-5 text-orange-600" />
                    </div>
                    <div>
                      <h5 className="text-slate-900 text-sm mb-1">Extract from Video</h5>
                      <p className="text-xs text-slate-600">Get audio from video file</p>
                    </div>
                  </div>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
