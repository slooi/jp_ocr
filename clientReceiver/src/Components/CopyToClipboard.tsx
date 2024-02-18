import { useState } from "react";
import { HiCheck } from "react-icons/hi2";
import { RxClipboardCopy } from "react-icons/rx";

export function CopyToClipboard({getText}:{getText:()=>string}){
	const [textWasCopied,setTextWasCopied] = useState(false)
	const clickHandler = () => {
		// Write text to clipboard
		navigator.clipboard.writeText(getText());

		// Set textWasCopied to true
		setTextWasCopied(true)

		setTimeout(()=>{
			setTextWasCopied(false)
		},10000)
	}
	
	return (
		<span style={{position:"relative",top:"0.1rem",padding:"0.25rem"}} className='icon-wrapper' onClick={clickHandler}>
			{
				textWasCopied ? <HiCheck/> : <RxClipboardCopy/>
			}
		</span>
	)
}