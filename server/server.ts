import { promises as fsp } from "fs"
import path from "path"
import { File, Blob } from "@web-std/file"
import Jimp from "jimp";
import sharp from "sharp";
const dJSON = require('dirty-json');

const sizeOf = require("image-size")



class GoogleLensOCR {
	/* 
		This calls the Google Lens OCR api.
		RESTURNS:
			STRING - a string containing the text of the characters in the image
	*/
	constructor() { }
	call(imagePath: string) {

	}
	async preprocess(imagePath: string, MAX_PIXELS = 3000000) {
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

		//####################
		// Calculate new width and new height to ensure:   # of pixels in img is < MAX_PIXELS
		//####################
		// Calculate scale
		const scale = ((oldWidth * oldHeight) / MAX_PIXELS) ** 0.5

		// Calculate new image dimensions
		const newWidth = Math.floor(oldWidth / scale)
		const newHeight = Math.floor(oldHeight / scale)

		//####################
		// Reize Image
		//####################
		return image
			.resize(newWidth, newHeight)
			.jpeg({
				quality: 100,
			})
			.toBuffer()
		// .then(() => {
		// console.log("done!")
		// })

	}
}

var time = new Date().getTime()

const googleLensOCR = new GoogleLensOCR()
googleLensOCR.preprocess(path.join("assets", "saynotodrugs.png")).then(() => {
	console.log(Math.round(((new Date().getTime()) - time) / 10) / 100, "seconds")
})


// const imageBlob = new Blob([fs.readFileSync(path.join(__dirname, "assets", "edit.jpg"))])
// var file = new File([imageBlob], 'ocrImage.jpg', { type: 'image/jpeg' });

// var formData = new FormData();
// formData.append('encoded_image', file);

// console.log("Fetching!")
// var time = new Date().getTime()
// fetch(`https://lens.google.com/v3/upload?&stcs=${new Date().getTime()}`, {
// 	method: 'POST',
// 	body: formData
// }).then(res => {
// 	console.log("GOT RESPONSE!")
// 	return res.text()
// }).then(text => {


// 	const pattern = />AF_initDataCallback\({key: 'ds:1',.*?\)\;<\/script>/
// 	const matchResult = text.match(pattern)
// 	if (matchResult) {
// 		// Get JSON from response
// 		const codeBlockText = matchResult[0]
// 		const frontFiltered = codeBlockText.substring(21)
// 		const frontBackFiltered = frontFiltered.substring(0, frontFiltered.length - 11)
// 		const lensResponseJSON = dJSON.parse(frontBackFiltered)


// 		// If `errorHasStatus` field is `true`, then throw error
// 		if (lensResponseJSON["errorHasStatus"]) throw new Error("errorHasStatus is true.Your image is probably too large, and must be shrunk to less than 1,000,000 pixels")
// 		// If no text if found, length will be === 0
// 		if (lensResponseJSON.data[3][4][0].length === 0) throw new Error("No text")

// 		const textLines = lensResponseJSON.data[3][4][0][0]
// 		console.log(textLines.join(" "))

// 	} else {
// 		console.log(pattern)
// 		throw new Error("ERROR no match. ")
// 	}

// 	console.log(Math.round(((new Date().getTime()) - time) / 10) / 100, "seconds")
// }).catch(err => { throw new Error(err) })
