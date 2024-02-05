import path from "path"
import { GoogleLensOCR } from "./services/ocr"
import { ScreenCapturer } from "./services/ScreenCapturer"
import express, { NextFunction, Request, Response } from "express"
import multer from "multer"
import { asyncNextCaller } from "./errorUtils"
const PORT = 54321

const upload = multer()
const app = express()
app.use(express.json())
// app.use(express.json({ limit: '50mb' }));
// app.use(express.urlencoded({ limit: '50mb' }));




// Middleware for visibility
app.use((req, res, next) => {
	console.log("req.path req.method:", req.path, req.method);
	console.log("req.body:", req.body)
	next();
});




app.get("/", asyncNextCaller(async (req, res) => {
	console.log("GoT IT!")
	await controllerScreenToOCR()
	res.status(200).end()
}))
app.post("/", upload.single('image2'), asyncNextCaller(async (req, res) => {
	console.log("GoT IT! image")
	if (!req.file) throw new Error("File was not uploaded in post!")


	const googleLensOCR = new GoogleLensOCR({ DEBUG_MODE: true })
	await googleLensOCR.call(req.file.buffer)

	res.status(200).end()
}))
app.listen(PORT, () => { console.log("Listening on port " + PORT) })

async function controllerScreenToOCR() {
	// Create ScreenCapturer
	const screenCapturer = new ScreenCapturer({ DEBUG_MODE: true })
	const buffer = await screenCapturer.captureArea({ x1: 0, y1: 1000, x2: 1920, y2: 1080 })

	// Create GoogleLensOCR
	const googleLensOCR = new GoogleLensOCR()
	await googleLensOCR.call(buffer)

}


app.use(async (error: Error, req: Request, res: Response, next: NextFunction) => {
	console.log("############################### MIDDLEWARE ERROR ###############################################")
	// Error.captureStackTrace() //???????????

	const a = { error: error }
	console.log(a)
	res.status(500).json(a);
})

// setTimeout(() => { controllerScreenToOCR() }, 2000)



// (async function () {
// 	const chalk = (await import('chalk')).default
// 	console.log(chalk.blue('This is a blue message.'));
// 	console.log(chalk.red.bold('This is a bold red message.'));
// 	console.log(chalk.green.inverse('This is an inverted green message.'));

// 	// Aligning text to the right
// 	console.log(chalk.white.bgBlack('Aligned to the right').padStart(50));
// 	console.log(chalk.white.bgBlack('Aligned to asd').padStart(50));
// })()