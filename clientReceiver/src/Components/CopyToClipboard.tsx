import { useState } from "react";
import { HiCheck } from "react-icons/hi2";
import { RxClipboardCopy } from "react-icons/rx";

export function CopyToClipboard({getText,name}:{getText:()=>string,name:string}){
	const [textWasCopied,setTextWasCopied] = useState(false)
	const clickHandler = async () => {

		// Set textWasCopied to true
		try{
			await navigator.clipboard.writeText(getText());
		}catch(err){
			console.log("waiwaiwai")
			// throw new Error("waiwaiwai MY CUSTOM ERROR WHEN COPYING FAILS!")
			console.error("waiwaiwai MY CUSTOM ERROR WHEN COPYING FAILS!")			// should probably find a way to do better error handling
			try{
				copy(getText())
			}catch(err){
				console.log("asdajsd")
				console.error("MY CUSTOM ERROR WHEN COPYING FAILS!")			// should probably find a way to do better error handling
			}
		}
		setTextWasCopied(true)

		setTimeout(()=>{
			setTextWasCopied(false)
		},10000)
	}

	const copy = (text:string) => {
		document.oncopy = function(event){
			if (event && event.clipboardData){
				event.clipboardData.setData("text/plain",text)
				event.preventDefault()
			}else{
				throw new Error("event is NULL")
			}
		}
		document.execCommand("copy",false)
	}
	
	return (
		<span style={{position:"relative",top:"0.1rem",padding:"0.25rem"}} className={name} onClick={clickHandler}>
			{
				textWasCopied ? <HiCheck/> : <RxClipboardCopy/>
			}
		</span>
	)
}