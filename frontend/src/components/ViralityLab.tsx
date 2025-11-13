import { Card } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { TrendingUp, Sparkles, Clock, Target } from 'lucide-react';
import { Progress } from './ui/progress';

export function ViralityLab() {
  const subScores = [
    { label: 'Hook Strength', score: 94, color: 'green' },
    { label: 'Structure', score: 88, color: 'blue' },
    { label: 'Niche Fit', score: 91, color: 'purple' },
    { label: 'Timing', score: 76, color: 'orange' },
  ];

  const suggestions = [
    'Start with a stronger question in the first line',
    'Add specific numbers or statistics in paragraph 2',
    'Include a personal story or case study',
    'Break up long paragraphs for better readability',
    'End with a clear call-to-action',
  ];

  const trendInsights = [
    {
      title: 'AI & Automation',
      description: 'High engagement in tech circles',
      trend: '+28% this week',
    },
    {
      title: 'Short-form Video',
      description: 'Ideal format for current trends',
      trend: 'Peak time: 2-4 PM',
    },
    {
      title: 'Story-driven Posts',
      description: 'Personal narratives performing well',
      trend: '+41% engagement',
    },
  ];

  return (
    <div className="p-8">
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column - Input */}
        <div className="space-y-6">
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <Label htmlFor="content-input" className="text-sm text-slate-700">
              Content to Analyze
            </Label>
            <Textarea
              id="content-input"
              placeholder="Paste your content here..."
              className="mt-2 min-h-[300px] resize-none"
              defaultValue="The future of work is not what we expected. After managing remote teams for 3 years, I've learned that productivity isn't about hours logged—it's about outcomes delivered.

Here's what actually moves the needle:
• Clear goals over constant check-ins
• Async communication over endless meetings  
• Trust over surveillance

Last quarter, our team hit 127% of targets while working 20% fewer hours. The secret? We stopped measuring time and started measuring impact."
            />

            <div className="mt-4 space-y-4">
              <div>
                <Label htmlFor="platform" className="text-sm text-slate-700">Platform</Label>
                <Select defaultValue="linkedin">
                  <SelectTrigger id="platform" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="linkedin">LinkedIn</SelectItem>
                    <SelectItem value="twitter">X / Twitter</SelectItem>
                    <SelectItem value="tiktok">TikTok</SelectItem>
                    <SelectItem value="youtube">YouTube</SelectItem>
                    <SelectItem value="newsletter">Newsletter</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button className="w-full bg-slate-900 hover:bg-slate-800">
                <Sparkles className="w-4 h-4 mr-2" />
                Analyze & Score
              </Button>
            </div>
          </Card>
        </div>

        {/* Right Column - Results */}
        <div className="space-y-6">
          {/* Virality Score */}
          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-green-200 shadow-sm">
            <div className="text-center">
              <p className="text-sm text-slate-700 mb-2">Virality Score</p>
              <div className="relative inline-flex items-center justify-center">
                <div className="w-32 h-32 rounded-full bg-white shadow-md flex items-center justify-center border-4 border-green-500">
                  <div className="text-center">
                    <div className="text-green-600">87</div>
                    <p className="text-xs text-slate-600">/ 100</p>
                  </div>
                </div>
              </div>
              <Badge className="mt-4 bg-green-600 text-white">High Potential</Badge>
            </div>
          </Card>

          {/* Sub-scores */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <h5 className="text-slate-900 mb-4">Breakdown</h5>
            <div className="space-y-4">
              {subScores.map((item, index) => (
                <div key={index}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-700">{item.label}</span>
                    <span className="text-sm text-slate-900">{item.score}/100</span>
                  </div>
                  <Progress value={item.score} className="h-2" />
                </div>
              ))}
            </div>
          </Card>

          {/* Suggestions */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <h5 className="text-slate-900 mb-4">
              <Target className="w-5 h-5 inline mr-2 text-blue-600" />
              Suggestions
            </h5>
            <ul className="space-y-3">
              {suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2 flex-shrink-0"></div>
                  <span className="text-sm text-slate-700">{suggestion}</span>
                </li>
              ))}
            </ul>

            <div className="mt-6 space-y-2">
              <Button className="w-full bg-slate-900 hover:bg-slate-800">
                Rewrite for Max Virality
              </Button>
              <Button variant="outline" className="w-full">
                Generate 5 Alternative Hooks
              </Button>
            </div>
          </Card>
        </div>
      </div>

      {/* Trend Insights */}
      <div className="mt-8">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-blue-600" />
          <h4 className="text-slate-900">Trend Insights</h4>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {trendInsights.map((insight, index) => (
            <Card key={index} className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all">
              <h5 className="text-slate-900 mb-1">{insight.title}</h5>
              <p className="text-sm text-slate-600 mb-3">{insight.description}</p>
              <Badge variant="secondary" className="bg-blue-50 text-blue-700 text-xs">
                <Clock className="w-3 h-3 mr-1" />
                {insight.trend}
              </Badge>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
