import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Development only (npm run dev): the page comes from Vite (:5173) but the data comes from the
    // telemetry server, so Vite forwards WebSocket requests on /ws to it.
    // Keep the port in sync with DASHBOARD_PORT in telemetry_server/config.py.
    proxy: {
      '/ws': {
        target: 'ws://127.0.0.1:8082',
        ws: true,
        configure: (proxy) => {
          // Vite prints every dropped connection as an error; here that is normal
          // (tab closed, server stopped), so replace its handler with a quiet one.
          proxy.removeAllListeners('error');
          proxy.on('error', () => {});
        },
      },
    },
  },
})