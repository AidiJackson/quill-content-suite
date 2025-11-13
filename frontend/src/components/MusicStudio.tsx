import { Card } from './ui/card';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Textarea } from './ui/textarea';
import { Slider } from './ui/slider';
import { Play, Download, Upload, Layers, Mic, Music } from 'lucide-react';
import { Badge } from './ui/badge';

export function MusicStudio() {
  return (
    <div className="p-8 space-y-8">
      {/* AI Music Playground */}
      <div>
        <h4 className="text-slate-900 mb-6">AI Music Playground</h4>
        
        <div className="grid grid-cols-3 gap-8">
          {/* Left - Controls */}
          <div className="col-span-2 space-y-6">
            <Card className="p-6 bg-white border-slate-200 shadow-sm">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="genre" className="text-sm text-slate-700">Genre</Label>
                  <Select defaultValue="trap">
                    <SelectTrigger id="genre" className="mt-1.5">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="trap">Trap</SelectItem>
                      <SelectItem value="drill">Drill</SelectItem>
                      <SelectItem value="afrobeat">Afrobeat</SelectItem>
                      <SelectItem value="lofi">Lo-fi</SelectItem>
                      <SelectItem value="pop">Pop</SelectItem>
                      <SelectItem value="edm">EDM</SelectItem>
                      <SelectItem value="rnb">R&B</SelectItem>
                      <SelectItem value="hiphop">Hip Hop</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="mood" className="text-sm text-slate-700">Mood</Label>
                  <Select defaultValue="energetic">
                    <SelectTrigger id="mood" className="mt-1.5">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dark">Dark</SelectItem>
                      <SelectItem value="energetic">Energetic</SelectItem>
                      <SelectItem value="emotional">Emotional</SelectItem>
                      <SelectItem value="dreamy">Dreamy</SelectItem>
                      <SelectItem value="uplifting">Uplifting</SelectItem>
                      <SelectItem value="chill">Chill</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="col-span-2">
                  <Label className="text-sm text-slate-700 mb-2 block">Upload Sample/Loop (Optional)</Label>
                  <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-slate-400 transition-colors cursor-pointer">
                    <Upload className="w-8 h-8 mx-auto text-slate-400 mb-2" />
                    <p className="text-sm text-slate-600">Click to upload or drag & drop</p>
                    <p className="text-xs text-slate-500 mt-1">MP3, WAV up to 10MB</p>
                  </div>
                </div>

                <div>
                  <Label className="text-sm text-slate-700 mb-3 block">Tempo (BPM)</Label>
                  <div className="px-2">
                    <Slider defaultValue={[128]} min={60} max={180} step={1} />
                    <div className="flex justify-between mt-2">
                      <span className="text-xs text-slate-500">60</span>
                      <span className="text-sm text-slate-900">128 BPM</span>
                      <span className="text-xs text-slate-500">180</span>
                    </div>
                  </div>
                </div>

                <div>
                  <Label className="text-sm text-slate-700 mb-3 block">Intensity</Label>
                  <div className="px-2">
                    <Slider defaultValue={[75]} min={0} max={100} step={1} />
                    <div className="flex justify-between mt-2">
                      <span className="text-xs text-slate-500">Low</span>
                      <span className="text-sm text-slate-900">75%</span>
                      <span className="text-xs text-slate-500">High</span>
                    </div>
                  </div>
                </div>
              </div>

              <Button className="w-full mt-6 bg-slate-900 hover:bg-slate-800">
                <Music className="w-4 h-4 mr-2" />
                Generate Track
              </Button>
            </Card>
          </div>

          {/* Right - Output Preview */}
          <div>
            <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Music className="w-5 h-5 text-purple-600" />
                <h5 className="text-slate-900">Generated Track</h5>
              </div>

              <div className="p-4 bg-white rounded-lg mb-4">
                <p className="text-sm text-slate-900 mb-1">Untitled Track 001</p>
                <div className="flex items-center gap-2 text-xs text-slate-600">
                  <Badge variant="secondary" className="bg-purple-100 text-purple-700">Trap</Badge>
                  <span>•</span>
                  <span>3:24</span>
                </div>
              </div>

              <div className="space-y-2">
                <Button variant="outline" className="w-full">
                  <Play className="w-4 h-4 mr-2" />
                  Play Preview
                </Button>
                <Button variant="outline" className="w-full">
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </Button>
                <Button variant="outline" className="w-full">
                  <Layers className="w-4 h-4 mr-2" />
                  View Stems
                </Button>
              </div>
            </Card>

            <Card className="p-5 bg-blue-50 border-blue-200 mt-4">
              <p className="text-xs text-blue-900">
                <strong>Pro Tip:</strong> Upload a sample loop to guide the AI's creative direction and maintain your signature sound.
              </p>
            </Card>
          </div>
        </div>
      </div>

      {/* Lyrics & Vocals Studio */}
      <div>
        <h4 className="text-slate-900 mb-6">Lyrics & Vocals Studio</h4>

        <div className="grid grid-cols-2 gap-8">
          {/* Left - Lyrics */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <Music className="w-5 h-5 text-blue-600" />
              <h5 className="text-slate-900">Lyrics Generation</h5>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="lyrics-input" className="text-sm text-slate-700">Song Concept or Starting Lyric</Label>
                <Textarea
                  id="lyrics-input"
                  placeholder="Describe your song or paste a starting lyric..."
                  className="mt-2 min-h-[200px] resize-none"
                  defaultValue="A song about chasing dreams in the city lights, overcoming struggles, and staying true to yourself..."
                />
              </div>

              <Button className="w-full bg-slate-900 hover:bg-slate-800">
                Generate Full Lyrics
              </Button>
            </div>

            <div className="mt-6 pt-6 border-t border-slate-200">
              <h6 className="text-sm text-slate-700 mb-3">Alternative Hooks</h6>
              <div className="space-y-2">
                {[
                  'City lights, they shine so bright, chasing dreams into the night',
                  'From the bottom to the top, never gonna let it stop',
                  'Breaking through the darkness, finding my own way',
                ].map((hook, index) => (
                  <div key={index} className="p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer">
                    <p className="text-sm text-slate-700">{hook}</p>
                  </div>
                ))}
              </div>
            </div>
          </Card>

          {/* Right - Vocals */}
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <Mic className="w-5 h-5 text-purple-600" />
              <h5 className="text-slate-900">Vocal Generation</h5>
            </div>

            <div className="space-y-6">
              <div>
                <Label htmlFor="voice-type" className="text-sm text-slate-700">Voice Type</Label>
                <Select defaultValue="male-rnb">
                  <SelectTrigger id="voice-type" className="mt-1.5">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="male-rnb">Male R&B</SelectItem>
                    <SelectItem value="female-pop">Female Pop</SelectItem>
                    <SelectItem value="male-rap">Male Rap</SelectItem>
                    <SelectItem value="female-rap">Female Rap</SelectItem>
                    <SelectItem value="soft-male">Soft Male</SelectItem>
                    <SelectItem value="soft-female">Soft Female</SelectItem>
                    <SelectItem value="choir">Choir</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label className="text-sm text-slate-700 mb-3 block">Emotion</Label>
                <div className="px-2">
                  <Slider defaultValue={[60]} min={0} max={100} step={1} />
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-slate-500">Calm</span>
                    <span className="text-sm text-slate-900">Balanced</span>
                    <span className="text-xs text-slate-500">Intense</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-sm text-slate-700 mb-3 block">Pitch</Label>
                <div className="px-2">
                  <Slider defaultValue={[50]} min={0} max={100} step={1} />
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-slate-500">Low</span>
                    <span className="text-sm text-slate-900">Natural</span>
                    <span className="text-xs text-slate-500">High</span>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-sm text-slate-700 mb-3 block">Energy</Label>
                <div className="px-2">
                  <Slider defaultValue={[70]} min={0} max={100} step={1} />
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-slate-500">Mellow</span>
                    <span className="text-sm text-slate-900">Energetic</span>
                    <span className="text-xs text-slate-500">Max</span>
                  </div>
                </div>
              </div>

              <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
                <Mic className="w-4 h-4 mr-2" />
                Generate Vocal
              </Button>

              <div className="pt-4 border-t border-slate-200">
                <p className="text-sm text-slate-700 mb-2">Output Options:</p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary" className="bg-purple-50 text-purple-700">Acapella</Badge>
                  <Badge variant="secondary" className="bg-purple-50 text-purple-700">Harmonies</Badge>
                  <Badge variant="secondary" className="bg-purple-50 text-purple-700">Backing Vocals</Badge>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
