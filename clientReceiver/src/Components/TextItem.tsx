
import { HiCheck } from "react-icons/hi2";
import { RxClipboardCopy } from "react-icons/rx";
import {useState} from "react"
import { CopyToClipboard } from "./CopyToClipboard";

export function TextItem({text}:{text:string}){

	const getText = () => text

	return (
		<>
			<CopyToClipboard getText={getText}/>
			<span style={{margin:"0.25rem 0.5rem"}}>{text}</span>
		</>
	)
}