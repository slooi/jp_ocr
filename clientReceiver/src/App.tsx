import React, { useEffect, useState } from 'react';

const ws = new WebSocket(location.origin.replace("http", "ws") + "/websocket");

function App() {
	const [textArray, setTextArray] = useState<string[]>([]);

	ws.onopen = (event) => console.log("WEBSOCKET IS OPEN");
	ws.onmessage = (event) => {
		console.log("event", event);
		setTextArray((prevTextArray) => [...prevTextArray, event.data]);
	};
	ws.onerror = (err) => console.log('error:', err)

	useEffect(() => {
		console.log("Notified! :D", textArray);
	}, [textArray]);

	return (
		<>
			{textArray.map(text => (
				<p>{text}</p>
			))}
		</>
	);
}

export default App;
