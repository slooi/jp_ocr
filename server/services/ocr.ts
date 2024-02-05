import { promises as fsp } from "fs"
import path from "path"
import { File, Blob } from "@web-std/file"
import sharp from "sharp";
import { TimeLogger } from "./utils/TimeLogger";



export class GoogleLensOCR {
	timeLogger: TimeLogger
	/* 
		This calls the Google Lens OCR api.
		RETURNS:
			STRING - a string containing the text of the characters in the image
	*/
	DEBUG_MODE: boolean
	constructor(options?: { DEBUG_MODE: boolean }) {
		this.DEBUG_MODE = options?.DEBUG_MODE || false
		this.timeLogger = new TimeLogger()
	}
	async call(imageArg: string | Buffer) {
		/* 
			INPUTS:
				string - path to image
				Buffer - buffer of image
		*/


		try {
			if (this.timeLogger) this.timeLogger.start()


			const imageBuffer = typeof imageArg === "string" ? await fsp.readFile(imageArg) : imageArg
			// PRE-PROCESS
			// console.log(sharp.format)
			const file = await this.preprocess(imageBuffer)
			if (this.timeLogger) this.timeLogger.lap("PRE-PROCESSING IMAGE  DONE")
			if (this.DEBUG_MODE) {
				await fsp.writeFile(path.join(__dirname, ".debug." + "ocr.jpg"), imageBuffer);
				if (this.timeLogger) this.timeLogger.lap("\t***   DEBUG IMAGE  CREATED   ***")
			}

			// ADD FILE TO FORM DATA
			var formData = new FormData();
			formData.append('encoded_image', file);

			// FETCH
			const res = await fetch(`https://lens.google.com/v3/upload?&stcs=${new Date().getTime()}`, {
				method: 'POST',
				body: formData
			})
			if (this.timeLogger) this.timeLogger.lap("FETCHING  DONE")

			// PROCESS RESPONSE
			const text = await res.text()
			if (this.timeLogger) this.timeLogger.lap("PROCESSING RESPONSE  DONE")
			const pattern = />AF_initDataCallback\({key: 'ds:1',.*?\)\;<\/script>/
			const matchResult = text.match(pattern)

			// CHECK
			if (!matchResult) throw new Error("ERROR no match. You most likely have an post request with invalid data (eg: File with text/jpg instead of text/jpeg). ")


			// Get JSON from response
			const codeBlockText = matchResult[0]
			const frontFiltered = codeBlockText.substring(21 + 30)
			const frontBackFiltered = frontFiltered.substring(0, frontFiltered.length - (11 + 18))

			let lensResponseJSON = {}
			try {
				lensResponseJSON = JSON.parse(frontBackFiltered)
			} catch (err) {
				throw new Error("ERROR: could not JSON.parse filtered response")
			}



			// If `errorHasStatus` field is `true`, then throw error
			if (lensResponseJSON["errorHasStatus"]) throw new Error("errorHasStatus is true. Your image is probably too large, and must be shrunk to less than 1,000,000 pixels")
			// If no text if found, length will be === 0
			if (lensResponseJSON[3][4][0].length === 0) throw new Error("No text")

			// Get content
			const textLines = lensResponseJSON[3][4][0][0]
			const ocrText = textLines.join("\n")
			if (this.timeLogger) this.timeLogger.lap("PARSING TEXT  DONE")
			console.log(ocrText)

			return ocrText
		} catch (err) {
			throw err
		}
	}
	async preprocess(imageBuffer: Buffer, MAX_PIXELS = 3000000) {
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


		//####################
		// Get image size
		//####################
		// Get image and image meta data
		if (imageBuffer.buffer.byteLength === 0) throw new Error("ERROR: image uploaded has byte length of 0. Make sure to reset pointer")
		const image = await sharp(imageBuffer)
		const metaData = await image.metadata()

		// Get old width
		const oldWidth = metaData.width
		const oldHeight = metaData.height

		if (oldWidth === undefined || oldHeight === undefined) throw new Error("image width and height are undefined!")


		if (oldWidth * oldHeight < MAX_PIXELS) {
			if (this.timeLogger) this.timeLogger.lap("  ***   SKIPPING IMAGE RESIZE   ***  ")
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

// /* TESTING */
// (async function () {

// 	const googleLensOCR = new GoogleLensOCR()
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "e3.png"))
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "a1.png"))
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "a2.png"))
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "e0.png"))
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "e1.png"))
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "e2.png"))
// 	googleLensOCR.call(path.join(__dirname, "..", "assets", "e3.png"))
// })()