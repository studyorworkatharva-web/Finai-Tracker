import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { jwtDecode } from 'jwt-decode';
import { authApi } from '../lib/api';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: { id: number; email: string } | null;
  login: (tokens: { access_token: string; refresh_token: string }) => Promise<void>;
  logout: () => void;
}

interface DecodedToken {
  sub: string;
  exp: number;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,

      login: async (tokens) => {
        try {
          const decoded = jwtDecode<DecodedToken>(tokens.access_token);
          const me = await authApi.get('/me', {
            headers: { Authorization: `Bearer ${tokens.access_token}` },
          });

          set({
            accessToken: tokens.access_token,
            refreshToken: tokens.refresh_token,
            user: me.data || { id: parseInt(decoded.sub), email: 'unknown' },
          });
        } catch (error) {
          console.error('Login failed:', error);
          set({ accessToken: null, refreshToken: null, user: null });
        }
      },

      logout: () => set({ accessToken: null, refreshToken: null, user: null }),
    }),
    { name: 'finai-auth-storage' }
  )
);
