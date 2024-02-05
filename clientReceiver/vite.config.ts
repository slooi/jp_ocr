import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		proxy: {
			"/": {
				target: "ws://localhost:54321",
				ws: true
			},
		}
	}
})
