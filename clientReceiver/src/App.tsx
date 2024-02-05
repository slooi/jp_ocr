import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'



const ws = new WebSocket(location.origin.replace("http", "ws"))

function App() {
	const [count, setCount] = useState(0)


	return (
		<>
			<div>hi</div>
		</>
	)
}

export default App
