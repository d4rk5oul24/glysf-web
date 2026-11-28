/* Glysf: funciones comunes a todas las páginas (WhatsApp, cookies y analítica). */
(function(){
// ===== Configuración: completa estos dos datos =====
var WHATSAPP='573103102908';      // Número de WhatsApp de Glysf con indicativo y sin espacios, ej.: 573001234567
var GA_ID='';         // ID de Google Analytics 4, ej.: G-ABC123XYZ
var WA_TEXTO='Hola, quiero información sobre las automatizaciones de Glysf.';
// ===================================================

var KEY='glysf-cookies';
function get(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
function set(v){try{localStorage.setItem(KEY,v);}catch(e){}}

// Botones de WhatsApp: el flotante (#waBtn) y cualquier enlace con data-wa (su valor es el mensaje inicial)
if(/^\d{10,15}$/.test(WHATSAPP)){
 document.querySelectorAll('#waBtn,[data-wa]').forEach(function(a){
  var t=a.getAttribute('data-wa')||WA_TEXTO;
  a.href='https://wa.me/'+WHATSAPP+'?text='+encodeURIComponent(t);a.hidden=false;
  a.addEventListener('click',function(){if(window.gtag)gtag('event','contacto_whatsapp');});});
}

// Analítica: solo se carga con consentimiento
function loadGA(){if(!/^G-[A-Z0-9]+$/.test(GA_ID)||window.gtag)return;
 window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};
 gtag('js',new Date());gtag('config',GA_ID,{anonymize_ip:true});
 var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID;document.head.appendChild(s);}

// Borra las cookies de Google Analytics (_ga y _ga_*) en este dominio y en el dominio principal.
function clearGA(){
 var names=document.cookie.split(';').map(function(c){return c.split('=')[0].trim();}).filter(function(n){return n==='_ga'||n.indexOf('_ga_')===0;});
 var h=location.hostname,parts=h.split('.'),doms=['',h,'.'+h];
 if(parts.length>1){var root=parts.slice(-2).join('.');doms.push(root,'.'+root);}
 names.forEach(function(n){doms.forEach(function(d){document.cookie=n+'=; Max-Age=0; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'+(d?'; domain='+d:'');});});
 return names.length>0;}

// Aviso de cookies. Mientras se ve, la página reserva su alto (--cbh) para que no tape el control enfocado.
var bar=document.getElementById('cookieBar'),root=document.documentElement;
function fit(){if(bar&&!bar.hidden)root.style.setProperty('--cbh',(bar.offsetHeight+24)+'px');}
function show(){if(bar){bar.hidden=false;root.classList.add('has-cookiebar');fit();}}
function hide(){if(bar){bar.hidden=true;root.classList.remove('has-cookiebar');root.style.removeProperty('--cbh');}}
if(bar){
 window.addEventListener('resize',fit);
 bar.addEventListener('click',function(e){var b=e.target.closest('[data-consent]');if(!b)return;var v=b.getAttribute('data-consent');set(v);hide();
  if(v==='si'){loadGA();return;}
  // Revocar: se desactiva la analítica, se borran sus cookies y se recarga sin gtag.
  if(GA_ID)window['ga-disable-'+GA_ID]=true;
  var had=clearGA();if(window.gtag||had)location.reload();});
 document.querySelectorAll('[data-cookies]').forEach(function(b){b.addEventListener('click',function(){show();var f=bar.querySelector('[data-consent]');if(f)f.focus();});});
 // El aviso solo aparece si hay analítica configurada (sin analítica la web no usa cookies).
 var hasGA=/^G-[A-Z0-9]+$/.test(GA_ID);
 if(!hasGA)document.querySelectorAll('[data-cookies]').forEach(function(b){b.hidden=true;});
 var c=get();if(c==='si')loadGA();else{if(c==='no')clearGA();if(c!=='no'&&hasGA)show();}
}
// Que el aviso de cookies no tape el campo que se está llenando
document.addEventListener('focusin',function(e){if(!bar||bar.hidden)return;var r=e.target.getBoundingClientRect(),top=bar.getBoundingClientRect().top;if(r.bottom>top-8)window.scrollBy(0,r.bottom-top+16);});
window.glysfEvent=function(n,p){if(window.gtag)gtag('event',n,p||{});};
})();
