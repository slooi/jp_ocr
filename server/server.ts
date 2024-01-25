import path from "path"
import { GoogleLensOCR } from "./ocr"

const googleLensOCR = new GoogleLensOCR()
googleLensOCR.call(path.join(__dirname, "assets", "e3.png"))