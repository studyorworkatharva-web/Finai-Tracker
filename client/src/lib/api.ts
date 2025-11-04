import axios from 'axios';
import { config } from '../config';
import { useAuthStore } from '../hooks/useAuthStore';

// Create an instance for each microservice
const createApiClient = (baseURL: string) => {
  const api = axios.create({
    baseURL,
  });

  // Request interceptor to add the auth token
  api.interceptors.request.use(
    (config) => {
      const { accessToken } = useAuthStore.getState();
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // TODO: Add response interceptor for 401 errors to trigger refresh token logic

  return api;
};

export const authApi = createApiClient(config.apiUrl.auth);
export const transactionsApi = createApiClient(config.apiUrl.transactions);
export const aiApi = createApiClient(config.apiUrl.ai);