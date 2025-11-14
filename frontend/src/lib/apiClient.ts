/**
 * API Client for Quillography Content Suite
 *
 * Provides typed fetch wrappers for all backend endpoints.
 * Handles authentication headers, JSON serialization, and error handling.
 */

import type * as T from './types';

// Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const DEFAULT_USER_ID = 'default-user'; // TODO: Replace with actual auth

/**
 * Custom error class for API errors
 */
export class APIClientError extends Error {
  constructor(
    public status: number,
    public detail: string | T.APIError['detail'],
    public url: string
  ) {
    super(typeof detail === 'string' ? detail : 'API Error');
    this.name = 'APIClientError';
  }
}

/**
 * Generic fetch wrapper with error handling
 */
async function apiRequest<TResponse>(
  endpoint: string,
  options: RequestInit = {}
): Promise<TResponse> {
  const url = `${API_BASE_URL}${endpoint}`;

  // Set default headers
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    'X-User-Id': DEFAULT_USER_ID,
    ...options.headers,
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle error responses
    if (!response.ok) {
      let errorDetail: string | T.APIError['detail'] = `HTTP ${response.status}`;

      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch {
        // If JSON parsing fails, use status text
        errorDetail = response.statusText || errorDetail;
      }

      throw new APIClientError(response.status, errorDetail, url);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return null as TResponse;
    }

    // Parse JSON response
    return await response.json();
  } catch (error) {
    if (error instanceof APIClientError) {
      throw error;
    }

    // Network or other errors
    throw new APIClientError(
      0,
      error instanceof Error ? error.message : 'Network error',
      url
    );
  }
}

/**
 * GET request helper
 */
async function get<TResponse>(endpoint: string): Promise<TResponse> {
  return apiRequest<TResponse>(endpoint, { method: 'GET' });
}

/**
 * POST request helper
 */
async function post<TRequest, TResponse>(
  endpoint: string,
  data: TRequest
): Promise<TResponse> {
  return apiRequest<TResponse>(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * PATCH request helper
 */
async function patch<TRequest, TResponse>(
  endpoint: string,
  data: TRequest
): Promise<TResponse> {
  return apiRequest<TResponse>(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

/**
 * DELETE request helper
 */
async function del(endpoint: string): Promise<void> {
  return apiRequest<void>(endpoint, { method: 'DELETE' });
}

// ==================== Health & Status ====================

export const health = {
  check: () => get<T.HealthResponse>('/health'),
};

// ==================== Dashboard ====================

export const dashboard = {
  getSummary: () => get<T.DashboardSummary>('/summary'),
};

// ==================== Projects ====================

export const projects = {
  list: (params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.skip) query.append('skip', params.skip.toString());
    if (params?.limit) query.append('limit', params.limit.toString());
    const queryString = query.toString();
    return get<T.Project[]>(`/projects${queryString ? `?${queryString}` : ''}`);
  },

  create: (data: T.CreateProjectRequest) =>
    post<T.CreateProjectRequest, T.Project>('/projects', data),

  getById: (projectId: string) =>
    get<T.Project>(`/projects/${projectId}`),

  update: (projectId: string, data: T.UpdateProjectRequest) =>
    patch<T.UpdateProjectRequest, T.Project>(`/projects/${projectId}`, data),

  delete: (projectId: string) =>
    del(`/projects/${projectId}`),

  getContent: (projectId: string, params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.skip) query.append('skip', params.skip.toString());
    if (params?.limit) query.append('limit', params.limit.toString());
    const queryString = query.toString();
    return get<T.ContentItem[]>(
      `/projects/${projectId}/content${queryString ? `?${queryString}` : ''}`
    );
  },

  getMedia: (projectId: string, params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.skip) query.append('skip', params.skip.toString());
    if (params?.limit) query.append('limit', params.limit.toString());
    const queryString = query.toString();
    return get<T.MediaFile[]>(
      `/projects/${projectId}/media${queryString ? `?${queryString}` : ''}`
    );
  },
};

// ==================== Content Generation ====================

export const content = {
  generateBlog: (data: T.GenerateBlogRequest) =>
    post<T.GenerateBlogRequest, T.GenerateBlogResponse>('/content/blog', data),

  generateOutline: (data: T.GenerateOutlineRequest) =>
    post<T.GenerateOutlineRequest, T.GenerateOutlineResponse>('/content/outline', data),

  generateNewsletter: (data: T.GenerateNewsletterRequest) =>
    post<T.GenerateNewsletterRequest, T.GenerateNewsletterResponse>('/content/newsletter', data),

  generatePost: (data: T.GenerateSocialPostRequest) =>
    post<T.GenerateSocialPostRequest, T.GenerateSocialPostResponse>('/content/post', data),

  generateHooks: (data: T.GenerateHooksRequest) =>
    post<T.GenerateHooksRequest, T.GenerateHooksResponse>('/content/hooks', data),

  generateCampaign: (data: T.GenerateCampaignRequest) =>
    post<T.GenerateCampaignRequest, T.GenerateCampaignResponse>('/content/campaign', data),

  expand: (data: T.ExpandContentRequest) =>
    post<T.ExpandContentRequest, T.ExpandContentResponse>('/content/expand', data),

  shorten: (data: T.ShortenContentRequest) =>
    post<T.ShortenContentRequest, T.ShortenContentResponse>('/content/shorten', data),

  rewrite: (data: T.RewriteContentRequest) =>
    post<T.RewriteContentRequest, T.RewriteContentResponse>('/content/rewrite', data),
};

// ==================== Virality ====================

export const virality = {
  score: (data: T.ViralityScoreRequest) =>
    post<T.ViralityScoreRequest, T.ViralityScoreResponse>('/virality/score', data),

  rewrite: (data: T.ViralityRewriteRequest) =>
    post<T.ViralityRewriteRequest, T.ViralityRewriteResponse>('/virality/rewrite', data),
};

// ==================== Video Processing ====================

export const video = {
  trim: (data: T.TrimVideoRequest) =>
    post<T.TrimVideoRequest, T.TrimVideoResponse>('/video/trim', data),

  generateCaptions: (data: T.GenerateCaptionsRequest) =>
    post<T.GenerateCaptionsRequest, T.GenerateCaptionsResponse>('/video/captions', data),

  resize: (data: T.ResizeVideoRequest) =>
    post<T.ResizeVideoRequest, T.ResizeVideoResponse>('/video/resize', data),

  generateShorts: (data: T.GenerateShortsRequest) =>
    post<T.GenerateShortsRequest, T.GenerateShortsResponse>('/video/shorts', data),
};

// ==================== Audio Processing ====================

export const audio = {
  cleanup: (data: T.CleanupAudioRequest) =>
    post<T.CleanupAudioRequest, T.CleanupAudioResponse>('/audio/cleanup', data),

  pitchShift: (data: T.PitchShiftRequest) =>
    post<T.PitchShiftRequest, T.PitchShiftResponse>('/audio/pitch', data),

  tempoShift: (data: T.TempoShiftRequest) =>
    post<T.TempoShiftRequest, T.TempoShiftResponse>('/audio/tempo', data),

  extractFromVideo: (data: T.ExtractAudioRequest) =>
    post<T.ExtractAudioRequest, T.ExtractAudioResponse>('/audio/extract', data),
};

// ==================== Music Studio (Stub) ====================

export const music = {
  generateTrack: (data: T.GenerateTrackRequest) =>
    post<T.GenerateTrackRequest, T.GenerateTrackResponse>('/music/generate', data),
};

// ==================== AI Video (Stub) ====================

export const aiVideo = {
  generate: (data: T.GenerateAIVideoRequest) =>
    post<T.GenerateAIVideoRequest, T.GenerateAIVideoResponse>('/video/generate-ai', data),
};

// ==================== Default Export ====================

const apiClient = {
  health,
  dashboard,
  projects,
  content,
  virality,
  video,
  audio,
  music,
  aiVideo,
};

export default apiClient;
