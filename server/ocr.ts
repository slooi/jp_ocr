import { promises as fsp } from "fs"
import path from "path"
import { File, Blob } from "@web-std/file"
import sharp from "sharp";

class TimeLogger {
	times: number[]
	constructor() {
		this.times = []
	}
	start() {
		this.times.push(new Date().getTime())
		this.comment("!!!   TIMER START   !!!")
	}
	lap(text: string) {
		this.comment(text)
		this.times.push(new Date().getTime())
	}
	comment(text: string) {
		console.log(Math.round(((new Date().getTime()) - this.times[0]) / 10) / 100, "\t", Math.round(((new Date().getTime()) - this.times[this.times.length - 1]) / 10) / 100, "\t", text)

	}
}
const timeLogger = new TimeLogger()

export class GoogleLensOCR {
	/* 
		This calls the Google Lens OCR api.
		RETURNS:
			STRING - a string containing the text of the characters in the image
	*/
	constructor() { }
	async call(imagePath: string) {
		try {
			console.log(`imagePath: ${imagePath}`)
			timeLogger.start()

			// PRE-PROCESS
			timeLogger.lap("PRE-PROCESSING IMAGE\t")
			const file = await this.preprocess(imagePath)

			// ADD FILE TO FORM DATA
			var formData = new FormData();
			formData.append('encoded_image', file);

			// FETCH
			timeLogger.lap("FETCHING\t\t")
			const res = await fetch(`https://lens.google.com/v3/upload?&stcs=${new Date().getTime()}`, {
				method: 'POST',
				body: formData
			})

			// PROCESS RESPONSE
			timeLogger.lap("PROCESSING RESPONSE\t")
			const text = await res.text()
			timeLogger.lap("PARSING TEXT\t\t")
			const pattern = />AF_initDataCallback\({key: 'ds:1',.*?\)\;<\/script>/
			const matchResult = text.match(pattern)

			// CHECK
			if (!matchResult) throw new Error("ERROR no match. You most likely have an post request with invalid data (eg: File with text/jpg instead of text/jpeg). ")


			// Get JSON from response
			const codeBlockText = matchResult[0]
			const frontFiltered = codeBlockText.substring(21 + 30)
			const frontBackFiltered = frontFiltered.substring(0, frontFiltered.length - (11 + 18))
			const lensResponseJSON = JSON.parse(frontBackFiltered)


			// If `errorHasStatus` field is `true`, then throw error
			if (lensResponseJSON["errorHasStatus"]) throw new Error("errorHasStatus is true. Your image is probably too large, and must be shrunk to less than 1,000,000 pixels")
			// If no text if found, length will be === 0
			if (lensResponseJSON[3][4][0].length === 0) throw new Error("No text")

			// Get content
			const textLines = lensResponseJSON[3][4][0][0]
			const ocrText = textLines.join(" ")
			timeLogger.lap("FINISHED\t\t")
			console.log(ocrText)

			return ocrText
		} catch (err) {
			throw new Error(`${err}`)
		}
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
	}
}


// const googleLensOCR = new GoogleLensOCR()
// googleLensOCR.call(path.join(__dirname, "assets", "e3.png"))