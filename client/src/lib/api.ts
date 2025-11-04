import axios from 'axios';
import { config } from '../config';
import { useAuthStore } from '../hooks/useAuthStore';

const createApiClient = (baseURL: string) => {
  const api = axios.create({ baseURL });

  // Attach access token to every request
  api.interceptors.request.use((config) => {
    const { accessToken } = useAuthStore.getState();
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  });

  // Optional: auto-refresh token on 401
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        const { refreshToken, logout, login } = useAuthStore.getState();
        if (refreshToken) {
          try {
            const res = await axios.post(`${config.apiUrl.auth}/refresh`, {
              refresh_token: refreshToken,
            });
            login(res.data);
            error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
            return axios(error.config);
          } catch {
            logout();
          }
        }
      }
      return Promise.reject(error);
    }
  );

  return api;
};

export const authApi = createApiClient(config.apiUrl.auth);
export const transactionsApi = createApiClient(config.apiUrl.transactions);
export const aiApi = createApiClient(config.apiUrl.ai);
