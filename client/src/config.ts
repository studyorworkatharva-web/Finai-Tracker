const isProduction = import.meta.env.MODE === 'production';

const API_URLS = {
  development: {
    auth: 'http://localhost:8001',
    transactions: 'http://localhost:8002',
    ai: 'http://localhost:8003',
  },
  production: {
    // These VITE_ vars are set in Vercel
    auth: import.meta.env.VITE_API_AUTH_URL,
    transactions: import.meta.env.VITE_API_TRANSACTIONS_URL,
    ai: import.meta.env.VITE_API_AI_URL,
  },
};

export const config = {
  apiUrl: isProduction ? API_URLS.production : API_URLS.development,
};