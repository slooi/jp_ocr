import { TimeLogger } from "./utils/TimeLogger"
const screenshot = require('screenshot-desktop')
import fs from "fs"
import path from "path"
import sharp from "sharp";


type RectangularShape = {x1:number,y1:number,x2:number,y2:number}

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
	async captureArea(rectangularShape:RectangularShape): Promise<Buffer> {
		function calcExtractArgs(area:RectangularShape){
			/* 
				Purpose:
				- Receives some SHAPE and outputs arguments which can be used by Sharp's .extract method
			*/

			if(area.x1 === area.x2 || area.y1 === area.y2) throw new Error("ERROR: Width AND height must both have a length > 0")
			
			let top, left, width,height = 0

			// Calculate vertical
			if (area.y1<area.y2) {
				top =area.y1 
				height = area.y2 - area.y1
			} else {
				top =area.y2
				height = area.y1 - area.y2 
			}

			// Calculate horizontal
			if (area.x1<area.x2) {
				left =area.x1
				width = area.x2 - area.x1
			} else {
				left =area.x2
				width = area.x1 - area.x2
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
			image.extract(calcExtractArgs(rectangularShape)).toFile(path.join(__dirname,"..",".assets","crop.jpg"))
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

