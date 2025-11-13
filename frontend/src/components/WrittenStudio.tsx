import { Card } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { FileText, Mail, MessageSquare, Zap } from 'lucide-react';

export function WrittenStudio() {
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
                <Select defaultValue="blog">
                  <SelectTrigger id="content-type" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="blog">Blog Post</SelectItem>
                    <SelectItem value="newsletter">Newsletter</SelectItem>
                    <SelectItem value="linkedin">LinkedIn Post</SelectItem>
                    <SelectItem value="thread">Twitter Thread</SelectItem>
                    <SelectItem value="email">Email Campaign</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="topic" className="text-sm text-slate-700">Topic</Label>
                <Input 
                  id="topic"
                  placeholder="What do you want to write about?"
                  className="mt-1.5"
                />
              </div>

              <div>
                <Label htmlFor="audience" className="text-sm text-slate-700">Target Audience</Label>
                <Input 
                  id="audience"
                  placeholder="e.g., Tech entrepreneurs, Marketers..."
                  className="mt-1.5"
                />
              </div>

              <div>
                <Label htmlFor="tone" className="text-sm text-slate-700">Tone</Label>
                <Select defaultValue="professional">
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

              <Button className="w-full bg-slate-900 hover:bg-slate-800 mt-2">
                Generate Draft
              </Button>
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-slate-50 to-blue-50 border-slate-200">
            <h5 className="text-slate-900 mb-3">Preview Example</h5>
            <div className="p-4 bg-white rounded-lg border border-slate-200">
              <p className="text-sm text-slate-700 leading-relaxed">
                "The future of content creation is here. AI-powered tools are transforming how we write, edit, and publish..."
              </p>
              <p className="text-xs text-slate-500 mt-3">Generated preview • 324 words</p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
