import { promises as fsp } from "fs"
import path from "path"
import { File, Blob } from "@web-std/file"
import Jimp from "jimp";
import sharp from "sharp";
const dJSON = require('dirty-json');

const sizeOf = require("image-size")


class TimeLogger {
	times: number[]
	constructor() {
		this.times = []
	}
	start() {
		this.times.push(new Date().getTime())
	}
	lapAndLog() {
		console.log("Full-time:", Math.round(((new Date().getTime()) - this.times[0]) / 10) / 100, "seconds", " Delta-time:", Math.round(((new Date().getTime()) - this.times[this.times.length - 1]) / 10) / 100, "seconds")
		this.times.push(new Date().getTime())
	}
}
const timeLogger = new TimeLogger()

class GoogleLensOCR {
	/* 
		This calls the Google Lens OCR api.
		RESTURNS:
			STRING - a string containing the text of the characters in the image
	*/
	constructor() { }
	async call(imagePath: string) {
		console.log("!!!   TIMER START   !!!")
		timeLogger.start()


		const file = await this.preprocess(imagePath)
		timeLogger.lapAndLog()
		var formData = new FormData();
		formData.append('encoded_image', file);

		console.log("---   FETCHING TEXT   ---")
		fetch(`https://lens.google.com/v3/upload?&stcs=${new Date().getTime()}`, {
			method: 'POST',
			body: formData
		}).then(res => {
			timeLogger.lapAndLog()
			console.log("---   PROCESSING RESPONSE   ---")
			return res.text()
		}).then(async text => {


			timeLogger.lapAndLog()
			const pattern = />AF_initDataCallback\({key: 'ds:1',.*?\)\;<\/script>/
			const matchResult = text.match(pattern)
			if (matchResult) {
				// Get JSON from response
				const codeBlockText = matchResult[0]
				const frontFiltered = codeBlockText.substring(21 + 30)
				const frontBackFiltered = frontFiltered.substring(0, frontFiltered.length - (11 + 18))
				await fsp.writeFile("asdfghjk.json", frontBackFiltered, { encoding: "utf-8" })
				timeLogger.lapAndLog()
				console.log("  # 1")
				const lensResponseJSON = JSON.parse(frontBackFiltered)
				timeLogger.lapAndLog()
				console.log("  # 2")


				// If `errorHasStatus` field is `true`, then throw error
				if (lensResponseJSON["errorHasStatus"]) throw new Error("errorHasStatus is true.Your image is probably too large, and must be shrunk to less than 1,000,000 pixels")
				// If no text if found, length will be === 0
				if (lensResponseJSON[3][4][0].length === 0) throw new Error("No text")

				const textLines = lensResponseJSON[3][4][0][0]
				timeLogger.lapAndLog()
				console.log(textLines.join(" "))

			} else {
				console.log(pattern)
				throw new Error("ERROR no match. You most likely have an post request with invalid data (eg: File with text/jpg instead of text/jpeg). ")
			}

		}).catch(err => { throw new Error(err) })

	}
	async preprocess(imagePath: string, MAX_PIXELS = 3000000) {
		function findMaxPossibleDimensions(oldWidth, oldHeight, maxPixels) {
			// Calculate scale
			const scale = ((oldWidth * oldHeight) / maxPixels) ** 0.5

			// Calculate new image dimensions
			const newWidth = Math.floor(oldWidth / scale)
			const newHeight = Math.floor(oldHeight / scale)

			return [newWidth, newHeight]
		}
		function findDimensionsWhereLongestLengthIs(oldWidth, oldHeight, LONGEST_LENGTH = 1000) {
			// Find if width or height is larger. We will set the larger dimension to 1000 and reduce the other dimension to keep the same previous aspect ratio
			const aspectRatio = oldWidth / oldHeight


			let newWidth = 0
			let newHeight = 0
			// Calculate new image dimensions
			if (aspectRatio) {
				// Width is larger than height
				newWidth = LONGEST_LENGTH
				const scale = LONGEST_LENGTH / oldWidth

				newHeight = Math.floor(oldHeight * scale)
			} else {
				// Height is larger than width
				newHeight = LONGEST_LENGTH
				const scale = LONGEST_LENGTH / oldHeight

				newWidth = Math.floor(oldWidth * scale)
			}
			return [newWidth, newHeight]
		}
		console.log("---   PRE-PROCESSING IMAGE   ---")
		const file = await fsp.readFile(imagePath)

		//####################
		// Get image size
		//####################
		// Get image and image meta data
		const image = await sharp(file)
		const metaData = await image.metadata()

		// Get old width
		const oldWidth = metaData.width
		const oldHeight = metaData.height

		if (oldWidth === undefined || oldHeight === undefined) throw new Error("image width and height are undefined!")


		if (oldWidth * oldHeight < MAX_PIXELS) {
			console.log("  ***   SKIPPING PRE-PROCESSING   ***  ")
			return new File([new Blob([await image.toBuffer()])], 'ocrImage.png', { type: 'image/png' });
		}
		//####################
		// Calculate new width and new height to ensure:   # of pixels in img is < MAX_PIXELS
		//####################
		const [newWidth, newHeight] = findDimensionsWhereLongestLengthIs(oldWidth, oldHeight)

		//####################
		// Reize Image
		//####################
		return image
			.resize(newWidth, newHeight)
			.jpeg({
				quality: 100,
			})
			.toBuffer()
			.then(res => {
				return new File([new Blob([res])], 'ocrImage.jpg', { type: 'image/jpeg' });
			})
		// .then(() => {
		// console.log("done!")
		// })

	}
}

// var time = new Date().getTime()

const googleLensOCR = new GoogleLensOCR()
// googleLensOCR.preprocess(path.join("assets", "saynotodrugs.png")).then(() => {
// 	console.log(Math.round(((new Date().getTime()) - time) / 10) / 100, "seconds")
// })


googleLensOCR.call(path.join(__dirname, "assets", "w4.png"))
// fs.readFileSync(path.join(__dirname, "assets", "edit.jpg"))