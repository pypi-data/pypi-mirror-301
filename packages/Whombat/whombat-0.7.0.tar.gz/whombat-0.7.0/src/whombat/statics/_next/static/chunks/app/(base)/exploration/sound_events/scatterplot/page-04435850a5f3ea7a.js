(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[2959],{48187:function(e,t,n){Promise.resolve().then(n.bind(n,21002))},16463:function(e,t,n){"use strict";var s=n(71169);n.o(s,"notFound")&&n.d(t,{notFound:function(){return s.notFound}}),n.o(s,"usePathname")&&n.d(t,{usePathname:function(){return s.usePathname}}),n.o(s,"useRouter")&&n.d(t,{useRouter:function(){return s.useRouter}}),n.o(s,"useSearchParams")&&n.d(t,{useSearchParams:function(){return s.useSearchParams}}),n.o(s,"useSelectedLayoutSegment")&&n.d(t,{useSelectedLayoutSegment:function(){return s.useSelectedLayoutSegment}})},21002:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return v}});var s=n(57437),a=n(57818),r=n(2265),i=n(36920),o=n(22427),l=n(10336),d=n(39527),u=n(2312),c=n(5071),g=n(20206),x=n(26184),f=n(76845),m=n(58002),p=n(90840);let h=(0,a.default)(()=>Promise.all([n.e(5934),n.e(843)]).then(n.bind(n,70843)),{loadableGenerated:{webpack:()=>[70843]},ssr:!1});function v(){let[e,t]=(0,r.useState)(null),n=(0,m.Z)(),{items:a,pagination:o,total:l,query:{isLoading:u}}=(0,p.Z)({name:"sound_event_annotations_scatter_plot",queryFn:d.Z.soundEventAnnotations.getScatterPlotData,pageSize:1e3,filter:n});return(0,s.jsx)(c.Z,{isLoading:u,Pagination:(0,s.jsx)(i.Z,{pagination:o}),Counts:(0,s.jsx)(g.Z,{total:l,startIndex:o.page*o.pageSize,endIndex:Math.min((o.page+1)*o.pageSize,l)}),children:(0,s.jsxs)("div",{className:"grid grid-cols-2 gap-4",children:[(0,s.jsx)(h,{data:a,onClickSoundEvent:t,height:600}),(0,s.jsx)("div",{className:"col-start-2 h-full grow",children:null==e?(0,s.jsx)(x.Z,{outerClassName:"h-full",className:"h-full grow",children:"Select a sound event by clicking on the plot."}):(0,s.jsx)(j,{soundEvent:e,height:400})})]})})}function j(e){let{soundEvent:t,height:n}=e,{data:a,isLoading:r,error:i}=(0,l.Z)({uuid:t.uuid});return r?(0,s.jsx)(f.Z,{}):null==a?(0,s.jsx)(u.default,{error:i||void 0}):(0,s.jsx)(o.Z,{soundEventAnnotation:a,height:n})}},36920:function(e,t,n){"use strict";n.d(t,{Z:function(){return r}});var s=n(57437),a=n(24863);function r(e){let{pagination:t,pageSizeOptions:n}=e;return(0,s.jsx)(a.Z,{page:t.page,numPages:t.numPages,pageSize:t.pageSize,hasNextPage:t.hasNextPage,hasPrevPage:t.hasPrevPage,onNextPage:t.nextPage,onPrevPage:t.prevPage,onSetPage:t.setPage,onSetPageSize:t.setPageSize,pageSizeOptions:n})}},22427:function(e,t,n){"use strict";n.d(t,{Z:function(){return z}});var s=n(57437),a=n(97342),r=n(40402),i=n(2265),o=n(79001),l=n(35783),d=n(9486),u=n(34553),c=n(16471),g=n(63075),x=n(40014),f=n(24342),m=n(53744);function p(e){let{soundEventAnnotation:t,viewport:n,recording:a,audioSettings:r,spectrogramSettings:p,audio:h,spectrogramState:v,height:j=400,withAnnotations:w=!0,enabled:Z=!0}=e,{drawFn:S,...b}=(0,x.Z)({viewport:n,audio:h,state:v.mode,onZoom:v.enablePanning}),{drawFn:P}=(0,g.Z)({recording:a,audioSettings:r,spectrogramSettings:p}),N=(0,i.useMemo)(()=>w?[t]:[],[w,t]),y=(0,c.Z)({viewport:n.viewport,soundEvents:N}),k=(0,i.useCallback)((e,t)=>{P(e,t);let n=(0,m.f5)(h.currentTime,t,e.canvas.width);(0,f.Z)(e,n),S(e,t),y(e)},[h.currentTime,P,S,y]),C=(0,o.d)(b);return(0,s.jsx)(u.ZP,{soundEvents:N,viewport:n.viewport,SoundEventTags:l.Z,enabled:Z,children:(0,s.jsx)(d.Z,{viewport:n.viewport,height:j,drawFn:k,...C})})}var h=n(62135),v=n(68361),j=n(10336),w=n(96956),Z=n(51642),S=n(2289),b=n(2312),P=n(68097),N=n(76845),y=n(1010),k=n(49733),C=n(86811),E=n(72091);function z(e){let{soundEventAnnotation:t,...n}=e,{data:a=t,recording:r}=(0,j.Z)({uuid:t.uuid,soundEventAnnotation:t,withRecording:!0});return r.isLoading?(0,s.jsx)(N.Z,{}):null==r.data?(0,s.jsx)(b.default,{error:r.error||void 0}):(0,s.jsx)(_,{soundEventAnnotation:a,recording:r.data,...n})}function _(e){let{soundEventAnnotation:t,recording:n,height:o,withAnnotations:l=!0,withPlayer:d=!0,withControls:u=!0,withViewportBar:c=!0,withHotKeys:g=!0,enabled:x=!1}=e,f=(0,Z.Z)(),m=(0,S.Z)(),j=(0,k.Z)(),b=function(e){let{soundEvent:t,recording:n}=e,s=(0,i.useMemo)(()=>(0,E.ll)({geometry:t.geometry,recording:n,timeBuffer:.2}),[t.geometry,n]),a=(0,i.useMemo)(()=>(0,E.ll)({geometry:t.geometry,recording:n,timeBuffer:.1,freqBuffer:null}),[t.geometry,n]),r=(0,C.Z)({initial:a,bounds:s}),{set:o}=r;return(0,i.useEffect)(()=>{o(a)},[t.uuid,o]),r}({soundEvent:t.sound_event,recording:n}),N=(0,y.Z)({viewport:b,recording:n,audioSettings:f.settings});return(0,w.Z)({audio:N,viewport:b,spectrogramState:j,enabled:g}),(0,s.jsx)(P.Z,{ViewportToolbar:u?(0,s.jsx)(v.Z,{state:j,viewport:b}):void 0,Player:d?(0,s.jsx)(a.Z,{audio:N,samplerate:n.samplerate,onChangeSpeed:e=>f.dispatch({type:"setSpeed",speed:e})}):void 0,SettingsMenu:u?(0,s.jsx)(r.Z,{samplerate:n.samplerate,audioSettings:f,spectrogramSettings:m}):void 0,ViewportBar:c?(0,s.jsx)(h.Z,{viewport:b}):void 0,Canvas:(0,s.jsx)(p,{height:o,soundEventAnnotation:t,audioSettings:f.settings,spectrogramSettings:m.settings,spectrogramState:j,recording:n,audio:N,viewport:b,withAnnotations:l,enabled:x})})}},2312:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return d}});var s=n(57437),a=n(16463),r=n(90912),i=n(56541),o=n(79799);function l(e){let{error:t,onReset:n,onGoHome:a}=e;return(0,s.jsx)("div",{className:"flex flex-row justify-center items-center w-screen h-screen",children:(0,s.jsxs)("div",{className:"flex flex-col gap-2 items-center",children:[(0,s.jsx)(r.aN,{className:"w-32 h-32 text-red-500"}),(0,s.jsx)(o.H2,{className:"font-bold",children:"Oops! Something went wrong."}),(0,s.jsxs)("div",{className:"inline-flex gap-2 items-center",children:[(0,s.jsx)(i.Z,{mode:"text",variant:"warning",onClick:n,children:"Try Again"}),(0,s.jsx)(i.Z,{mode:"text",onClick:a,children:"Go Home"})]}),(0,s.jsxs)("div",{className:"flex flex-col items-center p-6 max-w-prose",children:[(0,s.jsx)("p",{className:"text-center text-stone-700 dark:text-stone-300",children:"We encountered an issue. Please reach out to our developers and provide details on what you were doing. Include the following error message for assistance:"}),(0,s.jsx)("span",{className:"p-4 max-w-prose text-red-500 whitespace-pre-wrap",children:null==t?void 0:t.message})]})]})})}function d(){let{error:e,reset:t}=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},n=(0,a.useRouter)();return(0,s.jsx)(l,{error:e,onReset:t,onGoHome:()=>n.push("/")})}},96956:function(e,t,n){"use strict";n.d(t,{Z:function(){return a}});var s=n(23627);function a(e){let{audio:t,spectrogramState:n,viewport:a,enabled:r=!0}=e;(0,s.y1)("space",t.togglePlay,{preventDefault:!0,description:"Toggle playing",enabled:r}),(0,s.y1)("z",n.enableZooming,{description:"Enable spectrogram zooming",enabled:r}),(0,s.y1)("x",n.enablePanning,{description:"Enable spectrogram panning",enabled:r}),(0,s.y1)("b",a.back,{description:"Go back to previous view",enabled:r})}},5071:function(e,t,n){"use strict";n.d(t,{Z:function(){return r}});var s=n(57437),a=n(76845);function r(e){return(0,s.jsxs)("div",{className:"flex flex-col gap-4 p-2",children:[null!=e.Filtering&&(0,s.jsx)("div",{className:"flex top-0 z-50 flex-row justify-between items-center dark:bg-stone-900",children:e.Filtering}),(0,s.jsxs)("div",{className:"flex sticky top-0 z-50 flex-row justify-between items-center dark:bg-stone-900",children:[e.Counts,e.Pagination]}),(0,s.jsx)("div",{className:"p-4",children:e.isLoading?(0,s.jsx)(a.Z,{}):e.children})]})}},20206:function(e,t,n){"use strict";n.d(t,{Z:function(){return a}});var s=n(57437);function a(e){return(0,s.jsx)("div",{children:(0,s.jsxs)("span",{className:"text-stone-500",children:["Showing"," ",(0,s.jsxs)("span",{className:"font-bold",children:[e.startIndex," - ",e.endIndex]})," ","out of ",(0,s.jsx)("span",{className:"font-bold text-emerald-500",children:e.total})," "]})})}},24863:function(e,t,n){"use strict";n.d(t,{Z:function(){return d}});var s=n(57437),a=n(90912),r=n(91614),i=n(92369),o=n(56541);let l=[1,5,10,25,50,100];function d(e){let{page:t=0,numPages:n=1,pageSize:r=10,hasNextPage:d=!1,hasPrevPage:c=!1,onNextPage:g,onPrevPage:x,onSetPage:f,onSetPageSize:m,pageSizeOptions:p=l}=e;return(0,s.jsxs)("div",{className:"flex flex-row space-x-2",children:[(0,s.jsx)(o.Z,{disabled:0===t,onClick:()=>null==f?void 0:f(0),variant:"secondary",mode:"text",children:(0,s.jsx)(a.Op,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,s.jsx)(o.Z,{onClick:x,disabled:!c,variant:"secondary",mode:"text",children:(0,s.jsx)(a.jJ,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,s.jsx)("div",{className:"w-14",children:(0,s.jsx)(i.II,{disabled:1===n,type:"number",className:"remove-arrow",value:t+1,onChange:e=>null==f?void 0:f(parseInt(e.target.value)-1)})}),(0,s.jsxs)(o.Z,{disabled:!0,variant:"secondary",mode:"text",children:["/ ",n]}),(0,s.jsx)(o.Z,{onClick:g,disabled:!d,variant:"secondary",mode:"text",children:(0,s.jsx)(a.Ne,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,s.jsx)(o.Z,{disabled:t===n-1,onClick:()=>null==f?void 0:f(n-1),variant:"secondary",mode:"text",children:(0,s.jsx)(a.OZ,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,s.jsx)(u,{pageSize:r,onSetPageSize:m,pageSizeOptions:p})]})}function u(e){let{pageSize:t=10,onSetPageSize:n,pageSizeOptions:a=l}=e;return(0,s.jsx)(r.Z,{label:"Page Size:",selected:{label:t.toString(),value:t,id:t},onChange:e=>null==n?void 0:n(e),options:a.map(e=>({label:e.toString(),value:e,id:e}))})}},26184:function(e,t,n){"use strict";n.d(t,{Z:function(){return i}});var s=n(57437),a=n(56800),r=n.n(a);function i(e){let{children:t,outerClassName:n="p-8",className:a}=e;return(0,s.jsx)("div",{className:"".concat(n," w-full"),children:(0,s.jsx)("div",{className:r()(a,"flex flex-col justify-center items-center p-4 w-full text-center rounded-md border border-dashed border-stone-500 text-stone-500"),children:t})})}},76057:function(e,t,n){"use strict";var s=n(2265);let a=s.forwardRef(function(e,t){let{title:n,titleId:a,...r}=e;return s.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 20 20",fill:"currentColor","aria-hidden":"true","data-slot":"icon",ref:t,"aria-labelledby":a},r),n?s.createElement("title",{id:a},n):null,s.createElement("path",{fillRule:"evenodd",d:"M10.53 3.47a.75.75 0 0 0-1.06 0L6.22 6.72a.75.75 0 0 0 1.06 1.06L10 5.06l2.72 2.72a.75.75 0 1 0 1.06-1.06l-3.25-3.25Zm-4.31 9.81 3.25 3.25a.75.75 0 0 0 1.06 0l3.25-3.25a.75.75 0 1 0-1.06-1.06L10 14.94l-2.72-2.72a.75.75 0 0 0-1.06 1.06Z",clipRule:"evenodd"}))});t.Z=a}},function(e){e.O(0,[5501,7819,5660,9772,8472,1336,5657,9226,932,6259,3215,4880,2817,6151,152,8026,7068,9527,4593,3516,2962,357,2971,7023,1744],function(){return e(e.s=48187)}),_N_E=e.O()}]);