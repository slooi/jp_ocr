import express from "express"
import fs from "fs"
import path from "path";
const app = express()
const PORT = 8080

const dJSON = require('dirty-json');






send()


function send() {
	// Create form with image attached to `encoded_image` 
	var formdata = new FormData();
	formdata.append("encoded_image",  new Blob([fs.readFileSync(path.join(__dirname,"a1.png"))], { type: 'image/png' }));


	// Inherit from RequestInit so I don't get error		<= !@#!@#!@# LEARNING
	interface RequestInitWithBody extends RequestInit {
		body: FormData;
	}
	const requestOptions: RequestInitWithBody = {
		method: 'POST',
		body: formdata,
	  };
	  
	  fetch(`https://lens.google.com/v3/upload?hl=en-NZ&re=df&st=${new Date().getTime()}&vpw=794&vph=993&ep=gisbubb`, requestOptions)		.then(res => {
			// Handle the response
			console.log("getting response text!")
			return res.text()
		})
		.then(data => {
			// fs.writeFile("./res.html", data, { encoding: "utf-8", flag: "w" }, err => { if (err) { throw new Error(`${err}`) } else { console.log("no error when logging") } })
			console.log("WRITING OUTPUT")
			fs.writeFileSync("./res.html",data,{encoding:"utf-8"})
			console.log("WRITING OUTPUT DONE")
			const text = data
			const pattern = />AF_initDataCallback\({key: 'ds:1',.*?\)\;<\/script>/
			const matchResult = text.match(pattern)
			if (matchResult) {
				const codeBlockText = matchResult[0]
				const frontFiltered = codeBlockText.substring(21)
				const frontBackFiltered = frontFiltered.substring(0, frontFiltered.length - 11)
				const lensResponseJSON = dJSON.parse(frontBackFiltered)

				// If `errorHasStatus` field is `true`, then throw error
				if (lensResponseJSON["errorHasStatus"]) throw new Error("errorHasStatus is true")
				// If no text if found, length will be === 0
				if (lensResponseJSON.data[3][4][0].length === 0) throw new Error("No text")

				const textLines = lensResponseJSON.data[3][4][0][0]
				console.log(textLines)
			} else {
				throw new Error("THIS SHOULDNT BE HAPPENING")
			}

		})
		.catch(error => {
			// Handle errors
			throw new Error(error)
		});
}




// var formdata = new FormData();
// formdata.append("encoded_image",  new Blob([fs.readFileSync(path.join(__dirname,"a2.png"))], { type: 'image/png' }));

// interface RequestInitWithBody extends RequestInit {
// 	body: FormData;
// }
// const requestOptions: RequestInitWithBody = {
//   method: 'POST',
//   body: formdata
// };

// fetch("https://lens.google.com/v3/upload", requestOptions)
//   .then(response => response.text())
//   .then(result => console.log(result))
//   .catch(error => console.log('error', error));