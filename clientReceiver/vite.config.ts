import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

import fs from "fs"
import path from "path"

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		https: {
			key: fs.readFileSync(path.join("..",".keys","server.key")),
			cert: fs.readFileSync(path.join("..",".keys","server.crt"))
		},
		proxy: {
			"/websocket": {
				target: "wss://localhost:54321",
				ws: true,
				changeOrigin: true,
				secure: false
			},
		},
		host: "0.0.0.0"
	}
})
