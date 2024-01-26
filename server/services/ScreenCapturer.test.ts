import { ScreenCapturer } from "./ScreenCapturer";


(async function(){
	const screenCapturer = new ScreenCapturer()
	const buffer = await screenCapturer.captureArea({x1:0,y1:1080/2,x2:1920,y2:1080})

})()