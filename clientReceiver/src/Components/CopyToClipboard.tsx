import { useState } from "react";
import { HiCheck } from "react-icons/hi2";
import { RxClipboardCopy } from "react-icons/rx";

export function CopyToClipboard({getText}:{getText:()=>string}){
	const [textWasCopied,setTextWasCopied] = useState(false)
	const clickHandler = () => {
		// Write text to clipboard
		// navigator.clipboard.writeText(getText());
		copy(getText())

		// Set textWasCopied to true
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
		<span style={{position:"relative",top:"0.1rem",padding:"0.25rem"}} className='icon-wrapper' onClick={clickHandler}>
			{
				textWasCopied ? <HiCheck/> : <RxClipboardCopy/>
			}
		</span>
	)
}