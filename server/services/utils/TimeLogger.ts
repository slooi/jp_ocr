export class TimeLogger {
	times: number[]
	constructor() {
		this.times = []
	}
	start() {
		this.times.push(new Date().getTime())
		console.log("TIME\tDELTATIME")
		this.comment("!!!   TIMER START   !!!")
	}
	lap(text: string) {
		this.comment(text)
		this.times.push(new Date().getTime())
	}
	comment(text: string) {
		const totalTime = Math.round(((new Date().getTime()) - this.times[0]) / 10) / 100
		const deltaTime = Math.round(((new Date().getTime()) - this.times[this.times.length - 1]) / 10) / 100

		const taskTimeTabbs = deltaTime.toString().length === 1 ? "\t\t" : "\t"
		console.log(totalTime, "\t", "Task Time: ", deltaTime, taskTimeTabbs, text)
	}
}