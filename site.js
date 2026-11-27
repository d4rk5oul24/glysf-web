/* Glysf: funciones comunes a todas las páginas (WhatsApp, cookies y analítica). */
(function(){
// ===== Configuración: completa estos dos datos =====
var WHATSAPP='';      // Número de WhatsApp de Glysf con indicativo y sin espacios, ej.: 573001234567
var GA_ID='';         // ID de Google Analytics 4, ej.: G-ABC123XYZ
var WA_TEXTO='Hola, quiero información sobre las automatizaciones de Glysf.';
// ===================================================

var KEY='glysf-cookies';
function get(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
function set(v){try{localStorage.setItem(KEY,v);}catch(e){}}

// Botón de WhatsApp
var wa=document.getElementById('waBtn');
if(wa&&/^\d{10,15}$/.test(WHATSAPP)){wa.href='https://wa.me/'+WHATSAPP+'?text='+encodeURIComponent(WA_TEXTO);wa.hidden=false;
 wa.addEventListener('click',function(){if(window.gtag)gtag('event','contacto_whatsapp');});}

// Analítica: solo se carga con consentimiento
function loadGA(){if(!/^G-[A-Z0-9]+$/.test(GA_ID)||window.gtag)return;
 window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};
 gtag('js',new Date());gtag('config',GA_ID,{anonymize_ip:true});
 var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID;document.head.appendChild(s);}

// Aviso de cookies
var bar=document.getElementById('cookieBar');
function show(){if(bar){bar.hidden=false;document.body.classList.add('has-cookiebar');}}
function hide(){if(bar){bar.hidden=true;document.body.classList.remove('has-cookiebar');}}
if(bar){
 bar.addEventListener('click',function(e){var b=e.target.closest('[data-consent]');if(!b)return;var v=b.getAttribute('data-consent');set(v);hide();
  if(v==='si')loadGA();else if(window.gtag){location.reload();}});
 document.querySelectorAll('[data-cookies]').forEach(function(b){b.addEventListener('click',show);});
 // El aviso solo aparece si hay analítica configurada (sin analítica la web no usa cookies).
 var hasGA=/^G-[A-Z0-9]+$/.test(GA_ID);
 if(!hasGA)document.querySelectorAll('[data-cookies]').forEach(function(b){b.hidden=true;});
 var c=get();if(c==='si')loadGA();else if(c!=='no'&&hasGA)show();
}
window.glysfEvent=function(n,p){if(window.gtag)gtag('event',n,p||{});};
})();
