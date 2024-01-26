import { TimeLogger } from "./utils/TimeLogger"
const screenshot = require('screenshot-desktop')
import fs from "fs"
import path from "path"

// Create screen capturer
export class ScreenCapturer {
	constructor() { }
	async selectArea(): Promise<Buffer> {

		try {
			const img = await screenshot() as Buffer
			// fs.writeFileSync(path.join(".assets", "testing.jpg"), img);
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
// 	await new ScreenCapturer().selectArea()
// 	timeLogger.lap("Finished capturing")
// })()