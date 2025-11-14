import { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { TrendingUp, Sparkles, Clock, Target, Loader2 } from 'lucide-react';
import { Progress } from './ui/progress';
import { toast } from 'sonner';
import apiClient from '@/lib/apiClient';
import type { ViralityScoreResponse, ViralityRewriteResponse, GenerateHooksResponse } from '@/lib/types';

export function ViralityLab() {
  const [contentText, setContentText] = useState(
    `The future of work is not what we expected. After managing remote teams for 3 years, I've learned that productivity isn't about hours logged—it's about outcomes delivered.

Here's what actually moves the needle:
• Clear goals over constant check-ins
• Async communication over endless meetings
• Trust over surveillance

Last quarter, our team hit 127% of targets while working 20% fewer hours. The secret? We stopped measuring time and started measuring impact.`
  );
  const [platform, setPlatform] = useState('linkedin');
  const [analyzing, setAnalyzing] = useState(false);
  const [rewriting, setRewriting] = useState(false);
  const [generatingHooks, setGeneratingHooks] = useState(false);

  const [score, setScore] = useState<ViralityScoreResponse | null>(null);
  const [rewrittenContent, setRewrittenContent] = useState<ViralityRewriteResponse | null>(null);
  const [hooks, setHooks] = useState<string[] | null>(null);

  const handleAnalyze = async () => {
    if (!contentText.trim()) {
      toast.error('Please enter content to analyze');
      return;
    }

    try {
      setAnalyzing(true);
      const result = await apiClient.virality.score({ text: contentText });
      setScore(result);
      toast.success('Content analyzed!', {
        description: `Overall score: ${result.overall_score}/100`,
      });
    } catch (error: any) {
      console.error('Failed to analyze content:', error);
      toast.error('Failed to analyze content', {
        description: error.detail || error.message || 'Please try again',
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const handleRewrite = async () => {
    if (!contentText.trim()) {
      toast.error('Please enter content to rewrite');
      return;
    }

    try {
      setRewriting(true);
      const result = await apiClient.virality.rewrite({
        text: contentText,
        target_platform: platform,
      });
      setRewrittenContent(result);
      toast.success('Content rewritten!', {
        description: `Score improved from ${result.original_score} to ${result.improved_score}`,
      });
    } catch (error: any) {
      console.error('Failed to rewrite content:', error);
      toast.error('Failed to rewrite content', {
        description: error.detail || error.message || 'Please try again',
      });
    } finally {
      setRewriting(false);
    }
  };

  const handleGenerateHooks = async () => {
    if (!contentText.trim()) {
      toast.error('Please enter content context for hooks');
      return;
    }

    try {
      setGeneratingHooks(true);
      const result = await apiClient.content.generateHooks({
        topic: contentText.split('\n')[0], // Use first line as topic
        count: 5,
        platform,
      });
      setHooks(result.hooks);
      toast.success('Hooks generated!', {
        description: `${result.hooks.length} alternative hooks`,
      });
    } catch (error: any) {
      console.error('Failed to generate hooks:', error);
      toast.error('Failed to generate hooks', {
        description: error.detail || error.message || 'Please try again',
      });
    } finally {
      setGeneratingHooks(false);
    }
  };

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
              value={contentText}
              onChange={(e) => setContentText(e.target.value)}
            />

            <div className="mt-4 space-y-4">
              <div>
                <Label htmlFor="platform" className="text-sm text-slate-700">Platform</Label>
                <Select value={platform} onValueChange={setPlatform}>
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

              <Button
                className="w-full bg-slate-900 hover:bg-slate-800"
                onClick={handleAnalyze}
                disabled={analyzing}
              >
                {analyzing ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    Analyze & Score
                  </>
                )}
              </Button>
            </div>
          </Card>

          {/* Rewritten Content or Hooks Display */}
          {(rewrittenContent || hooks) && (
            <Card className="p-6 bg-gradient-to-br from-blue-50 to-purple-50 border-slate-200 shadow-sm">
              <h5 className="text-slate-900 mb-3">
                {rewrittenContent ? 'Rewritten Content' : 'Alternative Hooks'}
              </h5>
              {rewrittenContent && (
                <div className="p-4 bg-white rounded-lg border border-slate-200">
                  <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                    {rewrittenContent.rewritten_text}
                  </p>
                  <div className="flex gap-2 mt-3 pt-3 border-t border-slate-100">
                    <Badge variant="secondary" className="text-xs">
                      Original: {rewrittenContent.original_score}
                    </Badge>
                    <Badge className="text-xs bg-green-50 text-green-700">
                      Improved: {rewrittenContent.improved_score}
                    </Badge>
                  </div>
                </div>
              )}
              {hooks && (
                <div className="space-y-2">
                  {hooks.map((hook, idx) => (
                    <div key={idx} className="p-3 bg-white rounded-lg border border-slate-200">
                      <p className="text-sm text-slate-700">{hook}</p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )}
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
                    <div className="text-green-600">
                      {score ? score.overall_score : '—'}
                    </div>
                    <p className="text-xs text-slate-600">/ 100</p>
                  </div>
                </div>
              </div>
              {score && (
                <Badge className="mt-4 bg-green-600 text-white">
                  {score.overall_score >= 80 ? 'High Potential' : score.overall_score >= 60 ? 'Good' : 'Needs Work'}
                </Badge>
              )}
              {!score && (
                <p className="mt-4 text-sm text-slate-500">Analyze content to see score</p>
              )}
            </div>
          </Card>

          {/* Sub-scores */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <h5 className="text-slate-900 mb-4">Breakdown</h5>
            {score ? (
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-700">Hook Strength</span>
                    <span className="text-sm text-slate-900">{score.hook_score}/100</span>
                  </div>
                  <Progress value={score.hook_score} className="h-2" />
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-700">Structure</span>
                    <span className="text-sm text-slate-900">{score.structure_score}/100</span>
                  </div>
                  <Progress value={score.structure_score} className="h-2" />
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-slate-700">Niche Fit</span>
                    <span className="text-sm text-slate-900">{score.niche_score}/100</span>
                  </div>
                  <Progress value={score.niche_score} className="h-2" />
                </div>
                <div className="pt-3 border-t border-slate-100">
                  <p className="text-sm text-slate-700 mb-1">Predicted Engagement</p>
                  <p className="text-2xl font-semibold text-slate-900">{Math.round(score.predicted_engagement).toLocaleString()}</p>
                  <p className="text-xs text-slate-500">estimated interactions</p>
                </div>
              </div>
            ) : (
              <p className="text-sm text-slate-500 text-center py-8">
                No analysis yet
              </p>
            )}
          </Card>

          {/* Suggestions */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <h5 className="text-slate-900 mb-4">
              <Target className="w-5 h-5 inline mr-2 text-blue-600" />
              Suggestions
            </h5>
            {score && score.recommendations ? (
              <ul className="space-y-3 mb-6">
                {score.recommendations.map((suggestion, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2 flex-shrink-0"></div>
                    <span className="text-sm text-slate-700">{suggestion}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-500 mb-6">
                Analyze your content to get personalized suggestions
              </p>
            )}

            <div className="space-y-2">
              <Button
                className="w-full bg-slate-900 hover:bg-slate-800"
                onClick={handleRewrite}
                disabled={rewriting}
              >
                {rewriting ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Rewriting...
                  </>
                ) : (
                  'Rewrite for Max Virality'
                )}
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={handleGenerateHooks}
                disabled={generatingHooks}
              >
                {generatingHooks ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  'Generate 5 Alternative Hooks'
                )}
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
