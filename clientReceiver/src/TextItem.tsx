
import { HiCheck } from "react-icons/hi2";
import { RxClipboardCopy } from "react-icons/rx";
import {useState} from "react"

export function TextItem({text}:{text:string}){
	const [textWasCopied,setTextWasCopied] = useState(false)
	
	const copyText = (text:string) => {
		// Write text to clipboard
		navigator.clipboard.writeText(text);

		// Set textWasCopied to true
		setTextWasCopied(true)

		setTimeout(()=>{
			setTextWasCopied(false)
		},10000)
	}

	return (
		<>
			<span style={{padding:"0.25rem",marginRight:"0.5rem"}} className='icon-wrapper' onClick={()=>copyText(text)}>
				{
					textWasCopied ? <HiCheck/> : <RxClipboardCopy/>
				}
			</span>
			<span style={{margin:"0.25rem 0"}}>{text}</span>
		</>
	)
}