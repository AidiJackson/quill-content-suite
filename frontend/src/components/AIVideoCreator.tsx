import { Card } from './ui/card';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Switch } from './ui/switch';
import { Sparkles, Smartphone } from 'lucide-react';
import { Badge } from './ui/badge';

export function AIVideoCreator() {
  return (
    <div className="p-8">
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column - Script/Input */}
        <div className="space-y-6">
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-6">
              <Sparkles className="w-5 h-5 text-blue-600" />
              <h4 className="text-slate-900">Script or Idea</h4>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="video-script" className="text-sm text-slate-700">Describe the video or paste your script</Label>
                <Textarea
                  id="video-script"
                  placeholder="Example: Create a 30-second motivational video about overcoming challenges. Start with a hook question, show 3 key tips with text overlays, end with a call to action..."
                  className="mt-2 min-h-[250px] resize-none"
                  defaultValue="A 60-second TikTok about '3 productivity hacks that changed my life':

Hook: 'I used to work 12 hours a day and get nothing done...'

Tip 1: Time blocking (show calendar)
Tip 2: Single-tasking (cross out multitasking)
Tip 3: 2-minute rule (quick wins)

CTA: Try these today and watch your productivity soar!"
                />
              </div>

              <div>
                <Label htmlFor="format" className="text-sm text-slate-700">Format</Label>
                <Select defaultValue="tiktok">
                  <SelectTrigger id="format" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="tiktok">TikTok (9:16)</SelectItem>
                    <SelectItem value="reel">Instagram Reel (9:16)</SelectItem>
                    <SelectItem value="short">YouTube Short (9:16)</SelectItem>
                    <SelectItem value="story">Story (9:16)</SelectItem>
                    <SelectItem value="landscape">Landscape (16:9)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="theme" className="text-sm text-slate-700">Theme</Label>
                <Select defaultValue="motivational">
                  <SelectTrigger id="theme" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="motivational">Motivational</SelectItem>
                    <SelectItem value="storytime">Storytime</SelectItem>
                    <SelectItem value="educational">Educational</SelectItem>
                    <SelectItem value="music">Music Video</SelectItem>
                    <SelectItem value="podcast">Podcast Clip</SelectItem>
                    <SelectItem value="product">Product Demo</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button className="w-full bg-slate-900 hover:bg-slate-800 mt-2">
                <Sparkles className="w-4 h-4 mr-2" />
                Generate Clip
              </Button>
            </div>
          </Card>
        </div>

        {/* Right Column - Preview & Controls */}
        <div className="space-y-6">
          {/* Preview */}
          <Card className="p-6 bg-slate-900 border-slate-700 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <Smartphone className="w-5 h-5 text-slate-400" />
              <h5 className="text-white">Preview</h5>
            </div>

            {/* Phone Frame */}
            <div className="flex justify-center">
              <div className="w-64 bg-slate-800 rounded-3xl p-3 shadow-xl">
                <div className="aspect-[9/16] bg-gradient-to-br from-slate-700 to-slate-800 rounded-2xl overflow-hidden relative">
                  {/* Simulated video preview */}
                  <div className="absolute inset-0 flex flex-col justify-between p-4">
                    <div className="text-white text-center">
                      <p className="text-xs opacity-75 mb-2">00:15 / 01:00</p>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="bg-black/60 backdrop-blur-sm px-3 py-2 rounded-lg">
                        <p className="text-white text-sm">I used to work 12 hours a day...</p>
                      </div>
                      <div className="bg-black/60 backdrop-blur-sm px-3 py-2 rounded-lg">
                        <p className="text-white text-sm">Here's what changed 🔥</p>
                      </div>
                    </div>
                  </div>

                  <div className="absolute top-4 right-4 space-y-3">
                    <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                      <span className="text-white text-xl">👤</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Video Options */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <h5 className="text-slate-900 mb-4">Video Options</h5>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-sm text-slate-900">Auto-captions</Label>
                  <p className="text-xs text-slate-600">Add animated subtitles</p>
                </div>
                <Switch defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-sm text-slate-900">Emojis</Label>
                  <p className="text-xs text-slate-600">Auto-insert relevant emojis</p>
                </div>
                <Switch defaultChecked />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-sm text-slate-900">Zoom effects</Label>
                  <p className="text-xs text-slate-600">Dynamic zoom on key points</p>
                </div>
                <Switch />
              </div>

              <div className="pt-4 border-t border-slate-200">
                <Label htmlFor="bg-music" className="text-sm text-slate-700">Background Music</Label>
                <Select defaultValue="from-studio">
                  <SelectTrigger id="bg-music" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="from-studio">From Music Studio</SelectItem>
                    <SelectItem value="none">No Music</SelectItem>
                    <SelectItem value="library">Stock Library</SelectItem>
                    <SelectItem value="upload">Upload Custom</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </Card>

          {/* Scene Timeline */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <h5 className="text-slate-900 mb-4">Scene Timeline</h5>
            
            <div className="flex gap-3 overflow-x-auto pb-2">
              {['Hook', 'Tip 1', 'Tip 2', 'Tip 3', 'CTA'].map((scene, index) => (
                <div key={index} className="flex-shrink-0">
                  <div className="w-24 h-32 bg-slate-100 rounded-lg border-2 border-slate-200 hover:border-blue-400 transition-colors cursor-pointer flex items-center justify-center relative">
                    <span className="text-sm text-slate-600">{scene}</span>
                    <Badge className="absolute -top-2 -right-2 text-xs bg-slate-900 text-white">
                      {index + 1}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-500 text-center mt-2">{(index * 12) + 5}s</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
