import { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { FileText, Mail, MessageSquare, Zap, Loader2, Check } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/lib/apiClient';
import type { GenerateBlogResponse, GenerateNewsletterResponse, GenerateSocialPostResponse } from '@/lib/types';

type ContentType = 'blog' | 'newsletter' | 'linkedin' | 'twitter' | 'facebook';

export function WrittenStudio() {
  const [contentType, setContentType] = useState<ContentType>('blog');
  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('');
  const [tone, setTone] = useState('professional');
  const [generating, setGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState<any>(null);

  const handleGenerate = async () => {
    if (!topic.trim()) {
      toast.error('Please enter a topic');
      return;
    }

    try {
      setGenerating(true);
      setGeneratedContent(null);

      let result;

      switch (contentType) {
        case 'blog': {
          result = await apiClient.content.generateBlog({
            topic,
            style_profile: {
              tone,
              voice: audience || undefined,
              length: 'medium',
            },
          });
          toast.success('Blog post generated!', {
            description: `${result.word_count} words`,
          });
          break;
        }

        case 'newsletter': {
          result = await apiClient.content.generateNewsletter({
            subject: topic,
            topics: [topic],
            tone,
          });
          toast.success('Newsletter generated!', {
            description: `${result.word_count} words`,
          });
          break;
        }

        case 'linkedin':
        case 'twitter':
        case 'facebook': {
          result = await apiClient.content.generatePost({
            topic,
            platforms: [contentType],
            include_hooks: true,
          });
          toast.success('Social post generated!', {
            description: `${result.posts.length} post${result.posts.length !== 1 ? 's' : ''}`,
          });
          break;
        }

        default:
          throw new Error('Unsupported content type');
      }

      setGeneratedContent(result);
    } catch (error: any) {
      console.error('Failed to generate content:', error);
      toast.error('Failed to generate content', {
        description: error.detail || error.message || 'Please try again',
      });
    } finally {
      setGenerating(false);
    }
  };

  const renderGeneratedContent = () => {
    if (!generatedContent) {
      return (
        <div className="p-4 bg-white rounded-lg border border-slate-200 text-center">
          <p className="text-sm text-slate-500">
            Your generated content will appear here
          </p>
        </div>
      );
    }

    // Blog post
    if ('title' in generatedContent && 'content' in generatedContent) {
      return (
        <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-3">
          <h5 className="text-slate-900 font-semibold">{generatedContent.title}</h5>
          <div className="text-sm text-slate-700 leading-relaxed line-clamp-6">
            {generatedContent.content.substring(0, 400)}...
          </div>
          <div className="flex items-center justify-between pt-2 border-t border-slate-100">
            <p className="text-xs text-slate-500">{generatedContent.word_count} words</p>
            <Badge variant="secondary" className="bg-green-50 text-green-700">
              <Check className="w-3 h-3 mr-1" />
              Generated
            </Badge>
          </div>
        </div>
      );
    }

    // Newsletter
    if ('subject' in generatedContent && 'sections' in generatedContent) {
      return (
        <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-3">
          <h5 className="text-slate-900 font-semibold">{generatedContent.subject}</h5>
          <p className="text-sm text-slate-600">{generatedContent.preview_text}</p>
          <div className="space-y-2">
            {generatedContent.sections.slice(0, 2).map((section: any, idx: number) => (
              <div key={idx} className="text-xs text-slate-600">
                • {section.heading}
              </div>
            ))}
          </div>
          <div className="flex items-center justify-between pt-2 border-t border-slate-100">
            <p className="text-xs text-slate-500">{generatedContent.word_count} words</p>
            <Badge variant="secondary" className="bg-green-50 text-green-700">
              <Check className="w-3 h-3 mr-1" />
              Generated
            </Badge>
          </div>
        </div>
      );
    }

    // Social posts
    if ('posts' in generatedContent) {
      const firstPost = generatedContent.posts[0];
      return (
        <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-3">
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="capitalize">
              {firstPost.platform}
            </Badge>
            <p className="text-xs text-slate-500">{firstPost.character_count} chars</p>
          </div>
          <p className="text-sm text-slate-700 leading-relaxed">
            {firstPost.content}
          </p>
          {firstPost.hashtags && firstPost.hashtags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {firstPost.hashtags.map((tag: string, idx: number) => (
                <span key={idx} className="text-xs text-blue-600">
                  #{tag}
                </span>
              ))}
            </div>
          )}
          <div className="pt-2 border-t border-slate-100">
            <Badge variant="secondary" className="bg-green-50 text-green-700">
              <Check className="w-3 h-3 mr-1" />
              Generated
            </Badge>
          </div>
        </div>
      );
    }

    return null;
  };

  const contentItems = [
    { title: 'The Future of AI in Content Creation', type: 'Blog', status: 'Published', edited: '2 hours ago' },
    { title: 'Weekly Newsletter #45', type: 'Newsletter', status: 'Draft', edited: '5 hours ago' },
    { title: '10 Tips for Viral LinkedIn Posts', type: 'LinkedIn Post', status: 'Published', edited: '1 day ago' },
    { title: 'Product Launch Thread', type: 'Thread', status: 'Draft', edited: '2 days ago' },
    { title: 'Community Update Email', type: 'Email', status: 'Published', edited: '3 days ago' },
  ];

  return (
    <div className="p-8">
      <div className="grid grid-cols-3 gap-8">
        {/* Left Column - Content List */}
        <div className="col-span-2 space-y-6">
          <Tabs defaultValue="blogs" className="w-full">
            <TabsList className="bg-slate-100 p-1">
              <TabsTrigger value="blogs">Blogs</TabsTrigger>
              <TabsTrigger value="newsletters">Newsletters</TabsTrigger>
              <TabsTrigger value="social">Social Posts</TabsTrigger>
              <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
            </TabsList>

            <TabsContent value="blogs" className="mt-6">
              <div className="space-y-3">
                {contentItems.map((item, index) => (
                  <Card
                    key={index}
                    className="p-5 bg-white border-slate-200 hover:border-slate-300 hover:shadow-md transition-all cursor-pointer"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-blue-50 rounded-lg">
                            {item.type === 'Blog' && <FileText className="w-4 h-4 text-blue-600" />}
                            {item.type === 'Newsletter' && <Mail className="w-4 h-4 text-purple-600" />}
                            {(item.type === 'LinkedIn Post' || item.type === 'Thread') && <MessageSquare className="w-4 h-4 text-green-600" />}
                            {item.type === 'Email' && <Mail className="w-4 h-4 text-orange-600" />}
                          </div>
                          <div className="flex-1">
                            <h5 className="text-slate-900">{item.title}</h5>
                            <p className="text-sm text-slate-500 mt-1">{item.type} • {item.edited}</p>
                          </div>
                        </div>
                      </div>
                      <Badge
                        variant="secondary"
                        className={item.status === 'Published' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-slate-100 text-slate-700'}
                      >
                        {item.status}
                      </Badge>
                    </div>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="newsletters" className="mt-6">
              <p className="text-slate-500 text-center py-12">Newsletter content items will appear here</p>
            </TabsContent>

            <TabsContent value="social" className="mt-6">
              <p className="text-slate-500 text-center py-12">Social post content items will appear here</p>
            </TabsContent>

            <TabsContent value="campaigns" className="mt-6">
              <p className="text-slate-500 text-center py-12">Campaign content items will appear here</p>
            </TabsContent>
          </Tabs>
        </div>

        {/* Right Column - Create New */}
        <div className="space-y-6">
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-6">
              <Zap className="w-5 h-5 text-blue-600" />
              <h4 className="text-slate-900">Create New Content</h4>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="content-type" className="text-sm text-slate-700">Content Type</Label>
                <Select value={contentType} onValueChange={(val) => setContentType(val as ContentType)}>
                  <SelectTrigger id="content-type" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="blog">Blog Post</SelectItem>
                    <SelectItem value="newsletter">Newsletter</SelectItem>
                    <SelectItem value="linkedin">LinkedIn Post</SelectItem>
                    <SelectItem value="twitter">Twitter Post</SelectItem>
                    <SelectItem value="facebook">Facebook Post</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="topic" className="text-sm text-slate-700">Topic</Label>
                <Input
                  id="topic"
                  placeholder="What do you want to write about?"
                  className="mt-1.5"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="audience" className="text-sm text-slate-700">Target Audience (Optional)</Label>
                <Input
                  id="audience"
                  placeholder="e.g., Tech entrepreneurs, Marketers..."
                  className="mt-1.5"
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="tone" className="text-sm text-slate-700">Tone</Label>
                <Select value={tone} onValueChange={setTone}>
                  <SelectTrigger id="tone" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="professional">Professional</SelectItem>
                    <SelectItem value="casual">Casual</SelectItem>
                    <SelectItem value="enthusiastic">Enthusiastic</SelectItem>
                    <SelectItem value="educational">Educational</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                className="w-full bg-slate-900 hover:bg-slate-800 mt-2"
                onClick={handleGenerate}
                disabled={generating}
              >
                {generating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  'Generate Draft'
                )}
              </Button>
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-slate-50 to-blue-50 border-slate-200">
            <h5 className="text-slate-900 mb-3">Generated Preview</h5>
            {renderGeneratedContent()}
          </Card>
        </div>
      </div>
    </div>
  );
}
