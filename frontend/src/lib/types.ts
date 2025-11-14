/**
 * TypeScript types for API requests and responses
 * Based on API_REFERENCE.md and backend Pydantic models
 */

// ==================== Project Types ====================
export interface Project {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectRequest {
  user_id: string;
  title: string;
  description?: string;
}

export interface UpdateProjectRequest {
  title?: string;
  description?: string;
}

// ==================== Content Types ====================
export interface ContentItem {
  id: string;
  project_id: string;
  type: 'blog' | 'newsletter' | 'post' | 'outline' | 'campaign' | 'hooks';
  title: string;
  content: string;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface StyleProfile {
  tone?: string;
  voice?: string;
  length?: 'short' | 'medium' | 'long';
}

export interface GenerateBlogRequest {
  topic: string;
  style_profile?: StyleProfile;
  keywords?: string[];
  project_id?: string;
}

export interface GenerateBlogResponse {
  title: string;
  content: string;
  word_count: number;
  metadata: Record<string, any>;
  saved_item_id?: string;
}

export interface GenerateNewsletterRequest {
  subject: string;
  topics: string[];
  tone?: string;
  project_id?: string;
}

export interface NewsletterSection {
  heading: string;
  content: string;
}

export interface GenerateNewsletterResponse {
  subject: string;
  preview_text: string;
  sections: NewsletterSection[];
  cta: string;
  word_count: number;
  saved_item_id?: string;
}

export interface GenerateSocialPostRequest {
  topic: string;
  platforms: string[];
  include_hooks?: boolean;
  project_id?: string;
}

export interface SocialPost {
  platform: string;
  content: string;
  character_count: number;
  hashtags: string[];
}

export interface GenerateSocialPostResponse {
  posts: SocialPost[];
  saved_item_ids?: string[];
}

export interface GenerateOutlineRequest {
  topic: string;
  sections?: number;
  project_id?: string;
}

export interface GenerateOutlineResponse {
  topic: string;
  sections: string[];
  saved_item_id?: string;
}

export interface GenerateHooksRequest {
  topic: string;
  count?: number;
  platform?: string;
}

export interface GenerateHooksResponse {
  hooks: string[];
}

export interface GenerateCampaignRequest {
  goal: string;
  steps?: number;
  audience?: string;
  project_id?: string;
}

export interface CampaignStep {
  step_number: number;
  subject: string;
  content: string;
  delay_days: number;
}

export interface GenerateCampaignResponse {
  goal: string;
  audience: string;
  steps: CampaignStep[];
  total_duration_days: number;
  saved_item_id?: string;
}

export interface ExpandContentRequest {
  text: string;
  target_length?: string;
}

export interface ExpandContentResponse {
  original_length: number;
  expanded_length: number;
  content: string;
}

export interface ShortenContentRequest {
  text: string;
  target_length?: number;
}

export interface ShortenContentResponse {
  original_length: number;
  shortened_length: number;
  content: string;
}

export interface RewriteContentRequest {
  text: string;
  instructions: string;
}

export interface RewriteContentResponse {
  original: string;
  rewritten: string;
}

// ==================== Virality Types ====================
export interface ViralityScoreRequest {
  text: string;
  content_item_id?: string;
}

export interface ViralityScoreResponse {
  hook_score: number;
  structure_score: number;
  niche_score: number;
  overall_score: number;
  predicted_engagement: number;
  recommendations: string[];
  saved_score_id?: string;
}

export interface ViralityRewriteRequest {
  text: string;
  target_platform?: string;
}

export interface ViralityRewriteResponse {
  original_text: string;
  rewritten_text: string;
  original_score: number;
  improved_score: number;
  improvements: string[];
}

// ==================== Media Types ====================
export interface MediaFile {
  id: string;
  project_id: string;
  type: 'video' | 'audio' | 'image';
  url: string;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Video Processing
export interface TrimVideoRequest {
  input_url: string;
  start_time: number;
  end_time: number;
  project_id?: string;
}

export interface TrimVideoResponse {
  output_url: string;
  duration: number;
  saved_media_id?: string;
}

export interface GenerateCaptionsRequest {
  input_url: string;
}

export interface GenerateCaptionsResponse {
  srt_content: string;
  caption_count: number;
}

export interface ResizeVideoRequest {
  input_url: string;
  aspect_ratio: string;
  project_id?: string;
}

export interface ResizeVideoResponse {
  output_url: string;
  aspect_ratio: string;
  saved_media_id?: string;
}

export interface GenerateShortsRequest {
  input_url: string;
  count?: number;
  project_id?: string;
}

export interface VideoClip {
  url: string;
  start_time: number;
  duration: number;
  score: number;
}

export interface GenerateShortsResponse {
  clips: VideoClip[];
  saved_media_ids?: string[];
}

// Audio Processing
export interface CleanupAudioRequest {
  input_url: string;
  project_id?: string;
}

export interface CleanupAudioResponse {
  output_url: string;
  saved_media_id?: string;
}

export interface PitchShiftRequest {
  input_url: string;
  semitones: number;
  project_id?: string;
}

export interface PitchShiftResponse {
  output_url: string;
  semitones: number;
  saved_media_id?: string;
}

export interface TempoShiftRequest {
  input_url: string;
  percent: number;
  project_id?: string;
}

export interface TempoShiftResponse {
  output_url: string;
  tempo_percent: number;
  saved_media_id?: string;
}

export interface ExtractAudioRequest {
  input_url: string;
  project_id?: string;
}

export interface ExtractAudioResponse {
  output_url: string;
  duration: number;
  saved_media_id?: string;
}

// ==================== Dashboard Types ====================
export interface DashboardSummary {
  active_projects: number;
  items_created_this_week: number;
  avg_virality_score: number;
  video_clips_generated: number;
  tracks_in_production: number;
}

// ==================== Music Studio Types (Stub) ====================
export interface GenerateTrackRequest {
  prompt?: string;
  genre?: string;
  duration?: number;
  project_id?: string;
}

export interface GenerateTrackResponse {
  track_url: string;
  duration: number;
  metadata: Record<string, any>;
  saved_media_id?: string;
}

// ==================== AI Video Types (Stub) ====================
export interface GenerateAIVideoRequest {
  prompt: string;
  style?: string;
  duration?: number;
  project_id?: string;
}

export interface GenerateAIVideoResponse {
  video_url: string;
  duration: number;
  metadata: Record<string, any>;
  saved_media_id?: string;
}

// ==================== Health Types ====================
export interface HealthResponse {
  status: string;
  app_name: string;
  environment: string;
}

// ==================== Error Types ====================
export interface APIError {
  detail: string | Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}
