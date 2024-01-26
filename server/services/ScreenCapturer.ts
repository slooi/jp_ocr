import { TimeLogger } from "./utils/TimeLogger"
const screenshot = require('screenshot-desktop')
import fs from "fs"
import path from "path"

// Create screen capturer
export class ScreenCapturer {
	constructor() { }
	async captureScreen(): Promise<Buffer> {
		try {
			const img = await screenshot() as Buffer
			// fs.writeFileSync(path.join(__dirname,"..",".assets", "testing.jpg"), img);
			return img
		} catch (err) {
			throw err
		}
	}
}
// TESTING
// (async function () {
// 	const timeLogger = new TimeLogger()
// 	timeLogger.start()
// 	await new ScreenCapturer().captureScreen()
// 	timeLogger.lap("Finished capturing")
// })()