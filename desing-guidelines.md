# FinAI Design Guidelines

This document outlines the visual language, tokens, and component philosophy for the FinAI application, ensuring a "Modern, calm, trustworthy" aesthetic.

## 1. Visual Language & Brand Tokens

### Primary Palette
| Name | Light Mode | Dark Mode | CSS Variable | Tailwind |
| :--- | :--- | :--- | :--- | :--- |
| Primary | `#4F46E5` | `#6366F1` | `--color-primary` | `primary` |
| Accent | `#06B6D4` | `#22D3EE` | `--color-accent` | `accent` |
| Success | `#10B981` | `#34D399` | `--color-success` | `success` |
| Danger | `#EF4444` | `#F87171` | `--color-danger` | `danger` |
| Background | `#F8FAFC` | `#0F172A` | `--color-bg` | `bg-background` |
| Foreground | `#0F172A` | `#F8FAFC` | `--color-fg` | `text-foreground` |
| Muted | `#64748B` | `#94A3B8` | `--color-muted` | `text-muted` |
| Card BG | `rgba(255,255,255,0.6)`| `rgba(23, 37, 61, 0.6)`| `--color-card-bg`| `bg-card` |

### Secondary Gradient
* **Usage:** Hero elements, primary cards, goal progress.
* **Value:** `linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%)`

### Typography
* **UI Font:** `Inter` (Imported from Google Fonts)
    * Used for all body text, buttons, inputs, and data.
* **Heading Font:** `DM Serif Display` (Imported from Google Fonts)
    * Used for page titles (H1, H2) and large hero numbers.
* **Tailwind Families:** `font-sans` (Inter), `font-serif` (DM Serif Display)

### Spacing & Radius
* **Base Unit:** 4px
* **Spacing Scale:**
    * `p-1` (4px), `p-2` (8px), `p-3` (12px), `p-4` (16px), `p-6` (24px), `p-8` (32px)
* **Corner Radius:**
    * `--radius-md`: 0.5rem (8px) - Buttons, Inputs
    * `--radius-lg`: 1.0rem (16px) - Cards, Modals

### Elevation & Effects
* **Shadow:** `0 8px 24px rgba(12, 20, 40, 0.12)` (Used for `shadow-card` utility)
* **Glassmorphism:**
    * Applied to cards and sidebars.
    * `backdrop-filter: blur(16px);`
    * `background-color: var(--color-card-bg);` (Slightly transparent)

## 2. Motion (Framer Motion)
* **Provider:** `AnimatePresence` wraps the main page router.
* **Page Transitions:** 400-600ms. Fade + slight slide from bottom.
    ```javascript
    const pageVariants = {
      initial: { opacity: 0, y: 10 },
      in: { opacity: 1, y: 0 },
      out: { opacity: 0, y: -10 }
    };
    ```
* **Microinteractions:** 150-300ms (e.g., button hover, card hover).
    * **Card Hover:** `whileHover={{ scale: 1.02, y: -4 }}`
    * **Button Press:** `whileTap={{ scale: 0.95 }}`

## 3. Accessibility (AX)
* **Contrast:** All text combinations must meet WCAG AA (4.5:1 ratio).
* **Navigation:** All interactive elements (buttons, links, inputs) must be keyboard-focusable and have clear `:focus-visible` states (e.g., `focus-visible:ring-2 focus-visible:ring-primary`).
* **ARIA:**
    * Inputs use `aria-describedby` for error messages.
    * Icon buttons use `aria-label`.
    * Modals trap focus and close on `ESC`.
* **Dark Mode:** Implemented with `class` strategy and `useTheme` hook to respect system preference and allow manual toggle.