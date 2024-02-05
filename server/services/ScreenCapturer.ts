const screenshot = require('screenshot-desktop')
import fs from "fs"
import path from "path"
import sharp from "sharp";


type TwoPoints = { x1: number, y1: number, x2: number, y2: number }

// Create screen capturer
export class ScreenCapturer {
	DEBUG_MODE: boolean
	constructor(options?: { DEBUG_MODE: boolean }) {
		this.DEBUG_MODE = options?.DEBUG_MODE || false
	}
	async captureScreen(): Promise<Buffer> {
		try {
			const img = await screenshot() as Buffer
			// fs.writeFileSync(path.join(__dirname,"..",".assets", "testing.jpg"), img);
			return img
		} catch (err) {
			throw err
		}
	}
	async captureArea(twoPoints: TwoPoints): Promise<Buffer> {
		function calcRectangularShape(twoPoints: TwoPoints) {
			/* 
				Purpose:
				- Receives some SHAPE and outputs arguments which can be used by Sharp's .extract method
			*/

			if (twoPoints.x1 === twoPoints.x2 || twoPoints.y1 === twoPoints.y2) throw new Error("ERROR: Width AND height must both have a length > 0")

			let top, left, width, height = 0

			// Calculate vertical
			if (twoPoints.y1 < twoPoints.y2) {
				top = twoPoints.y1
				height = twoPoints.y2 - twoPoints.y1
			} else {
				top = twoPoints.y2
				height = twoPoints.y1 - twoPoints.y2
			}

			// Calculate horizontal
			if (twoPoints.x1 < twoPoints.x2) {
				left = twoPoints.x1
				width = twoPoints.x2 - twoPoints.x1
			} else {
				left = twoPoints.x2
				width = twoPoints.x1 - twoPoints.x2
			}

			return {
				width,
				height,
				left,
				top
			}
		}



		try {
			const img = await screenshot() as Buffer
			const image = await sharp(img)
			const imageExtract = await image.extract(calcRectangularShape(twoPoints))

			if (this.DEBUG_MODE) {
				imageExtract.toFile(path.join(__dirname, ".debug." + "ScreenCapturer.jpg"))
				console.log("___   CREATED DEBUG IMAGE   ___")
				// if (this.timeLogger) this.timeLogger.lap("\t***   DEBUG IMAGE  CREATED   ***")
			}
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

