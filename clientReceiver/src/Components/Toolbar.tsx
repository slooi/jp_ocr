import { useEffect, useRef, useState } from "react";
import { RxClipboardCopy } from "react-icons/rx";
import { CopyToClipboard } from "./CopyToClipboard";



export function Toolbar(){
	const [toolbarState, setToolbarState] = useState({x:0,y:0,show:false});
	const toolbarRef = useRef<HTMLDivElement | null>(null); // Fix the type of ref
	
	// Helper functions
	const doesRefContainTarget = (ref:React.MutableRefObject<HTMLDivElement | null>,target:EventTarget | null) => {
		if (target)
			return !!ref?.current?.contains(target as HTMLElement)
		return false
		
	}

	const getText = () => {
		console.log("getTest!")
		const selection = window.getSelection();
		if (selection && selection.toString().length > 0) {
			if (selection) {
				const selectedText = selection.toString();
				return selectedText.toString()
			}
		}
		throw new Error("ERROR WHEN TRYING TO COPY TEXT")
	}

	// HOOKS
	useEffect(()=>{
		
		// Mouse down handler
		const mouseDownHandler = (e: MouseEvent) =>{
			// console.log("doesRefContainTarget",doesRefContainTarget(toolbarRef,e.target))
			if (!doesRefContainTarget(toolbarRef,e.target)){
				setTimeout(()=>{
					setToolbarState(oldState=>({
						x:oldState.x,
						y:oldState.y,
						show: false,
					}));
				},10)
			}else{
				
			}
		}

		// Mouse up handler
		const mouseUpHandler = (e:MouseEvent) => {
			const selection = window.getSelection();
			if (selection && selection.toString().length > 0 && !doesRefContainTarget(toolbarRef,e.target)) {
				if (selection) {
					setTimeout(()=>{
						const selectedText = selection.toString();
						const range = selection.getRangeAt(0).getBoundingClientRect();
						console.log("selection",selection)
						setToolbarState({
							x: e.pageX,
							y: e.pageY,
							show: true,
						});
						console.log("showing!")
					},0)
				}
			}else{
				setTimeout(()=>{
					setToolbarState(oldState=>({
						x:oldState.x,
						y:oldState.y,
						show: false,
					}));
				},10)
			}
			
		}

		// Add listeners
		document.body.addEventListener("mousedown",mouseDownHandler)
		document.body.addEventListener("mouseup",mouseUpHandler)

		// Call listeners callback
		return ()=>{
			document.body.removeEventListener("mousedown",mouseDownHandler)
			document.body.removeEventListener("mouseup",mouseUpHandler)
		}
	},[])

	return (
		<>
			{
				toolbarState.show &&(
					<div style={{ position: 'absolute', top: toolbarState.y, left: toolbarState.x, backgroundColor:"rgb(230,230,230)", padding:"0.1rem", boxShadow:"0 2px 4px rgba(0, 0, 0, 0.7)",border:"1px solid black",userSelect:"none"}} ref={toolbarRef}>
						<CopyToClipboard getText={getText}/>
					</div>
				)
			}
		</>
	)
}