// ==UserScript==
// @name        Add clipboard copy
// @namespace   Violentmonkey Scripts
// @grant       none
// @version     1.0
// @author      -
// @grant       GM_setClipboard
// @description 2/18/2024, 11:58:10 PM
// @match       https://192.168.*.*/
// ==/UserScript==


function getText(){
	const selection = window.getSelection()
	if(selection && selection.toString().length > 0){
	  const selectedText = selection.toString()
	  return selectedText.toString()
	}
  }
  
  
  (function(){
	'use strict'
  
	var oldLen = 0
  
	setInterval(()=>{
  
	  const iconWrappers = document.querySelectorAll(".icon-wrapper")
	  if (oldLen !== iconWrappers.length){
		console.log("Update!")
		for(let i=0;i<iconWrappers.length;i++){
		  const element = iconWrappers[i]
		  element.onclick = () => {
			GM_setClipboard(element.parentNode.querySelector(".text").textContent);
		  }
		}
	  }
	  oldLen = iconWrappers.length
  
  
	  const iconWrapperSelector = document.querySelectorAll(".icon-wrapper-selector")[0]
	  if(iconWrapperSelector){
		iconWrapperSelector.onclick = () => {
		  GM_setClipboard(getText())
		}
	  }
	},50)
  })()