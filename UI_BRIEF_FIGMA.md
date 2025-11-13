# Quillography Content Suite - UI Design Brief

## Overview

This document outlines the user interface requirements for the Quillography Content Suite frontend application to be designed in Figma and implemented in React/Next.js.

---

## Design Goals

### Primary Objectives
1. **Intuitive Content Creation**: Make AI content generation feel natural and effortless
2. **Professional Polish**: Enterprise-grade UI suitable for content professionals
3. **Speed**: Fast workflows for power users
4. **Clarity**: Clear information hierarchy and visual feedback
5. **Flexibility**: Support different content types and workflows

### Target Users
- Content marketers
- Social media managers
- Copywriters
- Digital agencies
- Small business owners
- Content creators

---

## Color Palette

### Primary Colors
- **Brand Primary**: #6366F1 (Indigo) - Main actions, headers
- **Brand Secondary**: #8B5CF6 (Purple) - Accents, highlights
- **Success**: #10B981 (Green) - Success states, positive feedback
- **Warning**: #F59E0B (Amber) - Warnings, cautions
- **Error**: #EF4444 (Red) - Errors, destructive actions

### Neutral Colors
- **Dark**: #1F2937 (Gray 800) - Primary text
- **Medium**: #6B7280 (Gray 500) - Secondary text
- **Light**: #F3F4F6 (Gray 100) - Backgrounds
- **White**: #FFFFFF - Cards, surfaces

### Virality Score Colors
- **High (80-100)**: #10B981 (Green)
- **Medium (50-79)**: #F59E0B (Amber)
- **Low (0-49)**: #EF4444 (Red)

---

## Typography

### Font Family
- **Primary**: Inter (body text, UI elements)
- **Secondary**: Sora or Space Grotesk (headings, numbers)
- **Monospace**: JetBrains Mono (code, URLs)

### Type Scale
- **Display**: 48px / 600 - Page titles
- **H1**: 36px / 600 - Section headers
- **H2**: 24px / 600 - Card headers
- **H3**: 20px / 600 - Subsections
- **Body**: 16px / 400 - Main content
- **Small**: 14px / 400 - Meta information
- **Tiny**: 12px / 500 - Labels, tags

---

## Layout & Structure

### Dashboard (Home)
```
┌─────────────────────────────────────────────────┐
│ [Logo] Quillography        [Projects ▾] [User] │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Quick Stats                                │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│  │ 42   │ │ 156  │ │ 3.2K │ │ 87%  │          │
│  │Items │ │Posts │ │Reach │ │Avg   │          │
│  └──────┘ └──────┘ └──────┘ └──────┘          │
│                                                 │
│  Recent Content                    [+ New]     │
│  ┌─────────────────────────────────────────┐   │
│  │ 📝 Blog Post Title              [...]   │   │
│  │ Created 2 hours ago • 850 words         │   │
│  │ Virality: ████████░░ 82                 │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Projects                          [View All]  │
│  ┌──────┐ ┌──────┐ ┌──────┐                   │
│  │ 📁   │ │ 📁   │ │ ➕   │                   │
│  │Title │ │Title │ │ New  │                   │
│  └──────┘ └──────┘ └──────┘                   │
└─────────────────────────────────────────────────┘
```

### Content Creation Flow

#### Step 1: Choose Content Type
```
┌─────────────────────────────────────────────────┐
│ Create New Content                      [✕]    │
├─────────────────────────────────────────────────┤
│                                                 │
│  What would you like to create?                │
│                                                 │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐     │
│  │  📝   │ │  📧   │ │  📱   │ │  📣   │     │
│  │ Blog  │ │Letter │ │ Post  │ │Campaign│     │
│  └───────┘ └───────┘ └───────┘ └───────┘     │
│                                                 │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐     │
│  │  🎬   │ │  🎵   │ │  🔥   │ │  📋   │     │
│  │ Video │ │ Audio │ │Viral  │ │Outline│     │
│  └───────┘ └───────┘ └───────┘ └───────┘     │
└─────────────────────────────────────────────────┘
```

#### Step 2: Input Parameters
```
┌─────────────────────────────────────────────────┐
│ Generate Blog Post                      [✕]    │
├─────────────────────────────────────────────────┤
│                                                 │
│  Topic *                                        │
│  ┌─────────────────────────────────────────┐   │
│  │ AI and Machine Learning                 │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Style Profile                                  │
│  Tone:      [Professional ▾]                    │
│  Voice:     [Authoritative ▾]                   │
│  Length:    [Medium ▾]                          │
│                                                 │
│  Keywords (optional)                            │
│  ┌─────────────────────────────────────────┐   │
│  │ [AI] [ML] [+]                           │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Project                                        │
│  [Select project... ▾]                          │
│                                                 │
│  ┌─────────────────┐                           │
│  │ ✨ Generate     │                           │
│  └─────────────────┘                           │
└─────────────────────────────────────────────────┘
```

#### Step 3: Review & Edit
```
┌─────────────────────────────────────────────────┐
│ The Ultimate Guide to AI and ML   [💾] [⋮]    │
├─────────────────────────────────────────────────┤
│ [Edit] [Preview] [Virality]                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  # The Ultimate Guide to AI and Machine         │
│  Learning                                       │
│                                                 │
│  Introduction to AI and ML and why it           │
│  matters in today's world.                      │
│                                                 │
│  ## Section 1: Understanding AI                 │
│  This section explores the fundamentals...      │
│                                                 │
│  [Load More...]                                 │
│                                                 │
├─────────────────────────────────────────────────┤
│ 📊 Virality Score: 82  [Optimize]              │
│ 📈 Est. Reach: 850 • 💬 Est. Engagement: 45    │
│ 📝 Words: 1,200 • ⏱ Read Time: 5 min          │
└─────────────────────────────────────────────────┘
```

### Virality Dashboard
```
┌─────────────────────────────────────────────────┐
│ Virality Analysis                               │
├─────────────────────────────────────────────────┤
│                                                 │
│  Overall Score: 82 🔥                          │
│  ████████████████░░░░ High Potential           │
│                                                 │
│  Breakdown:                                     │
│  Hook Score:      ████████████████░░ 85        │
│  Structure Score: ███████████████░░░ 78        │
│  Niche Score:     ████████████████░░ 82        │
│                                                 │
│  Predicted Engagement: 850 interactions        │
│                                                 │
│  📋 Recommendations:                            │
│  ✓ Strong attention-grabbing hook              │
│  • Add more emotional triggers                  │
│  • Include specific examples                    │
│  • Strengthen call-to-action                    │
│                                                 │
│  ┌─────────────────────────────────┐           │
│  │ 🚀 Optimize for Virality        │           │
│  └─────────────────────────────────┘           │
└─────────────────────────────────────────────────┘
```

### Project Detail View
```
┌─────────────────────────────────────────────────┐
│ ← Projects  /  Content Marketing Q1             │
├─────────────────────────────────────────────────┤
│ [Content] [Media] [Analytics]                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Content Items (24)           [+ New] [Filter] │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ 📝 Blog: AI Guide              [...]    │   │
│  │ 1,200 words • Virality: 82 • 2h ago     │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ 📧 Newsletter: Week 5          [...]    │   │
│  │ 450 words • Virality: 75 • 1d ago       │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Media Files (8)                                │
│                                                 │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐                      │
│  │🎬 │ │🎬 │ │🎵 │ │📷 │                      │
│  └───┘ └───┘ └───┘ └───┘                      │
└─────────────────────────────────────────────────┘
```

---

## Component Library

### Buttons

**Primary Button**
- Background: Brand Primary (#6366F1)
- Text: White
- Hover: Darker shade
- Border radius: 8px
- Padding: 12px 24px

**Secondary Button**
- Background: Transparent
- Border: 2px solid Brand Primary
- Text: Brand Primary
- Hover: Light background

**Icon Button**
- 40x40px
- Border radius: 8px
- Icon: 20x20px

### Cards
- Border radius: 12px
- Shadow: 0 4px 6px rgba(0,0,0,0.1)
- Padding: 24px
- Background: White
- Hover: Slight shadow increase

### Inputs
- Height: 44px
- Border: 1px solid Gray 300
- Border radius: 8px
- Padding: 12px 16px
- Focus: Brand Primary border

### Progress Bars (Virality)
- Height: 8px
- Border radius: 4px
- Background: Gray 200
- Fill: Dynamic based on score

### Tags
- Border radius: 6px
- Padding: 4px 12px
- Font size: 12px
- Background: Brand Primary 10% opacity

---

## Iconography

### Icon Set
Use **Lucide Icons** or **Heroicons** for consistency

### Common Icons
- ✏️ Edit
- 🗑️ Delete
- 📋 Copy
- 💾 Save
- ⚙️ Settings
- 🔥 Virality/Hot
- 📊 Analytics
- 📁 Project
- ➕ Add/New
- 🔍 Search

---

## Animations & Interactions

### Micro-interactions
- Button hover: Scale 1.02, transition 150ms
- Card hover: Shadow increase, transition 200ms
- Loading: Spinner or skeleton screens
- Success: Green checkmark with bounce

### Transitions
- Page transitions: Fade 300ms
- Modal: Scale from 0.95 to 1.0, 200ms
- Dropdown: Slide down, 150ms

---

## Responsive Design

### Breakpoints
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px - 1439px
- Large Desktop: 1440px+

### Mobile Adaptations
- Bottom navigation bar
- Hamburger menu
- Stack cards vertically
- Simplified virality display
- Touch-friendly buttons (min 44x44px)

---

## Special Features

### AI Generation Loading State
```
┌─────────────────────────────────────┐
│  ✨ Generating your content...      │
│                                     │
│  [████████░░░░░░░░] 45%            │
│                                     │
│  Analyzing topic...                 │
│  Crafting engaging hook...          │
│  → Structuring content...           │
│  □ Optimizing for virality...       │
│  □ Finalizing...                    │
└─────────────────────────────────────┘
```

### Virality Score Meter
```
  Low        Medium        High
  ├─────────────┼─────────────┤
  ░░░░░░░░███████████████░░░░
              ↑
             82
```

### Content Type Selector
- Large, visual cards
- Icons that represent each type
- Hover state with description
- Quick keyboard shortcuts (B for Blog, etc.)

---

## Dark Mode Support

### Colors (Dark Theme)
- Background: #111827 (Gray 900)
- Surface: #1F2937 (Gray 800)
- Text Primary: #F9FAFB (Gray 50)
- Text Secondary: #D1D5DB (Gray 300)
- Brand colors remain the same

---

## Accessibility

### Requirements
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader friendly
- Focus indicators
- Sufficient color contrast (4.5:1 minimum)
- Alt text for all images
- ARIA labels for interactive elements

---

## Figma Deliverables

### Pages Required
1. **Dashboard** - Home screen
2. **Content Creation** - All content type flows
3. **Project Detail** - Project management view
4. **Virality Dashboard** - Scoring and optimization
5. **Settings** - User preferences
6. **Component Library** - All reusable components
7. **Mobile Views** - Responsive adaptations

### Assets Needed
- Logo variations
- Icon set
- Illustrations for empty states
- Loading animations
- Error state graphics

---

## Implementation Notes

### Frontend Stack
- React 18+ or Next.js 14+
- TypeScript
- Tailwind CSS for styling
- React Query for data fetching
- Zustand or Jotai for state management
- React Hook Form for forms
- Zod for validation

### API Integration
- Use API_REFERENCE.md for endpoint specs
- Handle loading states
- Handle error states
- Implement optimistic updates
- Cache responses appropriately

---

## Future Enhancements

### Phase 2
- Rich text editor integration
- Real-time collaboration indicators
- Advanced analytics visualizations
- Calendar/scheduling view
- Template library

### Phase 3
- Drag-and-drop content builder
- A/B testing UI
- Multi-user workspace management
- Advanced filters and search
- Export templates

---

Last Updated: 2024
Version: 1.0
