"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[2078],{16463:function(e,t,r){var n=r(71169);r.o(n,"notFound")&&r.d(t,{notFound:function(){return n.notFound}}),r.o(n,"usePathname")&&r.d(t,{usePathname:function(){return n.usePathname}}),r.o(n,"useRouter")&&r.d(t,{useRouter:function(){return n.useRouter}}),r.o(n,"useSearchParams")&&r.d(t,{useSearchParams:function(){return n.useSearchParams}}),r.o(n,"useSelectedLayoutSegment")&&r.d(t,{useSelectedLayoutSegment:function(){return n.useSelectedLayoutSegment}})},49896:function(e,t,r){let n,u;r.d(t,{J:function(){return L}});var o=r(2265),a=r(22934),l=r(6584),s=r(20635),c=r(72955),i=r(61463),p=r(88703),d=r(39110),f=r(62707),v=r(75180),P=r(4707),h=r(41469),m=r(45959),E=r(89080),C=r(53509),b=r(47986),y=r(19309),S=r(5583),g=r(91498),T=r(3600),B=r(7551),I=((n=I||{})[n.Open=0]="Open",n[n.Closed=1]="Closed",n),O=((u=O||{})[u.TogglePopover=0]="TogglePopover",u[u.ClosePopover=1]="ClosePopover",u[u.SetButton=2]="SetButton",u[u.SetButtonId=3]="SetButtonId",u[u.SetPanel=4]="SetPanel",u[u.SetPanelId=5]="SetPanelId",u);let R={0:e=>{let t={...e,popoverState:(0,S.E)(e.popoverState,{0:1,1:0})};return 0===t.popoverState&&(t.__demoMode=!1),t},1:e=>1===e.popoverState?e:{...e,popoverState:1},2:(e,t)=>e.button===t.button?e:{...e,button:t.button},3:(e,t)=>e.buttonId===t.buttonId?e:{...e,buttonId:t.buttonId},4:(e,t)=>e.panel===t.panel?e:{...e,panel:t.panel},5:(e,t)=>e.panelId===t.panelId?e:{...e,panelId:t.panelId}},D=(0,o.createContext)(null);function k(e){let t=(0,o.useContext)(D);if(null===t){let t=Error("<".concat(e," /> is missing a parent <Popover /> component."));throw Error.captureStackTrace&&Error.captureStackTrace(t,k),t}return t}D.displayName="PopoverContext";let x=(0,o.createContext)(null);function M(e){let t=(0,o.useContext)(x);if(null===t){let t=Error("<".concat(e," /> is missing a parent <Popover /> component."));throw Error.captureStackTrace&&Error.captureStackTrace(t,M),t}return t}x.displayName="PopoverAPIContext";let N=(0,o.createContext)(null);function F(){return(0,o.useContext)(N)}N.displayName="PopoverGroupContext";let w=(0,o.createContext)(null);function A(e,t){return(0,S.E)(t.type,R,e,t)}w.displayName="PopoverPanelContext";let z=T.AN.RenderStrategy|T.AN.Static,_=T.AN.RenderStrategy|T.AN.Static,L=Object.assign((0,T.yV)(function(e,t){var r;let{__demoMode:n=!1,...u}=e,c=(0,o.useRef)(null),i=(0,h.T)(t,(0,h.h)(e=>{c.current=e})),v=(0,o.useRef)([]),m=(0,o.useReducer)(A,{__demoMode:n,popoverState:n?0:1,buttons:v,button:null,buttonId:null,panel:null,panelId:null,beforePanelSentinel:(0,o.createRef)(),afterPanelSentinel:(0,o.createRef)()}),[{popoverState:E,button:b,buttonId:g,panel:B,panelId:I,beforePanelSentinel:O,afterPanelSentinel:R},k]=m,M=(0,f.i)(null!=(r=c.current)?r:b),N=(0,o.useMemo)(()=>{if(!b||!B)return!1;for(let e of document.querySelectorAll("body > *"))if(Number(null==e?void 0:e.contains(b))^Number(null==e?void 0:e.contains(B)))return!0;let e=(0,y.GO)(),t=e.indexOf(b),r=(t+e.length-1)%e.length,n=(t+1)%e.length,u=e[r],o=e[n];return!B.contains(u)&&!B.contains(o)},[b,B]),z=(0,p.E)(g),_=(0,p.E)(I),L=(0,o.useMemo)(()=>({buttonId:z,panelId:_,close:()=>k({type:1})}),[z,_,k]),V=F(),j=null==V?void 0:V.registerPopover,G=(0,l.z)(()=>{var e;return null!=(e=null==V?void 0:V.isFocusWithinPopoverGroup())?e:(null==M?void 0:M.activeElement)&&((null==b?void 0:b.contains(M.activeElement))||(null==B?void 0:B.contains(M.activeElement)))});(0,o.useEffect)(()=>null==j?void 0:j(L),[j,L]);let[K,Z]=(0,a.k)(),Y=(0,P.v)({mainTreeNodeRef:null==V?void 0:V.mainTreeNodeRef,portals:K,defaultContainers:[b,B]});(0,s.O)(null==M?void 0:M.defaultView,"focus",e=>{var t,r,n,u;e.target!==window&&e.target instanceof HTMLElement&&0===E&&(G()||b&&B&&(Y.contains(e.target)||null!=(r=null==(t=O.current)?void 0:t.contains)&&r.call(t,e.target)||null!=(u=null==(n=R.current)?void 0:n.contains)&&u.call(n,e.target)||k({type:1})))},!0),(0,d.O)(Y.resolveContainers,(e,t)=>{k({type:1}),(0,y.sP)(t,y.tJ.Loose)||(e.preventDefault(),null==b||b.focus())},0===E);let H=(0,l.z)(e=>{k({type:1});let t=e?e instanceof HTMLElement?e:"current"in e&&e.current instanceof HTMLElement?e.current:b:b;null==t||t.focus()}),q=(0,o.useMemo)(()=>({close:H,isPortalled:N}),[H,N]),J=(0,o.useMemo)(()=>({open:0===E,close:H}),[E,H]);return o.createElement(w.Provider,{value:null},o.createElement(D.Provider,{value:m},o.createElement(x.Provider,{value:q},o.createElement(C.up,{value:(0,S.E)(E,{0:C.ZM.Open,1:C.ZM.Closed})},o.createElement(Z,null,(0,T.sY)({ourProps:{ref:i},theirProps:u,slot:J,defaultTag:"div",name:"Popover"}),o.createElement(Y.MainTreeNode,null))))))}),{Button:(0,T.yV)(function(e,t){let r=(0,c.M)(),{id:n="headlessui-popover-button-".concat(r),...u}=e,[a,s]=k("Popover.Button"),{isPortalled:i}=M("Popover.Button"),p=(0,o.useRef)(null),d="headlessui-focus-sentinel-".concat((0,c.M)()),P=F(),C=null==P?void 0:P.closeOthers,g=null!==(0,o.useContext)(w);(0,o.useEffect)(()=>{if(!g)return s({type:3,buttonId:n}),()=>{s({type:3,buttonId:null})}},[g,n,s]);let[I]=(0,o.useState)(()=>Symbol()),O=(0,h.T)(p,t,g?null:e=>{if(e)a.buttons.current.push(I);else{let e=a.buttons.current.indexOf(I);-1!==e&&a.buttons.current.splice(e,1)}a.buttons.current.length>1&&console.warn("You are already using a <Popover.Button /> but only 1 <Popover.Button /> is supported."),e&&s({type:2,button:e})}),R=(0,h.T)(p,t),D=(0,f.i)(p),x=(0,l.z)(e=>{var t,r,n;if(g){if(1===a.popoverState)return;switch(e.key){case B.R.Space:case B.R.Enter:e.preventDefault(),null==(r=(t=e.target).click)||r.call(t),s({type:1}),null==(n=a.button)||n.focus()}}else switch(e.key){case B.R.Space:case B.R.Enter:e.preventDefault(),e.stopPropagation(),1===a.popoverState&&(null==C||C(a.buttonId)),s({type:0});break;case B.R.Escape:if(0!==a.popoverState)return null==C?void 0:C(a.buttonId);if(!p.current||null!=D&&D.activeElement&&!p.current.contains(D.activeElement))return;e.preventDefault(),e.stopPropagation(),s({type:1})}}),N=(0,l.z)(e=>{g||e.key===B.R.Space&&e.preventDefault()}),A=(0,l.z)(t=>{var r,n;(0,b.P)(t.currentTarget)||e.disabled||(g?(s({type:1}),null==(r=a.button)||r.focus()):(t.preventDefault(),t.stopPropagation(),1===a.popoverState&&(null==C||C(a.buttonId)),s({type:0}),null==(n=a.button)||n.focus()))}),z=(0,l.z)(e=>{e.preventDefault(),e.stopPropagation()}),_=0===a.popoverState,L=(0,o.useMemo)(()=>({open:_}),[_]),V=(0,v.f)(e,p),j=g?{ref:R,type:V,onKeyDown:x,onClick:A}:{ref:O,id:a.buttonId,type:V,"aria-expanded":0===a.popoverState,"aria-controls":a.panel?a.panelId:void 0,onKeyDown:x,onKeyUp:N,onClick:A,onMouseDown:z},G=(0,m.l)(),K=(0,l.z)(()=>{let e=a.panel;e&&(0,S.E)(G.current,{[m.N.Forwards]:()=>(0,y.jA)(e,y.TO.First),[m.N.Backwards]:()=>(0,y.jA)(e,y.TO.Last)})===y.fE.Error&&(0,y.jA)((0,y.GO)().filter(e=>"true"!==e.dataset.headlessuiFocusGuard),(0,S.E)(G.current,{[m.N.Forwards]:y.TO.Next,[m.N.Backwards]:y.TO.Previous}),{relativeTo:a.button})});return o.createElement(o.Fragment,null,(0,T.sY)({ourProps:j,theirProps:u,slot:L,defaultTag:"button",name:"Popover.Button"}),_&&!g&&i&&o.createElement(E._,{id:d,features:E.A.Focusable,"data-headlessui-focus-guard":!0,as:"button",type:"button",onFocus:K}))}),Overlay:(0,T.yV)(function(e,t){let r=(0,c.M)(),{id:n="headlessui-popover-overlay-".concat(r),...u}=e,[{popoverState:a},s]=k("Popover.Overlay"),i=(0,h.T)(t),p=(0,C.oJ)(),d=null!==p?(p&C.ZM.Open)===C.ZM.Open:0===a,f=(0,l.z)(e=>{if((0,b.P)(e.currentTarget))return e.preventDefault();s({type:1})}),v=(0,o.useMemo)(()=>({open:0===a}),[a]);return(0,T.sY)({ourProps:{ref:i,id:n,"aria-hidden":!0,onClick:f},theirProps:u,slot:v,defaultTag:"div",features:z,visible:d,name:"Popover.Overlay"})}),Panel:(0,T.yV)(function(e,t){let r=(0,c.M)(),{id:n="headlessui-popover-panel-".concat(r),focus:u=!1,...a}=e,[s,p]=k("Popover.Panel"),{close:d,isPortalled:v}=M("Popover.Panel"),P="headlessui-focus-sentinel-before-".concat((0,c.M)()),b="headlessui-focus-sentinel-after-".concat((0,c.M)()),g=(0,o.useRef)(null),I=(0,h.T)(g,t,e=>{p({type:4,panel:e})}),O=(0,f.i)(g),R=(0,T.Y2)();(0,i.e)(()=>(p({type:5,panelId:n}),()=>{p({type:5,panelId:null})}),[n,p]);let D=(0,C.oJ)(),x=null!==D?(D&C.ZM.Open)===C.ZM.Open:0===s.popoverState,N=(0,l.z)(e=>{var t;if(e.key===B.R.Escape){if(0!==s.popoverState||!g.current||null!=O&&O.activeElement&&!g.current.contains(O.activeElement))return;e.preventDefault(),e.stopPropagation(),p({type:1}),null==(t=s.button)||t.focus()}});(0,o.useEffect)(()=>{var t;e.static||1===s.popoverState&&(null==(t=e.unmount)||t)&&p({type:4,panel:null})},[s.popoverState,e.unmount,e.static,p]),(0,o.useEffect)(()=>{if(s.__demoMode||!u||0!==s.popoverState||!g.current)return;let e=null==O?void 0:O.activeElement;g.current.contains(e)||(0,y.jA)(g.current,y.TO.First)},[s.__demoMode,u,g,s.popoverState]);let F=(0,o.useMemo)(()=>({open:0===s.popoverState,close:d}),[s,d]),A={ref:I,id:n,onKeyDown:N,onBlur:u&&0===s.popoverState?e=>{var t,r,n,u,o;let a=e.relatedTarget;a&&g.current&&(null!=(t=g.current)&&t.contains(a)||(p({type:1}),(null!=(n=null==(r=s.beforePanelSentinel.current)?void 0:r.contains)&&n.call(r,a)||null!=(o=null==(u=s.afterPanelSentinel.current)?void 0:u.contains)&&o.call(u,a))&&a.focus({preventScroll:!0})))}:void 0,tabIndex:-1},z=(0,m.l)(),L=(0,l.z)(()=>{let e=g.current;e&&(0,S.E)(z.current,{[m.N.Forwards]:()=>{var t;(0,y.jA)(e,y.TO.First)===y.fE.Error&&(null==(t=s.afterPanelSentinel.current)||t.focus())},[m.N.Backwards]:()=>{var e;null==(e=s.button)||e.focus({preventScroll:!0})}})}),V=(0,l.z)(()=>{let e=g.current;e&&(0,S.E)(z.current,{[m.N.Forwards]:()=>{var e;if(!s.button)return;let t=(0,y.GO)(),r=t.indexOf(s.button),n=t.slice(0,r+1),u=[...t.slice(r+1),...n];for(let t of u.slice())if("true"===t.dataset.headlessuiFocusGuard||null!=(e=s.panel)&&e.contains(t)){let e=u.indexOf(t);-1!==e&&u.splice(e,1)}(0,y.jA)(u,y.TO.First,{sorted:!1})},[m.N.Backwards]:()=>{var t;(0,y.jA)(e,y.TO.Previous)===y.fE.Error&&(null==(t=s.button)||t.focus())}})});return o.createElement(w.Provider,{value:n},x&&v&&o.createElement(E._,{id:P,ref:s.beforePanelSentinel,features:E.A.Focusable,"data-headlessui-focus-guard":!0,as:"button",type:"button",onFocus:L}),(0,T.sY)({mergeRefs:R,ourProps:A,theirProps:a,slot:F,defaultTag:"div",features:_,visible:x,name:"Popover.Panel"}),x&&v&&o.createElement(E._,{id:b,ref:s.afterPanelSentinel,features:E.A.Focusable,"data-headlessui-focus-guard":!0,as:"button",type:"button",onFocus:V}))}),Group:(0,T.yV)(function(e,t){let r=(0,o.useRef)(null),n=(0,h.T)(r,t),[u,a]=(0,o.useState)([]),s=(0,P.H)(),c=(0,l.z)(e=>{a(t=>{let r=t.indexOf(e);if(-1!==r){let e=t.slice();return e.splice(r,1),e}return t})}),i=(0,l.z)(e=>(a(t=>[...t,e]),()=>c(e))),p=(0,l.z)(()=>{var e;let t=(0,g.r)(r);if(!t)return!1;let n=t.activeElement;return!!(null!=(e=r.current)&&e.contains(n))||u.some(e=>{var r,u;return(null==(r=t.getElementById(e.buttonId.current))?void 0:r.contains(n))||(null==(u=t.getElementById(e.panelId.current))?void 0:u.contains(n))})}),d=(0,l.z)(e=>{for(let t of u)t.buttonId.current!==e&&t.close()}),f=(0,o.useMemo)(()=>({registerPopover:i,unregisterPopover:c,isFocusWithinPopoverGroup:p,closeOthers:d,mainTreeNodeRef:s.mainTreeNodeRef}),[i,c,p,d,s.mainTreeNodeRef]),v=(0,o.useMemo)(()=>({}),[]);return o.createElement(N.Provider,{value:f},(0,T.sY)({ourProps:{ref:n},theirProps:e,slot:v,defaultTag:"div",name:"Popover.Group"}),o.createElement(s.MainTreeNode,null))})})},70407:function(e,t,r){r.d(t,{t:function(){return l}});var n={};n={"ar-AE":{"Clear search":`\u{645}\u{633}\u{62D} \u{627}\u{644}\u{628}\u{62D}\u{62B}`},"bg-BG":{"Clear search":`\u{418}\u{437}\u{447}\u{438}\u{441}\u{442}\u{432}\u{430}\u{43D}\u{435} \u{43D}\u{430} \u{442}\u{44A}\u{440}\u{441}\u{435}\u{43D}\u{435}`},"cs-CZ":{"Clear search":`Vymazat hled\xe1n\xed`},"da-DK":{"Clear search":`Ryd s\xf8gning`},"de-DE":{"Clear search":`Suche zur\xfccksetzen`},"el-GR":{"Clear search":`\u{391}\u{3C0}\u{3B1}\u{3BB}\u{3BF}\u{3B9}\u{3C6}\u{3AE} \u{3B1}\u{3BD}\u{3B1}\u{3B6}\u{3AE}\u{3C4}\u{3B7}\u{3C3}\u{3B7}\u{3C2}`},"en-US":{"Clear search":"Clear search"},"es-ES":{"Clear search":`Borrar b\xfasqueda`},"et-EE":{"Clear search":`T\xfchjenda otsing`},"fi-FI":{"Clear search":`Tyhjenn\xe4 haku`},"fr-FR":{"Clear search":"Effacer la recherche"},"he-IL":{"Clear search":`\u{5E0}\u{5E7}\u{5D4} \u{5D7}\u{5D9}\u{5E4}\u{5D5}\u{5E9}`},"hr-HR":{"Clear search":`Obri\u{161}i pretragu`},"hu-HU":{"Clear search":`Keres\xe9s t\xf6rl\xe9se`},"it-IT":{"Clear search":"Cancella ricerca"},"ja-JP":{"Clear search":`\u{691C}\u{7D22}\u{3092}\u{30AF}\u{30EA}\u{30A2}`},"ko-KR":{"Clear search":`\u{AC80}\u{C0C9} \u{C9C0}\u{C6B0}\u{AE30}`},"lt-LT":{"Clear search":`I\u{161}valyti ie\u{161}k\u{105}`},"lv-LV":{"Clear search":`Not\u{12B}r\u{12B}t mekl\u{113}\u{161}anu`},"nb-NO":{"Clear search":`T\xf8m s\xf8k`},"nl-NL":{"Clear search":"Zoekactie wissen"},"pl-PL":{"Clear search":`Wyczy\u{15B}\u{107} zawarto\u{15B}\u{107} wyszukiwania`},"pt-BR":{"Clear search":"Limpar pesquisa"},"pt-PT":{"Clear search":"Limpar pesquisa"},"ro-RO":{"Clear search":`\u{15E}terge\u{163}i c\u{103}utarea`},"ru-RU":{"Clear search":`\u{41E}\u{447}\u{438}\u{441}\u{442}\u{438}\u{442}\u{44C} \u{43F}\u{43E}\u{438}\u{441}\u{43A}`},"sk-SK":{"Clear search":`Vymaza\u{165} vyh\u{13E}ad\xe1vanie`},"sl-SI":{"Clear search":`Po\u{10D}isti iskanje`},"sr-SP":{"Clear search":`Obri\u{161}i pretragu`},"sv-SE":{"Clear search":`Rensa s\xf6kning`},"tr-TR":{"Clear search":`Aramay\u{131} temizle`},"uk-UA":{"Clear search":`\u{41E}\u{447}\u{438}\u{441}\u{442}\u{438}\u{442}\u{438} \u{43F}\u{43E}\u{448}\u{443}\u{43A}`},"zh-CN":{"Clear search":`\u{6E05}\u{9664}\u{641C}\u{7D22}`},"zh-TW":{"Clear search":`\u{6E05}\u{9664}\u{641C}\u{5C0B}\u{689D}\u{4EF6}`}};var u=r(5722),o=r(79822),a=r(45657);function l(e,t,r){var l;let s=(0,o.q)((l=n)&&l.__esModule?l.default:l,"@react-aria/searchfield"),{isDisabled:c,isReadOnly:i,onSubmit:p,onClear:d,type:f="search"}=e,{labelProps:v,inputProps:P,descriptionProps:h,errorMessageProps:m,...E}=(0,a.h)({...e,value:t.value,onChange:t.setValue,onKeyDown:i?e.onKeyDown:(0,u.t)(e=>{let r=e.key;"Enter"===r&&(c||i)&&e.preventDefault(),c||i||("Enter"===r&&p&&(e.preventDefault(),p(t.value)),"Escape"===r&&(""===t.value?e.continuePropagation():(t.setValue(""),d&&d())))},e.onKeyDown),type:f},r);return{labelProps:v,inputProps:{...P,defaultValue:void 0},clearButtonProps:{"aria-label":s.format("Clear search"),excludeFromTabOrder:!0,preventFocusOnPress:!0,isDisabled:c||i,onPress:()=>{t.setValue(""),d&&d()},onPressStart:()=>{var e;null===(e=r.current)||void 0===e||e.focus()}},descriptionProps:h,errorMessageProps:m,...E}}},93272:function(e,t,r){r.d(t,{c:function(){return u}});var n=r(41821);function u(e){let[t,r]=(0,n.z)(o(e.value),o(e.defaultValue)||"",e.onChange);return{value:t,setValue:r}}function o(e){if(null!=e)return e.toString()}}}]);