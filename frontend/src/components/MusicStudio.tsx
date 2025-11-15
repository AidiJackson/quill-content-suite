import { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { Play, Music, Copy, Loader2, Check, ExternalLink, Mic } from 'lucide-react';
import { Badge } from './ui/badge';
import { toast } from 'sonner';
import apiClient from '@/lib/apiClient';
import type { GenerateTrackRequest, GenerateTrackResponse, GenerateVocalsResponse } from '@/lib/types';

export function MusicStudio() {
  const [selectedArtists, setSelectedArtists] = useState<string[]>(['Depeche Mode']);
  const [artistStyle, setArtistStyle] = useState<string>('');
  const [mood, setMood] = useState('');
  const [tempoBpm, setTempoBpm] = useState<string>('');
  const [referenceText, setReferenceText] = useState('');
  const [generating, setGenerating] = useState(false);
  const [song, setSong] = useState<GenerateTrackResponse | null>(null);
  const [vocalDemo, setVocalDemo] = useState<GenerateVocalsResponse | null>(null);
  const [generatingVocals, setGeneratingVocals] = useState(false);

  // Available artists (from backend database)
  const availableArtists = [
    'Depeche Mode',
    'Gary Numan',
    'Kraftwerk',
    'New Order',
    'Pet Shop Boys',
    'The Human League',
    'Orchestral Manoeuvres in the Dark',
    'Tears for Fears',
    'Eurythmics',
    'Yazoo',
  ];

  const toggleArtist = (artist: string) => {
    setSelectedArtists((prev) =>
      prev.includes(artist)
        ? prev.filter((a) => a !== artist)
        : [...prev, artist]
    );
  };

  const handleGenerate = async () => {
    if (selectedArtists.length === 0) {
      toast.error('Please select at least one artist influence');
      return;
    }

    try {
      setGenerating(true);

      const request: GenerateTrackRequest = {
        artist_influences: selectedArtists,
        artist_style: artistStyle || undefined,
        mood: mood || undefined,
        tempo_bpm: tempoBpm ? parseInt(tempoBpm) : undefined,
        reference_text: referenceText || undefined,
      };

      const result = await apiClient.music.generateTrack(request);
      setSong(result);
      setVocalDemo(null); // Clear previous vocal demo

      toast.success('Premium track generated!', {
        description: `"${result.title}" is ready`,
      });
    } catch (error: any) {
      console.error('Failed to generate track:', error);
      toast.error('Failed to generate track', {
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

  const handleGenerateVocals = async () => {
    if (!song) return;

    try {
      setGeneratingVocals(true);

      // Gather all lyrics from all sections
      const allLyrics = song.sections
        .map((section) => section.lyrics)
        .join('\n\n');

      const result = await apiClient.vocals.generate({
        track_id: song.track_id,
        lyrics: allLyrics,
        vocal_style: song.vocal_style,
        tempo_bpm: song.tempo_bpm,
      });

      setVocalDemo(result);

      toast.success('Vocals generated!', {
        description: 'Demo vocal rendering ready',
      });
    } catch (error: any) {
      console.error('Failed to generate vocals:', error);
      toast.error('Failed to generate vocals', {
        description: error.detail || error.message || 'Please try again',
      });
    } finally {
      setGeneratingVocals(false);
    }
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
                <Label className="text-sm text-slate-700">
                  Artist Influences * <span className="text-slate-500">(Select 1-3)</span>
                </Label>
                <div className="mt-2 flex flex-wrap gap-2">
                  {availableArtists.map((artist) => (
                    <Badge
                      key={artist}
                      variant={selectedArtists.includes(artist) ? 'default' : 'outline'}
                      className={`cursor-pointer transition-all ${
                        selectedArtists.includes(artist)
                          ? 'bg-purple-600 hover:bg-purple-700'
                          : 'hover:bg-slate-100'
                      }`}
                      onClick={() => toggleArtist(artist)}
                    >
                      {artist}
                    </Badge>
                  ))}
                </div>
                {selectedArtists.length > 0 && (
                  <p className="text-xs text-slate-500 mt-2">
                    Selected: {selectedArtists.join(', ')}
                  </p>
                )}
              </div>

              <div>
                <Label htmlFor="artist-style" className="text-sm text-slate-700">
                  Artist Style <span className="text-slate-500">- Optional (for distinct procedural sound)</span>
                </Label>
                <Select value={artistStyle} onValueChange={setArtistStyle}>
                  <SelectTrigger id="artist-style" className="mt-1.5">
                    <SelectValue placeholder="Auto-detect from artists" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="depeche_mode">Depeche Mode Style</SelectItem>
                    <SelectItem value="gary_numan">Gary Numan Style</SelectItem>
                    <SelectItem value="kraftwerk">Kraftwerk Style</SelectItem>
                    <SelectItem value="pet_shop_boys">Pet Shop Boys Style</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="mood" className="text-sm text-slate-700">
                  Mood <span className="text-slate-500">- Optional (auto-detected from artists)</span>
                </Label>
                <Select value={mood} onValueChange={setMood}>
                  <SelectTrigger id="mood" className="mt-1.5">
                    <SelectValue placeholder="Auto-detect from artists" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dark">Dark</SelectItem>
                    <SelectItem value="dystopian">Dystopian</SelectItem>
                    <SelectItem value="melancholic">Melancholic</SelectItem>
                    <SelectItem value="romantic">Romantic</SelectItem>
                    <SelectItem value="atmospheric">Atmospheric</SelectItem>
                    <SelectItem value="uplifting">Uplifting</SelectItem>
                    <SelectItem value="sophisticated">Sophisticated</SelectItem>
                    <SelectItem value="emotive">Emotive</SelectItem>
                    <SelectItem value="powerful">Powerful</SelectItem>
                    <SelectItem value="mechanical">Mechanical</SelectItem>
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
              <h5 className="text-slate-900 mb-2 font-medium">Premium Track Info</h5>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Track ID:</span>
                  <code className="text-xs bg-white px-2 py-1 rounded">{song.track_id}</code>
                </div>
                <div>
                  <span className="text-slate-600 block mb-1">Artists:</span>
                  <div className="flex flex-wrap gap-1">
                    {song.artist_influences.map((artist) => (
                      <Badge key={artist} variant="secondary" className="text-xs">
                        {artist}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Artist Style:</span>
                  <Badge variant="secondary" className="capitalize text-xs">
                    {song.artist_style.replace(/_/g, ' ')}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Mood:</span>
                  <Badge variant="secondary" className="capitalize">{song.mood}</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Era:</span>
                  <Badge variant="secondary" className="capitalize text-xs">
                    {song.production_era.replace(/_/g, ' ')}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-600">Tempo:</span>
                  <span className="font-medium">{song.tempo_bpm} BPM</span>
                </div>
                <div>
                  <span className="text-slate-600 block mb-1">Instruments:</span>
                  <div className="flex flex-wrap gap-1">
                    {song.instruments.slice(0, 4).map((inst) => (
                      <Badge key={inst} variant="outline" className="text-xs">
                        {inst.replace(/_/g, ' ')}
                      </Badge>
                    ))}
                    {song.instruments.length > 4 && (
                      <Badge variant="outline" className="text-xs">
                        +{song.instruments.length - 4} more
                      </Badge>
                    )}
                  </div>
                </div>
                <div className="pt-2 border-t border-purple-200">
                  <p className="text-xs text-purple-900">
                    ✨ Premium quality with authentic 808/909 synthesis, ADSR envelopes, and artist-specific characteristics.
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

                <Button
                  className="w-full bg-blue-600 hover:bg-blue-700 mt-3"
                  onClick={handleGenerateVocals}
                  disabled={generatingVocals}
                >
                  {generatingVocals ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Generating Vocals...
                    </>
                  ) : (
                    <>
                      <Mic className="w-4 h-4 mr-2" />
                      Generate Vocals
                    </>
                  )}
                </Button>
              </Card>

              {/* Vocal Demo Player */}
              {vocalDemo && (
                <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200 shadow-sm">
                  <div className="flex items-center gap-2 mb-4">
                    <Mic className="w-5 h-5 text-blue-600" />
                    <h5 className="text-slate-900 font-medium">Vocal Demo</h5>
                    <Badge className="bg-blue-100 text-blue-700 ml-auto">
                      <Check className="w-3 h-3 mr-1" />
                      Ready
                    </Badge>
                  </div>

                  <div className="space-y-4">
                    {/* Vocal Info */}
                    <div className="p-4 bg-white rounded-lg border border-blue-200">
                      <div className="grid grid-cols-2 gap-3 text-sm">
                        <div>
                          <span className="text-slate-600">Gender:</span>
                          <span className="ml-2 font-medium capitalize">{vocalDemo.vocal_style.gender}</span>
                        </div>
                        <div>
                          <span className="text-slate-600">Tone:</span>
                          <span className="ml-2 font-medium capitalize">{vocalDemo.vocal_style.tone}</span>
                        </div>
                        <div>
                          <span className="text-slate-600">Energy:</span>
                          <span className="ml-2 font-medium capitalize">{vocalDemo.vocal_style.energy}</span>
                        </div>
                        {vocalDemo.duration_seconds && (
                          <div>
                            <span className="text-slate-600">Duration:</span>
                            <span className="ml-2 font-medium">{vocalDemo.duration_seconds}s</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Audio Player */}
                    <div className="p-4 bg-white rounded-lg border border-blue-200">
                      <audio
                        controls
                        className="w-full"
                        src={vocalDemo.audio_url}
                      >
                        Your browser does not support the audio element.
                      </audio>
                    </div>

                    {/* Notes */}
                    {vocalDemo.notes && (
                      <div className="p-3 bg-blue-100 rounded text-xs text-blue-900">
                        {vocalDemo.notes}
                      </div>
                    )}
                  </div>
                </Card>
              )}

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
