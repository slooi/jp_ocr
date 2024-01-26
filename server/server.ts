import path from "path"
import { GoogleLensOCR } from "./services/ocr"

const googleLensOCR = new GoogleLensOCR()
googleLensOCR.call(path.join(__dirname, "assets", "w9.png"))