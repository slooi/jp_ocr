
import { HiCheck } from "react-icons/hi2";
import { RxClipboardCopy } from "react-icons/rx";
import {useState} from "react"
import { CopyToClipboard } from "./CopyToClipboard";

export function TextItem({text}:{text:string}){

	const getText = () => text

	return (
		<>
			<p style={{display:"flex",alignItems:"end"}}>
				<CopyToClipboard getText={getText} name={"icon-wrapper"}/>
				<span style={{margin:"0.25rem 0.5rem"}} className="text">{text}</span>
			</p>
		</>
	)
}