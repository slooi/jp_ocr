import path from "path"
import { GoogleLensOCR } from "./services/ocr"
import { ScreenCapturer } from "./services/ScreenCapturer"

async function controller() {
	// Create ScreenCapturer
	const screenCapturer = new ScreenCapturer({DEBUG_MODE:true})
	const buffer = await screenCapturer.captureArea({x1:0,y1:1000,x2:1920,y2:1080})

	// Create GoogleLensOCR
	const googleLensOCR = new GoogleLensOCR()
	await googleLensOCR.call(buffer)

}


setTimeout(()=>{controller()},2000)



// (async function () {
// 	const chalk = (await import('chalk')).default
// 	console.log(chalk.blue('This is a blue message.'));
// 	console.log(chalk.red.bold('This is a bold red message.'));
// 	console.log(chalk.green.inverse('This is an inverted green message.'));

// 	// Aligning text to the right
// 	console.log(chalk.white.bgBlack('Aligned to the right').padStart(50));
// 	console.log(chalk.white.bgBlack('Aligned to asd').padStart(50));
// })()