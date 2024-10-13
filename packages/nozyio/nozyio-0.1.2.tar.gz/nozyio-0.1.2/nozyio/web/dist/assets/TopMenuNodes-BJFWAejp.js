import{j as e}from"./reactflow-vendor-DYfacRG4.js";import{B as m}from"./TopMenu-7mO9A9FQ.js";import{C as h}from"./CustomDrawer-CKyuU-vD.js";import{r as t}from"./react-vendor-CMZ2fpGT.js";import{b as x}from"./index-9ErzGo47.js";import{c as n,f,F as u}from"./shallow-D0wo54Jg.js";import{S as c}from"./Stack-1B6MSRlq.js";import"./react-syntax-highlighter-Ca70WVaL.js";/**
 * @license @tabler/icons-react v3.18.0 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */var v=n("outline","box","IconBox",[["path",{d:"M12 3l8 4.5l0 9l-8 4.5l-8 -4.5l0 -9l8 -4.5",key:"svg-0"}],["path",{d:"M12 12l8 -4.5",key:"svg-1"}],["path",{d:"M12 12l0 9",key:"svg-2"}],["path",{d:"M12 12l-8 -4.5",key:"svg-3"}]]);/**
 * @license @tabler/icons-react v3.18.0 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */var j=n("outline","brand-tabler","IconBrandTabler",[["path",{d:"M8 9l3 3l-3 3",key:"svg-0"}],["path",{d:"M13 15l3 0",key:"svg-1"}],["path",{d:"M4 4m0 4a4 4 0 0 1 4 -4h8a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h-8a4 4 0 0 1 -4 -4z",key:"svg-2"}]]);/**
 * @license @tabler/icons-react v3.18.0 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */var g=n("outline","folder","IconFolder",[["path",{d:"M5 4h4l3 3h7a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-11a2 2 0 0 1 2 -2",key:"svg-0"}]]);/**
 * @license @tabler/icons-react v3.18.0 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */var k=n("filled","triangle-inverted-filled","IconTriangleInvertedFilled",[["path",{d:"M20.118 3h-16.225a2.914 2.914 0 0 0 -2.503 4.371l8.116 13.549a2.917 2.917 0 0 0 4.987 .005l8.11 -13.539a2.914 2.914 0 0 0 -2.486 -4.386z",key:"svg-0"}]]);function p({path:r}){const[a,o]=t.useState([]),{setDropingNode:d}=x();return t.useEffect(()=>{f("/list_package_children?path="+encodeURIComponent(r)).then(s=>s.json()).then(s=>{o(s)})},[]),e.jsx("div",{className:"flex flex-col",children:e.jsx("div",{className:"flex flex-col",children:a.map(s=>{var i;return s.type==="folder"?e.jsx(y,{node:s},s.path):e.jsxs(c,{onClick:()=>{},children:[e.jsx(u,{children:e.jsx("p",{children:s.name})}),(i=s.functions)==null?void 0:i.map(l=>e.jsxs("div",{draggable:!0,onDragStart:N=>{console.log(l),d(l)},className:"flex flex-row items-center ml-3 gap-1 cursor-pointer hover:bg-secondary",children:[e.jsx(j,{size:16}),e.jsx("span",{children:l.name})]},s.path+"_"+l.name))]},s.type+"_"+s.name)})})})}function y({node:r}){const[a,o]=t.useState(!1);return e.jsxs(c,{className:"",children:[e.jsxs("div",{className:"flex flex-row items-center cursor-pointer",onClick:()=>o(!a),children:[e.jsx(k,{size:8,className:a?"mr-1":"-rotate-90 mr-1"}),e.jsx(g,{className:"mr-1"}),r.name]}),a&&e.jsx("div",{className:"ml-3",children:e.jsx(p,{path:r.path})})]})}function z(){const[r,a]=t.useState(!1);return e.jsxs(e.Fragment,{children:[e.jsx(m,{onClick:()=>a(!0),left:e.jsx(v,{size:18}),children:"Nodes"}),r&&e.jsx(h,{onClose:()=>a(!1),backdrop:null,children:e.jsxs(c,{className:"w-[400px] py-2 px-2 overflow-y-auto h-[100vh]",children:[e.jsx("h2",{className:"text-xl font-bold p-2",children:"Nodes"}),e.jsx(p,{path:""})]})})]})}export{z as default};
