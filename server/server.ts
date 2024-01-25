import fs from "fs"
import path from "path"
import { File, Blob } from "@web-std/file"
const dJSON = require('dirty-json');

var file = new File([new Blob([fs.readFileSync(path.join(__dirname, "assets", "a1.jpg"))])], 'a1a.jpg', { type: 'image/jpeg' });

var formData = new FormData();
formData.append('encoded_image', file);

console.log("Fetching!")
var time = new Date().getTime()
fetch(`https://lens.google.com/v3/upload?&stcs=${new Date().getTime()}`, {
	method: 'POST',
	body: formData
}).then(res => {
	console.log("GOT RESPONSE!")
	return res.text()
}).then(text => {


	const pattern = />AF_initDataCallback\({key: 'ds:1',.*?\)\;<\/script>/
	const matchResult = text.match(pattern)
	if (matchResult) {
		// Get JSON from response
		const codeBlockText = matchResult[0]
		const frontFiltered = codeBlockText.substring(21)
		const frontBackFiltered = frontFiltered.substring(0, frontFiltered.length - 11)
		const lensResponseJSON = dJSON.parse(frontBackFiltered)


		// If `errorHasStatus` field is `true`, then throw error
		if (lensResponseJSON["errorHasStatus"]) throw new Error("errorHasStatus is true.Your image is probably too large, and must be shrunk to less than 1,000,000 pixels")
		// If no text if found, length will be === 0
		if (lensResponseJSON.data[3][4][0].length === 0) throw new Error("No text")

		const textLines = lensResponseJSON.data[3][4][0][0]
		console.log(textLines.join(" "))

	} else {
		console.log(pattern)
		throw new Error("ERROR no match. ")
	}

	console.log(Math.round(((new Date().getTime()) - time) / 10) / 100, "seconds")
}).catch(err => { throw new Error(err) })
