(this["webpackJsonp@coreui/coreui-pro-react-admin-template"]=this["webpackJsonp@coreui/coreui-pro-react-admin-template"]||[]).push([[6],{1481:function(e,a,t){"use strict";t.r(a);var n=t(7),r=t(8),l=t(9),s=t(10),c=t(0),o=t.n(c),m=t(14),i=t(1),u=t(51),d=t(43),p=t(21),E=t(17),h=t(15),g=t(164),w=function(e){Object(s.a)(t,e);var a=Object(l.a)(t);function t(){var e;Object(n.a)(this,t);for(var r=arguments.length,l=new Array(r),s=0;s<r;s++)l[s]=arguments[s];return(e=a.call.apply(a,[this].concat(l))).handleSubmit=function(a){e.props.login(a.username,a.password,e.props.history)},e}return Object(r.a)(t,[{key:"render",value:function(){var e=this.props.loading;return o.a.createElement("div",{className:"c-app c-default-layout flex-row align-items-center"},o.a.createElement(i.n,null,o.a.createElement(i.Q,{className:"justify-content-center"},o.a.createElement(i.l,{md:"5"},o.a.createElement(i.g,null,o.a.createElement(i.e,{className:"p-4"},o.a.createElement(i.f,null,o.a.createElement(d.d,{initialValues:{email:"",password:""},validationSchema:p.object().shape({username:p.string().required("username is required!"),password:p.string().min(6,"Password has to be at least ".concat(6," characters!")).required("Password is required")}),onSubmit:this.handleSubmit},(function(a){var t=a.values,n=a.errors,r=a.touched,l=a.handleChange,s=a.handleBlur,c=a.handleSubmit,d=a.isValid;return o.a.createElement(i.Q,null,o.a.createElement(i.l,{lg:"12"},o.a.createElement(i.t,{onSubmit:c,noValidate:!0,name:"loginForm"},o.a.createElement("h1",null,"Login"),o.a.createElement("p",{className:"text-muted"},"Sign In to your account"),o.a.createElement(i.C,{className:"mb-3"},o.a.createElement(i.D,{addonType:"prepend"},o.a.createElement(i.E,null,o.a.createElement(u.a,{name:"cil-user"}))),o.a.createElement(i.B,{type:"text",name:"username",id:"username",placeholder:"username",autoComplete:"username",valid:!n.username,invalid:r.username&&!!n.username,required:!0,onChange:l,onBlur:s,value:t.username}),o.a.createElement(i.u,null,n.username)),o.a.createElement(i.C,{className:"mb-4"},o.a.createElement(i.D,{addonType:"prepend"},o.a.createElement(i.E,null,o.a.createElement(u.a,{name:"cil-lock-locked"}))),o.a.createElement(i.B,{type:"password",name:"password",id:"password",placeholder:"Password",autoComplete:"new-password",valid:!n.password,invalid:r.password&&!!n.password,required:!0,onChange:l,onBlur:s,value:t.password}),o.a.createElement(i.u,null,n.password)),o.a.createElement(i.Q,null,o.a.createElement(i.l,{xs:"6"},o.a.createElement(i.d,{type:"submit",color:"primary",className:"px-4",disabled:e||!d},e?"Wait...":"Login")),o.a.createElement(i.l,{xs:"6",className:"text-right"},o.a.createElement(m.b,{to:"/admin/reset_password"},o.a.createElement(i.d,{color:"link",className:"px-0"},"Forgot password?")))))))})))))))))}}]),t}(c.Component);var b={login:h.f.login};a.default=Object(g.g)(Object(E.b)((function(e){return{loading:e.authentication.loading}}),b)(w))}}]);
//# sourceMappingURL=6.7486b2cd.chunk.js.map