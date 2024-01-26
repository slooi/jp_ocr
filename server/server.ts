import path from "path"
import { GoogleLensOCR } from "./services/ocr"
import { ScreenCapturer } from "./services/ScreenCapturer"

async function controller() {
	// Create ScreenCapturer
	const screenCapturer = new ScreenCapturer()
	const buffer = await screenCapturer.selectArea()

	// Create GoogleLensOCR
	const googleLensOCR = new GoogleLensOCR()
	await googleLensOCR.call(buffer)

}
controller()


// (async function () {
// 	const chalk = (await import('chalk')).default
// 	console.log(chalk.blue('This is a blue message.'));
// 	console.log(chalk.red.bold('This is a bold red message.'));
// 	console.log(chalk.green.inverse('This is an inverted green message.'));

// 	// Aligning text to the right
// 	console.log(chalk.white.bgBlack('Aligned to the right').padStart(50));
// 	console.log(chalk.white.bgBlack('Aligned to asd').padStart(50));
// })()