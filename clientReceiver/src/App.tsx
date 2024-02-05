import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'



const ws = new WebSocket(location.origin.replace("http", "ws") + "/websocket")
const data: string[] = []
ws.onopen = (event) => {
	console.log("WEBSOCKET IS OPEN")
}
ws.onmessage = (event) => {
	data.push(event.data)
	console.log("event", event)
}
setTimeout(() => { ws.send("FROM CLIENT MSG") }, 5000)

function App() {
	const [count, setCount] = useState(0)

	// useEffect(() => {
	// 	console.log("hi")
	// }, [data])

	return (
		<>
			<div>hi2asdasd asd</div><div>hi2asdasd asd</div><div>hi2asdasd asd</div><div>hi2asdasd asd</div><div>hi2asdasd asd</div>
		</>
	)
}

export default App
