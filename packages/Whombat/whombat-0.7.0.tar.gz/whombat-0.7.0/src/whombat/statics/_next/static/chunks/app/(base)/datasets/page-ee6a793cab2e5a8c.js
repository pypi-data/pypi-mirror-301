(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[5198],{86395:function(e,t,a){Promise.resolve().then(a.bind(a,44416))},44416:function(e,t,a){"use strict";a.r(t),a.d(t,{default:function(){return D}});var n=a(57437),s=a(16463),l=a(2265),i=a(36920),r=a(25524),o=a(88726),c=a(39527),d=a(31014),u=a(39343),x=a(92369),m=a(42907);function h(e){var t,a,s;let{onCreateDataset:i}=e,{register:r,handleSubmit:o,formState:{errors:c}}=(0,u.cI)({resolver:(0,d.F)(m.SR),mode:"onChange"}),h=(0,l.useCallback)(e=>{null==i||i(e)},[i]);return(0,n.jsxs)("form",{className:"flex flex-col gap-4",onSubmit:o(h),children:[(0,n.jsx)(x.ZA,{name:"name",label:"Name",help:"Please provide a name for the dataset.",error:null===(t=c.name)||void 0===t?void 0:t.message,children:(0,n.jsx)(x.II,{...r("name")})}),(0,n.jsx)(x.ZA,{name:"description",label:"Description",help:"Describe the dataset.",error:null===(a=c.description)||void 0===a?void 0:a.message,children:(0,n.jsx)(x.Kx,{...r("description")})}),(0,n.jsx)(x.ZA,{name:"audio_dir",label:"Audio Directory",help:"Provide the path to the folder where the dataset recordings reside.",error:null===(s=c.name)||void 0===s?void 0:s.message,children:(0,n.jsx)(x.II,{...r("audio_dir")})}),(0,n.jsx)("div",{className:"mb-3",children:(0,n.jsx)(x.k4,{children:"Create Dataset"})})]})}function f(e){let{onCreateDataset:t,onError:a}=e,{mutateAsync:s}=(0,r.D)({mutationFn:c.Z.datasets.create,onError:a,onSuccess:t}),i=(0,l.useCallback)(async e=>{o.ZP.promise(s(e),{loading:"Creating dataset. Scanning files and creating metadata, please wait...",success:"Dataset created",error:"Failed to create dataset"})},[s]);return(0,n.jsx)(h,{onCreateDataset:i})}var j=a(90912);function v(e){var t,a,s;let{onImportDataset:i}=e,{register:r,handleSubmit:o,formState:{errors:c}}=(0,u.cI)({resolver:(0,d.F)(m.pz),mode:"onChange"}),h=(0,l.useCallback)(e=>{null==i||i(e)},[i]);return(0,n.jsxs)("form",{className:"flex flex-col gap-4",onSubmit:o(h),children:[(0,n.jsx)(x.ZA,{name:"dataset",label:"Select a dataset file to import",help:"The file must be in AOEF format",error:null===(a=c.dataset)||void 0===a?void 0:null===(t=a.message)||void 0===t?void 0:t.toString(),children:(0,n.jsx)(x.II,{type:"file",...r("dataset"),required:!0,multiple:!1,accept:"application/json"})}),(0,n.jsx)(x.ZA,{name:"audio_dir",label:"Audio directory",help:"Folder where all the dataset recordings are stored",error:null===(s=c.audio_dir)||void 0===s?void 0:s.message,children:(0,n.jsx)(x.II,{...r("audio_dir"),placeholder:"Path to audio directory...",required:!0})}),(0,n.jsxs)(x.k4,{children:[(0,n.jsx)(j.rG,{className:"inline-block mr-2 w-6 h-6 align-middle"}),"Import"]})]})}function p(e){let{onImportDataset:t,onError:a}=e,{mutateAsync:s}=(0,r.D)({mutationFn:c.Z.datasets.import,onError:a,onSuccess:t}),i=(0,l.useCallback)(async e=>{o.ZP.promise(s(e),{loading:"Importing dataset...",success:"Dataset imported",error:"Failed to import dataset"})},[s]);return(0,n.jsx)(v,{onImportDataset:i})}var g=a(85382),N=a(75514),b=a(42918),C=a(26184),w=a(7064);function Z(e){let{datasets:t,isLoading:a=!1,onClickDataset:s,DatasetSearch:l,DatasetCreate:i,DatasetImport:r,Pagination:o}=e;return(0,n.jsx)(w.Z,{isLoading:a,isEmpty:0===t.length,Search:l,Empty:(0,n.jsx)(k,{}),Actions:[(0,n.jsx)(b.Z,{mode:"text",title:"Create Dataset",label:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(j.dt,{className:"inline-block w-4 h-4 align-middle"})," Create"]}),children:()=>i},"create"),(0,n.jsx)(b.Z,{mode:"text",title:"Import a Dataset",label:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(j.rG,{className:"inline-block w-4 h-4 align-middle"})," ","Import"]}),children:()=>r},"import")],Pagination:o,items:t.map(e=>(0,n.jsx)(N.Z,{dataset:e,onClickDataset:()=>null==s?void 0:s(e)},e.uuid))})}function k(){return(0,n.jsxs)(C.Z,{children:[(0,n.jsx)(j.aN,{className:"w-8 h-8 text-stone-500"}),(0,n.jsx)("p",{children:"No datasets found."}),(0,n.jsxs)("p",{children:["To create a dataset, click on the",(0,n.jsxs)("span",{className:"text-emerald-500",children:[(0,n.jsx)(j.dt,{className:"inline-block mr-1 ml-2 w-4 h-4"}),"Create"," "]})," ","button above."]})]})}var y=a(44850);function S(e){let{onCreateDataset:t,onClickDataset:a}=e,{items:s,pagination:l,isLoading:r,filter:o}=(0,g.Z)({onCreateDataset:t});return(0,n.jsx)(Z,{datasets:s,isLoading:r,onClickDataset:a,DatasetImport:(0,n.jsx)(p,{onImportDataset:t}),DatasetSearch:(0,n.jsx)(y.Z,{label:"Search",placeholder:"Search project...",value:o.get("search"),onChange:e=>o.set("search",e),onSubmit:o.submit,icon:(0,n.jsx)(j.O4,{})}),DatasetCreate:(0,n.jsx)(f,{onCreateDataset:t}),Pagination:(0,n.jsx)(i.Z,{pagination:l})})}var P=a(23913);function D(){let e=(0,s.useRouter)(),t=(0,l.useCallback)(t=>{e.push("/datasets/detail/?dataset_uuid=".concat(t.uuid))},[e]);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(P.Z,{text:"Datasets"}),(0,n.jsx)(S,{onCreateDataset:t,onClickDataset:t})]})}},36920:function(e,t,a){"use strict";a.d(t,{Z:function(){return l}});var n=a(57437),s=a(24863);function l(e){let{pagination:t,pageSizeOptions:a}=e;return(0,n.jsx)(s.Z,{page:t.page,numPages:t.numPages,pageSize:t.pageSize,hasNextPage:t.hasNextPage,hasPrevPage:t.hasPrevPage,onNextPage:t.nextPage,onPrevPage:t.prevPage,onSetPage:t.setPage,onSetPageSize:t.setPageSize,pageSizeOptions:a})}},85382:function(e,t,a){"use strict";a.d(t,{Z:function(){return d}});var n=a(25524),s=a(88726),l=a(39527),i=a(58002),r=a(90840);let o={},c=[];function d(){let{filter:e=o,fixed:t=c,pageSize:a=10,enabled:d=!0,onCreateDataset:u}=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},x=(0,i.Z)({defaults:e,fixed:t}),{query:m,pagination:h,items:f,total:j}=(0,r.Z)({name:"datasets",queryFn:l.Z.datasets.getMany,pageSize:a,filter:x.filter,enabled:d}),v=(0,n.D)({mutationFn:l.Z.datasets.create,onSuccess:e=>{s.ZP.success("Dataset ".concat(e.name," created")),null==u||u(e),m.refetch()}});return{...m,filter:x,pagination:h,items:f,total:j,create:v}}},75514:function(e,t,a){"use strict";a.d(t,{Z:function(){return r},h:function(){return i}});var n=a(57437),s=a(90912),l=a(56541);function i(e){let{label:t,value:a}=e;return(0,n.jsxs)("div",{className:"flex flex-row mr-4 space-x-1",children:[(0,n.jsx)("div",{className:"text-sm font-medium text-stone-500",children:t}),(0,n.jsx)("div",{className:"text-sm text-stone-700 dark:text-stone-300",children:a})]})}function r(e){let{dataset:t,onClickDataset:a}=e;return(0,n.jsxs)("div",{className:"w-full",children:[(0,n.jsxs)("div",{className:"px-4 sm:px-0",children:[(0,n.jsxs)("h3",{className:"text-base font-semibold leading-7 text-stone-900 dark:text-stone-100",children:[(0,n.jsx)("span",{className:"inline-block w-6 h-6 align-middle text-stone-500",children:(0,n.jsx)(s.lQ,{})})," ",(0,n.jsx)(l.Z,{className:"inline-flex",padding:"p-0",mode:"text",onClick:a,children:t.name})]}),(0,n.jsx)("p",{className:"mt-1 w-full text-sm leading-5 text-stone-600 dark:text-stone-400",children:t.description})]}),(0,n.jsxs)("div",{className:"flex flex-row py-4",children:[(0,n.jsx)(i,{label:(0,n.jsx)(s.se,{className:"w-4 h-4 align-middle"}),value:t.recording_count.toString()}),(0,n.jsx)(i,{label:(0,n.jsx)(s.Qu,{className:"w-4 h-4 align-middle"}),value:t.created_on.toDateString()})]})]})}},44850:function(e,t,a){"use strict";a.d(t,{Z:function(){return x}});var n=a(57437),s=a(2265),l=a(70407),i=a(13354),r=a(93272),o=a(90912),c=a(56541),d=a(76845),u=a(93222);function x(e){let{label:t="Search",placeholder:a="Search...",isLoading:x=!1,icon:m,...h}=e,f=(0,r.c)({label:t,...h}),j=(0,s.useRef)(null),{labelProps:v,inputProps:p,clearButtonProps:g}=(0,l.t)({label:t,...h},f,j);return(0,n.jsxs)("div",{className:"flex items-center",children:[(0,n.jsx)(i.T,{children:(0,n.jsx)("label",{...v,children:t})}),(0,n.jsxs)("div",{className:"relative w-full",children:[(0,n.jsx)("div",{className:"flex absolute inset-y-0 left-0 items-center pl-3 w-8 pointer-events-none",children:x?(0,n.jsx)(d.Z,{}):m||(0,n.jsx)(o.W1,{})}),(0,n.jsx)(u.Z,{className:"pl-10 text-sm 5",ref:j,...p}),""!==f.value&&(0,n.jsxs)(c.Z,{variant:"primary",mode:"text",className:"flex absolute inset-y-0 right-0 items-center ml-2",onClick:g.onPress,children:[(0,n.jsx)(o.Tw,{className:"w-4 h-4"}),(0,n.jsx)("span",{className:"sr-only",children:t})]})]})]})}},7064:function(e,t,a){"use strict";a.d(t,{Z:function(){return r}});var n=a(57437);function s(e){let{items:t}=e;return(0,n.jsx)("ul",{role:"list",className:"w-full divide-y divide-stone-300 dark:divide-stone-700",children:t.map(e=>(0,n.jsx)("li",{className:"flex gap-x-6 justify-between py-5",children:e},e.key))})}var l=a(26184),i=a(76845);function r(e){let{isLoading:t=!1,isEmpty:a=!1,Search:r,Actions:o,Empty:c,Pagination:d,items:u}=e;return(0,n.jsxs)("div",{className:"flex flex-col p-8 space-y-2 w-full",children:[(0,n.jsxs)("div",{className:"flex flex-row space-x-4",children:[(0,n.jsx)("div",{className:"flex-grow",children:r}),null==o?void 0:o.map((e,t)=>(0,n.jsx)("div",{className:"h-full",children:e},t))]}),t?(0,n.jsx)(l.Z,{children:(0,n.jsx)("div",{className:"p-8",children:(0,n.jsx)(i.Z,{})})}):a?c:(0,n.jsx)(s,{items:u}),d]})}},24863:function(e,t,a){"use strict";a.d(t,{Z:function(){return c}});var n=a(57437),s=a(90912),l=a(91614),i=a(92369),r=a(56541);let o=[1,5,10,25,50,100];function c(e){let{page:t=0,numPages:a=1,pageSize:l=10,hasNextPage:c=!1,hasPrevPage:u=!1,onNextPage:x,onPrevPage:m,onSetPage:h,onSetPageSize:f,pageSizeOptions:j=o}=e;return(0,n.jsxs)("div",{className:"flex flex-row space-x-2",children:[(0,n.jsx)(r.Z,{disabled:0===t,onClick:()=>null==h?void 0:h(0),variant:"secondary",mode:"text",children:(0,n.jsx)(s.Op,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,n.jsx)(r.Z,{onClick:m,disabled:!u,variant:"secondary",mode:"text",children:(0,n.jsx)(s.jJ,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,n.jsx)("div",{className:"w-14",children:(0,n.jsx)(i.II,{disabled:1===a,type:"number",className:"remove-arrow",value:t+1,onChange:e=>null==h?void 0:h(parseInt(e.target.value)-1)})}),(0,n.jsxs)(r.Z,{disabled:!0,variant:"secondary",mode:"text",children:["/ ",a]}),(0,n.jsx)(r.Z,{onClick:x,disabled:!c,variant:"secondary",mode:"text",children:(0,n.jsx)(s.Ne,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,n.jsx)(r.Z,{disabled:t===a-1,onClick:()=>null==h?void 0:h(a-1),variant:"secondary",mode:"text",children:(0,n.jsx)(s.OZ,{className:"w-5 h-5 fill-transparent stroke-inherit"})}),(0,n.jsx)(d,{pageSize:l,onSetPageSize:f,pageSizeOptions:j})]})}function d(e){let{pageSize:t=10,onSetPageSize:a,pageSizeOptions:s=o}=e;return(0,n.jsx)(l.Z,{label:"Page Size:",selected:{label:t.toString(),value:t,id:t},onChange:e=>null==a?void 0:a(e),options:s.map(e=>({label:e.toString(),value:e,id:e}))})}},42918:function(e,t,a){"use strict";a.d(t,{Z:function(){return c},t:function(){return d}});var n=a(57437),s=a(59226),l=a(24880),i=a(2265),r=a(90912),o=a(56541);function c(e){let{title:t,children:a,label:s,open:l=!1,width:r="max-w-lg",...c}=e,[u,x]=(0,i.useState)(l);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(o.Z,{type:"button",onClick:()=>x(!0),...c,children:s}),(0,n.jsx)(d,{title:(0,n.jsx)("div",{children:t}),isOpen:u,onClose:()=>x(!1),children:e=>{let{close:t}=e;return(0,n.jsx)("div",{className:r,children:a({close:t})})}})]})}function d(e){let{title:t,children:a,onClose:c,isOpen:d=!0}=e;return(0,n.jsx)(s.u,{appear:!0,show:d,as:i.Fragment,children:(0,n.jsxs)(l.V,{as:"div",className:"relative z-50",onClose:()=>null==c?void 0:c(),children:[(0,n.jsx)(s.u.Child,{as:i.Fragment,enter:"ease-out duration-300",enterFrom:"opacity-0",enterTo:"opacity-100",leave:"ease-in duration-200",leaveFrom:"opacity-100",leaveTo:"opacity-0",children:(0,n.jsx)("div",{className:"fixed inset-0 bg-black bg-opacity-25"})}),(0,n.jsx)("div",{className:"overflow-y-auto fixed inset-0",children:(0,n.jsx)("div",{className:"flex justify-center items-center p-4 min-h-full text-center",children:(0,n.jsx)(s.u.Child,{as:i.Fragment,enter:"ease-out duration-300",enterFrom:"opacity-0 scale-95",enterTo:"opacity-100 scale-100",leave:"ease-in duration-200",leaveFrom:"opacity-100 scale-100",leaveTo:"opacity-0 scale-95",children:(0,n.jsxs)(l.V.Panel,{className:"overflow-hidden p-6 w-full text-left align-middle rounded-2xl shadow-xl transition-all transform max-w-fit bg-stone-50 text-stone-700 z-[99999] dark:bg-stone-700 dark:text-stone-300",children:[(0,n.jsxs)(l.V.Title,{as:"div",className:"flex flex-row gap-4 justify-between items-center mb-4",children:[null!=t&&(0,n.jsx)("h3",{className:"text-lg font-medium leading-6 text-stone-900 dark:text-stone-100",children:t}),(0,n.jsx)(o.Z,{onClick:()=>null==c?void 0:c(),variant:"secondary",mode:"text",children:(0,n.jsx)(r.Tw,{className:"w-5 h-5"})})]}),(0,n.jsx)("div",{className:"mt-2",children:a({close:()=>null==c?void 0:c()})})]})})})})]})})}},26184:function(e,t,a){"use strict";a.d(t,{Z:function(){return i}});var n=a(57437),s=a(56800),l=a.n(s);function i(e){let{children:t,outerClassName:a="p-8",className:s}=e;return(0,n.jsx)("div",{className:"".concat(a," w-full"),children:(0,n.jsx)("div",{className:l()(s,"flex flex-col justify-center items-center p-4 w-full text-center rounded-md border border-dashed border-stone-500 text-stone-500"),children:t})})}},87604:function(e,t,a){"use strict";a.d(t,{Z:function(){return s}});var n=a(57437);function s(e){let{children:t}=e;return(0,n.jsx)("header",{className:"shadow bg-stone-50 dark:bg-stone-800",children:(0,n.jsx)("div",{className:"py-3 px-2 max-w-7xl sm:px-3 lg:px-6",children:t})})}},79799:function(e,t,a){"use strict";a.d(t,{H1:function(){return i},H2:function(){return r},H3:function(){return o},H4:function(){return c}});var n=a(57437),s=a(56800),l=a.n(s);function i(e){let{children:t,className:a,...s}=e;return(0,n.jsx)("h1",{className:l()("text-2xl font-bold text-stone-800 dark:text-stone-300",a),...s,children:t})}function r(e){let{children:t,className:a,...s}=e;return(0,n.jsx)("h2",{className:l()("text-xl font-bold text-stone-800 dark:text-stone-300",a),...s,children:t})}function o(e){let{children:t,className:a,...s}=e;return(0,n.jsx)("h3",{className:l()("text-lg font-semibold leading-7 items-center text-stone-800 dark:text-stone-300",a),...s,children:t})}function c(e){let{children:t,className:a,...s}=e;return(0,n.jsx)("h4",{className:l()(a,"text-md font-semibold leading-6 text-stone-800 dark:text-stone-300"),...s,children:t})}},23913:function(e,t,a){"use strict";a.d(t,{Z:function(){return i}});var n=a(57437),s=a(87604),l=a(79799);function i(e){let{text:t}=e;return(0,n.jsx)(s.Z,{children:(0,n.jsx)(l.H1,{children:t})})}},76845:function(e,t,a){"use strict";a.d(t,{Z:function(){return l}});var n=a(57437),s=a(79803);function l(){let{text:e=""}=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return(0,n.jsxs)("div",{className:"flex flex-row justify-center items-center w-full h-full",children:[(0,n.jsx)(s.Z,{})," ",e]})}},79803:function(e,t,a){"use strict";a.d(t,{Z:function(){return i}});var n=a(57437),s=a(56800),l=a.n(s);function i(e){let{variant:t="primary",className:a="w-8 h-8"}=e;return(0,n.jsxs)("div",{role:"status",children:[(0,n.jsxs)("svg",{"aria-hidden":"true",className:l()(a,"mr-2 inline animate-spin text-stone-200 dark:text-stone-600",function(e){switch(e){case"primary":case"success":return"fill-emerald-500";case"secondary":return"fill-stone-900 dark:fill-stone-100";case"danger":return"fill-rose-500";case"warning":return"fill-yellow-500";case"info":return"fill-blue-500"}}(t)),viewBox:"0 0 100 101",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,n.jsx)("path",{d:"M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z",fill:"currentColor"}),(0,n.jsx)("path",{d:"M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z",fill:"currentFill"})]}),(0,n.jsx)("span",{className:"sr-only",children:"Loading..."})]})}},58002:function(e,t,a){"use strict";a.d(t,{Z:function(){return r}});var n=a(2265),s=a(48494);let l=[],i={};function r(){let{defaults:e=i,fixed:t=l,debounce:a=500}=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},[r,o]=(0,n.useState)(e),[c,d]=(0,n.useState)(r);(0,n.useEffect)(()=>{o(e),d(e)},[e]);let u=(0,n.useCallback)(e=>t.includes(e),[t]),x=(0,n.useCallback)(function(e,t){let a=arguments.length>2&&void 0!==arguments[2]&&arguments[2];(!u(e)||a)&&o(a=>({...a,[e]:t}))},[u]),m=(0,n.useCallback)(e=>r[e],[r]),h=(0,n.useCallback)(function(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];(!u(e)||t)&&o(t=>{let a={...t};return delete a[e],d(a),a})},[u]),f=(0,n.useCallback)(()=>o(e),[e]),j=(0,n.useCallback)(e=>{o(t=>({...t,...e}))},[]);return(0,s.Z)(()=>{d(r)},a,[r]),{filter:c,update:j,set:x,get:m,clear:h,reset:f,submit:(0,n.useCallback)(()=>{d(r)},[r]),size:(0,n.useMemo)(()=>Object.keys(r).filter(e=>!u(e)).length,[r,u]),isFixed:u,fixed:t}}},90840:function(e,t,a){"use strict";a.d(t,{Z:function(){return i}});var n=a(40932),s=a(56298),l=a(2265);function i(e){var t,a,i;let{name:r,queryFn:o,pageSize:c,filter:d,enabled:u=!0}=e,[x,m]=(0,l.useState)(0),[h,f]=(0,l.useState)(c),j=[r,x,h,JSON.stringify(d)],v=(0,n.a)({queryKey:j,queryFn:()=>o({limit:h,offset:x*h,...d}),enabled:u,refetchOnWindowFocus:!1,placeholderData:s.Wk}),p=Math.ceil((null!==(i=null===(t=v.data)||void 0===t?void 0:t.total)&&void 0!==i?i:0)/h);(0,l.useEffect)(()=>{m(e=>e>=p&&p>0?p-1:e)},[p]);let g=(0,l.useMemo)(()=>({page:x,numPages:p,pageSize:h,setPage:e=>{e>=0&&e<p&&m(e)},setPageSize:e=>{e>0&&f(t=>{var a,n,s,l;let i=Math.ceil((null!==(s=null===(a=v.data)||void 0===a?void 0:a.total)&&void 0!==s?s:0)/e);return m(Math.max(0,Math.min(Math.floor(Math.min(x*t,null!==(l=null===(n=v.data)||void 0===n?void 0:n.total)&&void 0!==l?l:0)/e),i-1))),e})},nextPage:()=>{x<p-1&&m(x+1)},prevPage:()=>{x>0&&m(x-1)},hasNextPage:x<p-1,hasPrevPage:x>0}),[x,p,h,null===(a=v.data)||void 0===a?void 0:a.total]),{items:N,total:b}=(0,l.useMemo)(()=>null==v.data||v.isLoading?{items:[],total:0}:{items:v.data.items,total:v.data.total},[v.data,v.isLoading]);return{items:N,total:b,pagination:g,query:v,queryKey:j}}}},function(e){e.O(0,[5501,7819,5660,9772,8472,1336,5657,9226,932,6259,3215,4880,4329,6638,9527,4593,2971,7023,1744],function(){return e(e.s=86395)}),_N_E=e.O()}]);