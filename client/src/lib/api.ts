import axios from "axios";
import { config } from "../config";
import { useAuthStore } from "../hooks/useAuthStore";

const createApiClient = (baseURL: string) => {
  const api = axios.create({ baseURL });

  // ✅ Attach access token to every request
  api.interceptors.request.use((config) => {
    const { accessToken } = useAuthStore.getState();
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  });

  // ✅ Auto-refresh token if expired (on 401)
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        const { refreshToken, logout, login } = useAuthStore.getState();

        if (refreshToken) {
          try {
            // 🔥 Send refresh token as form data to match backend
            const formData = new URLSearchParams();
            formData.append("refresh_token", refreshToken);

            const res = await axios.post(
              `${config.apiUrl.auth}/auth/refresh`,
              formData,
              { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
            );

            // Save new tokens
            login(res.data);

            // Retry original request with new access token
            error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
            return axios(error.config);
          } catch (refreshError) {
            console.error("Token refresh failed:", refreshError);
            logout();
          }
        } else {
          logout();
        }
      }
      return Promise.reject(error);
    }
  );

  return api;
};

// ✅ Exported clients for different microservices
export const authApi = createApiClient(config.apiUrl.auth);
export const transactionsApi = createApiClient(config.apiUrl.transactions);
export const aiApi = createApiClient(config.apiUrl.ai);
