import { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { Play, Music, Copy, Loader2, Check, ExternalLink } from 'lucide-react';
import { Badge } from './ui/badge';
import { toast } from 'sonner';
import apiClient from '@/lib/apiClient';
import type { GenerateTrackRequest, GenerateTrackResponse } from '@/lib/types';

export function MusicStudio() {
  const [genre, setGenre] = useState('trap');
  const [mood, setMood] = useState('energetic');
  const [tempoBpm, setTempoBpm] = useState<string>('');
  const [referenceText, setReferenceText] = useState('');
  const [generating, setGenerating] = useState(false);
  const [song, setSong] = useState<GenerateTrackResponse | null>(null);

  const handleGenerate = async () => {
    if (!genre || !mood) {
      toast.error('Please select genre and mood');
      return;
    }

    try {
      setGenerating(true);

      const request: GenerateTrackRequest = {
        genre,
        mood,
        tempo_bpm: tempoBpm ? parseInt(tempoBpm) : undefined,
        reference_text: referenceText || undefined,
      };

      const result = await apiClient.music.generateTrack(request);
      setSong(result);

      toast.success('Song generated!', {
        description: `"${result.title}" is ready`,
      });
    } catch (error: any) {
      console.error('Failed to generate song:', error);
      toast.error('Failed to generate song', {
        description: error.detail || error.message || 'Please try again',
      });
    } finally {
      setGenerating(false);
    }
  };

  const copyAllLyrics = () => {
    if (!song) return;

    const allLyrics = song.sections
      .map((section) => `[${section.name}]\n${section.lyrics}`)
      .join('\n\n');

    navigator.clipboard.writeText(allLyrics);
    toast.success('Lyrics copied to clipboard');
  };

  const playDemo = () => {
    if (!song) return;
    window.open(song.fake_audio_url, '_blank');
    toast.info('Audio playback not yet implemented', {
      description: 'Real audio engine coming soon',
    });
  };

  return (
    <div className="p-8">
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column - Track Settings */}
        <div className="space-y-6">
          <Card className="p-6 bg-white border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-6">
              <Music className="w-5 h-5 text-blue-600" />
              <h4 className="text-slate-900">Track Settings</h4>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="genre" className="text-sm text-slate-700">Genre *</Label>
                <Select value={genre} onValueChange={setGenre}>
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
                <Label htmlFor="mood" className="text-sm text-slate-700">Mood *</Label>
                <Select value={mood} onValueChange={setMood}>
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

              <div>
                <Label htmlFor="tempo" className="text-sm text-slate-700">
                  Tempo (BPM) <span className="text-slate-500">- Optional</span>
                </Label>
                <Input
                  id="tempo"
                  type="number"
                  min="60"
                  max="200"
                  placeholder="e.g., 128"
                  className="mt-1.5"
                  value={tempoBpm}
                  onChange={(e) => setTempoBpm(e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="reference" className="text-sm text-slate-700">
                  Describe your song <span className="text-slate-500">- Optional</span>
                </Label>
                <Textarea
                  id="reference"
                  placeholder="e.g., Something like a chilled night drive through neon-lit streets..."
                  className="mt-1.5 min-h-[100px] resize-none"
                  value={referenceText}
                  onChange={(e) => setReferenceText(e.target.value)}
                />
              </div>

              <Button
                className="w-full bg-slate-900 hover:bg-slate-800 mt-2"
                onClick={handleGenerate}
                disabled={generating}
              >
                {generating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating Song...
                  </>
                ) : (
                  <>
                    <Music className="w-4 h-4 mr-2" />
                    Generate Song
                  </>
                )}
              </Button>
            </div>
          </Card>

          {song && (
            <Card className="p-5 bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
              <h5 className="text-slate-900 mb-2 font-medium">Song Info</h5>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Track ID:</span>
                  <code className="text-xs bg-white px-2 py-1 rounded">{song.track_id}</code>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Genre:</span>
                  <Badge variant="secondary" className="capitalize">{song.genre}</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Mood:</span>
                  <Badge variant="secondary" className="capitalize">{song.mood}</Badge>
                </div>
                {song.tempo_bpm && (
                  <div className="flex items-center justify-between">
                    <span className="text-slate-600">Tempo:</span>
                    <span className="font-medium">{song.tempo_bpm} BPM</span>
                  </div>
                )}
                <div className="pt-2 border-t border-purple-200">
                  <p className="text-xs text-purple-900">
                    Audio is placeholder for now – real audio engine coming soon.
                  </p>
                </div>
              </div>
            </Card>
          )}
        </div>

        {/* Right Column - Song Blueprint */}
        <div className="space-y-6">
          {!song ? (
            <Card className="p-12 bg-white border-slate-200 shadow-sm text-center">
              <Music className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <h5 className="text-slate-900 mb-2">No song generated yet</h5>
              <p className="text-sm text-slate-600">
                Configure your settings and click "Generate Song" to create a full song blueprint with lyrics
              </p>
            </Card>
          ) : (
            <>
              <Card className="p-6 bg-white border-slate-200 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="text-slate-900 font-semibold">{song.title}</h4>
                    <p className="text-sm text-slate-600 mt-1">
                      {song.vocal_style.gender.charAt(0).toUpperCase() + song.vocal_style.gender.slice(1)} vocals •{' '}
                      {song.vocal_style.tone} •{' '}
                      {song.vocal_style.energy} energy
                    </p>
                  </div>
                  <Badge className="bg-green-50 text-green-700">
                    <Check className="w-3 h-3 mr-1" />
                    Generated
                  </Badge>
                </div>

                <div className="space-y-4">
                  {/* Hook */}
                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <Label className="text-xs text-blue-900 font-semibold uppercase">Hook</Label>
                    <p className="text-sm text-slate-900 mt-1 italic">{song.hook}</p>
                  </div>

                  {/* Chorus */}
                  <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                    <Label className="text-xs text-purple-900 font-semibold uppercase">Chorus</Label>
                    <p className="text-sm text-slate-900 mt-1 whitespace-pre-wrap">{song.chorus}</p>
                  </div>
                </div>

                <div className="flex gap-2 mt-6">
                  <Button
                    variant="outline"
                    className="flex-1"
                    onClick={playDemo}
                  >
                    <Play className="w-4 h-4 mr-2" />
                    Play Demo
                  </Button>
                  <Button
                    variant="outline"
                    className="flex-1"
                    onClick={copyAllLyrics}
                  >
                    <Copy className="w-4 h-4 mr-2" />
                    Copy Lyrics
                  </Button>
                </div>
              </Card>

              {/* Song Structure */}
              <Card className="p-6 bg-white border-slate-200 shadow-sm">
                <h5 className="text-slate-900 mb-4 font-medium">Song Structure</h5>
                <div className="space-y-4 max-h-[600px] overflow-y-auto">
                  {song.sections.map((section, idx) => (
                    <div key={idx} className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                      <div className="flex items-center justify-between mb-2">
                        <h6 className="text-slate-900 font-medium">{section.name}</h6>
                        <Badge variant="secondary" className="text-xs">
                          {section.bars} bars
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-600 mb-3">{section.description}</p>
                      <div className="p-3 bg-white rounded border border-slate-200">
                        <p className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">
                          {section.lyrics}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
