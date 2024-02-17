import React, { useEffect, useState } from 'react';
import { RxClipboardCopy } from "react-icons/rx";
import { TextItem } from './TextItem';

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
		const htmlElement = document.querySelectorAll("html")[0]
		htmlElement.scrollTop = htmlElement.scrollHeight - htmlElement.clientHeight
	}, [textArray]);

	return (
		<>
			<div id="content">
				{textArray.map(text => (
				<p style={{display:"flex",alignItems:"end"}}>
					<TextItem text={text}/>
				</p>
				))}
			</div>
			<footer></footer>
		</>
	);
}

export default App;
