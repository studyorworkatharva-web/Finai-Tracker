import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { jwtDecode } from 'jwt-decode';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: { id: number; email: string } | null;
  login: (tokens: { access_token: string; refresh_token: string }) => void;
  logout: () => void;
  // TODO: Add refresh token logic
}

interface DecodedToken {
  sub: string; // User ID
  exp: number;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,

      login: (tokens) => {
        try {
          const decoded = jwtDecode<DecodedToken>(tokens.access_token);
          // We don't have the email from the JWT,
          // so we'd fetch it from /auth/me
          // For now, let's just store the ID
          set({
            accessToken: tokens.access_token,
            refreshToken: tokens.refresh_token,
            user: { id: parseInt(decoded.sub), email: '...loading' }, // Placeholder
          });
        } catch (error) {
          console.error("Failed to decode token", error);
          set({ accessToken: null, refreshToken: null, user: null });
        }
      },

      logout: () => {
        set({ accessToken: null, refreshToken: null, user: null });
      },
    }),
    {
      name: 'finai-auth-storage', // key in localStorage
    }
  )
);