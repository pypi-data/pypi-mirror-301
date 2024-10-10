/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Version: 0.33.0(4b1abad427e58dbedc1215d99a0902ffc885fcd4)
 * Released under the MIT license
 * https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt
 *-----------------------------------------------------------------------------*/
define("vs/basic-languages/fsharp/fsharp", ["require","require"],(require)=>{
var moduleExports=(()=>{var s=Object.defineProperty;var r=Object.getOwnPropertyDescriptor;var a=Object.getOwnPropertyNames;var l=Object.prototype.hasOwnProperty;var c=n=>s(n,"__esModule",{value:!0});var g=(n,e)=>{for(var t in e)s(n,t,{get:e[t],enumerable:!0})},f=(n,e,t,i)=>{if(e&&typeof e=="object"||typeof e=="function")for(let o of a(e))!l.call(n,o)&&(t||o!=="default")&&s(n,o,{get:()=>e[o],enumerable:!(i=r(e,o))||i.enumerable});return n};var m=(n=>(e,t)=>n&&n.get(e)||(t=f(c({}),e,1),n&&n.set(e,t),t))(typeof WeakMap!="undefined"?new WeakMap:0);var p={};g(p,{conf:()=>u,language:()=>d});var u={comments:{lineComment:"//",blockComment:["(*","*)"]},brackets:[["{","}"],["[","]"],["(",")"]],autoClosingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:'"',close:'"'}],surroundingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:'"',close:'"'},{open:"'",close:"'"}],folding:{markers:{start:new RegExp("^\\s*//\\s*#region\\b|^\\s*\\(\\*\\s*#region(.*)\\*\\)"),end:new RegExp("^\\s*//\\s*#endregion\\b|^\\s*\\(\\*\\s*#endregion\\s*\\*\\)")}}},d={defaultToken:"",tokenPostfix:".fs",keywords:["abstract","and","atomic","as","assert","asr","base","begin","break","checked","component","const","constraint","constructor","continue","class","default","delegate","do","done","downcast","downto","elif","else","end","exception","eager","event","external","extern","false","finally","for","fun","function","fixed","functor","global","if","in","include","inherit","inline","interface","internal","land","lor","lsl","lsr","lxor","lazy","let","match","member","mod","module","mutable","namespace","method","mixin","new","not","null","of","open","or","object","override","private","parallel","process","protected","pure","public","rec","return","static","sealed","struct","sig","then","to","true","tailcall","trait","try","type","upcast","use","val","void","virtual","volatile","when","while","with","yield"],symbols:/[=><!~?:&|+\-*\^%;\.,\/]+/,escapes:/\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,integersuffix:/[uU]?[yslnLI]?/,floatsuffix:/[fFmM]?/,tokenizer:{root:[[/[a-zA-Z_]\w*/,{cases:{"@keywords":{token:"keyword.$0"},"@default":"identifier"}}],{include:"@whitespace"},[/\[<.*>\]/,"annotation"],[/^#(if|else|endif)/,"keyword"],[/[{}()\[\]]/,"@brackets"],[/[<>](?!@symbols)/,"@brackets"],[/@symbols/,"delimiter"],[/\d*\d+[eE]([\-+]?\d+)?(@floatsuffix)/,"number.float"],[/\d*\.\d+([eE][\-+]?\d+)?(@floatsuffix)/,"number.float"],[/0x[0-9a-fA-F]+LF/,"number.float"],[/0x[0-9a-fA-F]+(@integersuffix)/,"number.hex"],[/0b[0-1]+(@integersuffix)/,"number.bin"],[/\d+(@integersuffix)/,"number"],[/[;,.]/,"delimiter"],[/"([^"\\]|\\.)*$/,"string.invalid"],[/"""/,"string",'@string."""'],[/"/,"string",'@string."'],[/\@"/,{token:"string.quote",next:"@litstring"}],[/'[^\\']'B?/,"string"],[/(')(@escapes)(')/,["string","string.escape","string"]],[/'/,"string.invalid"]],whitespace:[[/[ \t\r\n]+/,""],[/\(\*(?!\))/,"comment","@comment"],[/\/\/.*$/,"comment"]],comment:[[/[^*(]+/,"comment"],[/\*\)/,"comment","@pop"],[/\*/,"comment"],[/\(\*\)/,"comment"],[/\(/,"comment"]],string:[[/[^\\"]+/,"string"],[/@escapes/,"string.escape"],[/\\./,"string.escape.invalid"],[/("""|"B?)/,{cases:{"$#==$S2":{token:"string",next:"@pop"},"@default":"string"}}]],litstring:[[/[^"]+/,"string"],[/""/,"string.escape"],[/"/,{token:"string.quote",next:"@pop"}]]}};return m(p);})();
return moduleExports;
});
