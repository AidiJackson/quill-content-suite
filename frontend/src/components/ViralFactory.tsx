import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Zap, FileText, Video, Mail, MessageSquare, TrendingUp, Download, FolderPlus } from 'lucide-react';
import { Badge } from './ui/badge';

export function ViralFactory() {
  const campaignAssets = [
    {
      type: 'TikTok Short',
      icon: Video,
      description: '30s hook-driven video with trending sound',
      viralityScore: 91,
      color: 'purple',
    },
    {
      type: 'LinkedIn Post',
      icon: MessageSquare,
      description: 'Professional thought leadership post',
      viralityScore: 87,
      color: 'blue',
    },
    {
      type: 'Newsletter Blurb',
      icon: Mail,
      description: 'Email-optimized announcement',
      viralityScore: 78,
      color: 'green',
    },
    {
      type: 'YouTube Short',
      icon: Video,
      description: 'Vertical video with captions',
      viralityScore: 89,
      color: 'orange',
    },
    {
      type: 'Twitter Thread',
      icon: MessageSquare,
      description: '7-tweet story arc',
      viralityScore: 84,
      color: 'cyan',
    },
    {
      type: 'Blog Article',
      icon: FileText,
      description: 'Long-form SEO-optimized content',
      viralityScore: 76,
      color: 'indigo',
    },
  ];

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="flex items-center justify-center gap-3 mb-4">
          <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-slate-900">Viral Factory</h3>
        </div>
        <p className="text-slate-600">
          Turn 1 idea into a full content system. Generate multi-channel campaigns in seconds.
        </p>
      </div>

      {/* Input Panel */}
      <Card className="max-w-3xl mx-auto p-8 bg-gradient-to-br from-slate-50 to-blue-50 border-slate-200 shadow-lg">
        <h4 className="text-slate-900 mb-6">Campaign Configuration</h4>
        
        <div className="space-y-6">
          <div>
            <Label htmlFor="core-idea" className="text-sm text-slate-700">Core Idea / Message</Label>
            <Input
              id="core-idea"
              placeholder="e.g., Launching our new AI-powered music creation tool for content creators"
              className="mt-2"
              defaultValue="Announcing Quillography 2.0 - All-in-one content creation suite with AI music & video"
            />
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <Label htmlFor="main-channel" className="text-sm text-slate-700">Main Channel Focus</Label>
              <Select defaultValue="tiktok">
                <SelectTrigger id="main-channel" className="mt-1.5">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="tiktok">TikTok</SelectItem>
                  <SelectItem value="linkedin">LinkedIn</SelectItem>
                  <SelectItem value="youtube">YouTube</SelectItem>
                  <SelectItem value="newsletter">Newsletter</SelectItem>
                  <SelectItem value="instagram">Instagram</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="goal" className="text-sm text-slate-700">Campaign Goal</Label>
              <Select defaultValue="launch">
                <SelectTrigger id="goal" className="mt-1.5">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="growth">Audience Growth</SelectItem>
                  <SelectItem value="launch">Product Launch</SelectItem>
                  <SelectItem value="authority">Authority Building</SelectItem>
                  <SelectItem value="engagement">Community Engagement</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg">
            <Zap className="w-4 h-4 mr-2" />
            Generate Campaign
          </Button>
        </div>
      </Card>

      {/* Output Panel */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h4 className="text-slate-900">Campaign Preview</h4>
          <Badge className="bg-green-50 text-green-700 border-green-200">
            <TrendingUp className="w-3 h-3 mr-1" />
            Avg Score: 84
          </Badge>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {campaignAssets.map((asset, index) => {
            const Icon = asset.icon;
            return (
              <Card 
                key={index}
                className="p-6 bg-white border-slate-200 hover:border-slate-300 hover:shadow-lg transition-all cursor-pointer"
              >
                <div className="flex items-start gap-4 mb-4">
                  <div className={`p-3 rounded-lg bg-${asset.color}-50`}>
                    <Icon className={`w-6 h-6 text-${asset.color}-600`} />
                  </div>
                  <div className="flex-1">
                    <h5 className="text-slate-900 mb-1">{asset.type}</h5>
                    <p className="text-sm text-slate-600">{asset.description}</p>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-200">
                  <Badge 
                    className={`
                      ${asset.viralityScore >= 85 ? 'bg-green-50 text-green-700 border-green-200' : ''}
                      ${asset.viralityScore >= 70 && asset.viralityScore < 85 ? 'bg-blue-50 text-blue-700 border-blue-200' : ''}
                      ${asset.viralityScore < 70 ? 'bg-slate-100 text-slate-700 border-slate-200' : ''}
                    `}
                  >
                    <TrendingUp className="w-3 h-3 mr-1" />
                    {asset.viralityScore}
                  </Badge>
                  <span className="text-xs text-slate-500">~2 min read</span>
                </div>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="max-w-3xl mx-auto">
        <Card className="p-6 bg-slate-900 border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <h5 className="text-white mb-1">Ready to launch?</h5>
              <p className="text-sm text-slate-400">Create all assets as a project or export the plan</p>
            </div>
            <div className="flex gap-3">
              <Button variant="outline" className="border-slate-600 text-white hover:bg-slate-800">
                <Download className="w-4 h-4 mr-2" />
                Export Plan
              </Button>
              <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white">
                <FolderPlus className="w-4 h-4 mr-2" />
                Create All Assets in Projects
              </Button>
            </div>
          </div>
        </Card>
      </div>

      {/* Stats */}
      <div className="max-w-3xl mx-auto grid grid-cols-3 gap-4">
        <Card className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200 text-center">
          <p className="text-purple-900">6</p>
          <p className="text-sm text-purple-700 mt-1">Assets Created</p>
        </Card>
        <Card className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200 text-center">
          <p className="text-blue-900">5</p>
          <p className="text-sm text-blue-700 mt-1">Channels Covered</p>
        </Card>
        <Card className="p-4 bg-gradient-to-br from-green-50 to-green-100 border-green-200 text-center">
          <p className="text-green-900">~15 min</p>
          <p className="text-sm text-green-700 mt-1">Time Saved</p>
        </Card>
      </div>
    </div>
  );
}
