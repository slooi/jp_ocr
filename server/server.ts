import path from "path"
import { GoogleLensOCR } from "./services/ocr"
import { ScreenCapturer } from "./services/ScreenCapturer"
import express, { NextFunction, Request, Response } from "express"
import multer from "multer"
import { asyncNextCaller } from "./errorUtils"
import ws from "ws"



// ############################################################################
// 								CONSTANTS
// ############################################################################

const PORT = 54321

const upload = multer()
const app = express()

// ############################################################################
// 								HTTP MIDDLEWARE
// ############################################################################

// 
app.use(express.json())
// app.use(express.json({ limit: '50mb' }));
// app.use(express.urlencoded({ limit: '50mb' }));

// Middleware for visibility
app.use((req, res, next) => {
	console.log("req.path req.method:", req.path, req.method);
	console.log("req.body:", req.body)
	next();
});

// ############################################################################
// 								HTTP ROUTES
// ############################################################################

app.get("/test", asyncNextCaller(async (req, res) => {
	console.log("GoT IT!")
	res.status(200).json(await controllerScreenToOCR())
}))
app.get("/", asyncNextCaller(async (req, res) => {
	res.status(200).sendFile(path.join(__dirname, "index.html"))
}))
app.post("/", upload.single('image2'), asyncNextCaller(async (req, res) => {
	console.log("GoT IT! image")
	if (!req.file) throw new Error("File was not uploaded in post!")

	const googleLensOCR = new GoogleLensOCR({ DEBUG_MODE: true })
	const ocrText = await googleLensOCR.call(req.file.buffer)
	wsList.forEach(ws => ws.send(ocrText))
	res.status(200).json(ocrText)
}))
const server = app.listen(PORT, () => { console.log("Listening on port " + PORT) })


// ############################################################################
// 								HTTP ERROR HANDLER
// ############################################################################

app.use(async (error: Error, req: Request, res: Response, next: NextFunction) => {
	console.log("############################### MIDDLEWARE ERROR ###############################################")
	// Error.captureStackTrace() //???????????

	const a = { error: error }
	console.log(a)
	res.status(500).json(a);
})

// ############################################################################
// 								WEBSOCKETS
// ############################################################################

// WEBSOCKET SERVER
const wsList: ws[] = []
const wsServer = new ws.Server({ server: server, path: "/websocket" })
wsServer.on("connection", ws => {
	wsList.push(ws)
	console.log("CONNECTION!")
	setTimeout(() => {
		ws.send("websocket connection established")
	}, 1000)

	ws.onmessage = (event) => {
		console.log(event.data)
	}
	ws.onclose = event => {
		const index = wsList.indexOf(ws)
		if (index === -1) throw new Error("ERROR could not find ws instance in wsList")
		wsList.splice(index, 1)
	}
})

// ############################################################################
// 								HELPER FUNCTIONS
// ############################################################################
async function controllerScreenToOCR(): Promise<string> {
	// Create ScreenCapturer
	const screenCapturer = new ScreenCapturer({ DEBUG_MODE: true })
	const buffer = await screenCapturer.captureArea({ x1: 0, y1: 1000, x2: 1920, y2: 1080 })

	// Create GoogleLensOCR
	const googleLensOCR = new GoogleLensOCR()
	return await googleLensOCR.call(buffer)
}

// ############################################################################
// ############################################################################
// ############################################################################



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