(this["webpackJsonp@coreui/coreui-pro-react-admin-template"]=this["webpackJsonp@coreui/coreui-pro-react-admin-template"]||[]).push([[9],{1482:function(e,a,t){"use strict";t.r(a);var l=t(7),n=t(8),r=t(9),i=t(10),c=t(0),m=t.n(c),o=t(14),s=t(1),u=t(51),d=t(15),p=t(17),E=t(21),h=t(43),b=function(e){Object(i.a)(t,e);var a=Object(r.a)(t);function t(){var e;Object(l.a)(this,t);for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];return(e=a.call.apply(a,[this].concat(r))).handleSubmit=function(a){e.props.getPasswordResetToken(a.email,e.props.history)},e}return Object(n.a)(t,[{key:"render",value:function(){var e=this.props.loading;return m.a.createElement("div",{className:"c-app c-default-layout flex-row align-items-center"},m.a.createElement(s.n,null,m.a.createElement(s.Q,{className:"justify-content-center"},m.a.createElement(s.l,{md:"5"},m.a.createElement(s.g,null,m.a.createElement(s.e,{className:"p-4"},m.a.createElement(s.f,null,m.a.createElement(s.C,{className:"mb-3"},m.a.createElement(h.d,{initialValues:{email:""},validationSchema:E.object().shape({email:E.string().email("Invalid email address").required("Email is required!")}),onSubmit:this.handleSubmit},(function(a){var t=a.values,l=a.errors,n=a.touched,r=a.handleChange,i=a.handleBlur,c=a.handleSubmit,d=a.isValid;return m.a.createElement(s.t,{onSubmit:c,noValidate:!0,name:"resetpasswordForm"},m.a.createElement(s.C,{className:"mb-4"},m.a.createElement("p",null,"Please enter email address. You will receive a link to create a new password via email."),m.a.createElement(s.D,{addonType:"prepend"},m.a.createElement(s.E,null,m.a.createElement(u.a,{name:"cil-lock-locked"}))),m.a.createElement(s.B,{type:"email",name:"email",id:"email",placeholder:"email",valid:!l.email,invalid:n.email&&!!l.email,required:!0,onChange:r,onBlur:i,value:t.email}),m.a.createElement(s.u,null,l.email)),m.a.createElement(s.Q,null,m.a.createElement(s.l,{xs:"8"},m.a.createElement(s.d,{type:"submit",color:"primary",className:"px-4",disabled:e||!d},e?"Wait...":"Send email")),m.a.createElement(s.l,{xs:"4",className:"text-right"},m.a.createElement(o.b,{to:"/admin/login"},m.a.createElement(s.d,{color:"link",className:"px-0"},"Log in")))))}))))))))))}}]),t}(c.Component);var v={alertError:d.a.error,getPasswordResetToken:d.f.getPasswordResetToken};a.default=Object(p.b)((function(e){return{loading:e.authentication.loading}}),v)(b)}}]);
//# sourceMappingURL=9.bd90b118.chunk.js.map