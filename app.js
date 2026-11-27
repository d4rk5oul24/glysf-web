/* ---------- Portada: equipo de agentes trabajando en vivo ---------- */
var AG=[
 {n:'Recepción',c:'#8FB3FF'},{n:'Agenda',c:'#7EE0C3'},{n:'Cobros',c:'#F5A3C7'},
 {n:'Inventario',c:'#FFD27A'},{n:'Reportes',c:'#B9A2FF'},{n:'Ventas',c:'#7FD4F5'}];
var H={timers:[],t0:0,done:0,running:false,visible:true,cursors:[]};
var HROWS=['5:00 p. m.','6:00 p. m.','7:00 p. m.','8:00 p. m.'];
var HINV=[['Pelotas',40,'tubos',8],['Raquetas',12,'und',9],['Bebidas',96,'und',58]];
function hq(id){return document.getElementById(id);}
function hel(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e;}
function hMoney(n){return '$'+Math.round(n).toLocaleString('es-CO');}
function hBuild(){
 var cal=hq('hCal');cal.replaceChildren(hel('span'));['Cancha 1','Cancha 2','Cancha 3'].forEach(function(c){cal.append(hel('span','ch',c));});
 HROWS.forEach(function(r,i){cal.append(hel('span','ct',r));for(var j=0;j<3;j++){var s=hel('span','cs');s.id='hs'+i+j;cal.append(s);}});
 hq('hChat').replaceChildren();hq('hPayList').replaceChildren();hq('hRep').replaceChildren();hq('hLog').replaceChildren();
 hq('hPay').textContent='$0';hq('hPay')._v=0;
 var inv=hq('hInv');inv.replaceChildren();HINV.forEach(function(x,i){var r=hel('div','ir');r.id='hi'+i;var b=hel('div','bar');b.append(hel('i'));r.append(hel('span',null,x[0]),hel('span','q',x[1]+' '+x[2]),b);inv.append(r);});
 inv.append(hel('div','note'));
 var cs=hq('hCursors');cs.replaceChildren();H.cursors=AG.map(function(a,i){var d=hel('div','cur');d.style.setProperty('--c',a.c);
  d.innerHTML='<svg viewBox="0 0 16 18"><path d="M1 1l13 7-6 1.5L5 16z" fill="'+a.c+'" stroke="#06112E" stroke-width="1.2" stroke-linejoin="round"/></svg>';
  d.append(hel('span',null,a.n));var w=hq('ws');d.style.transform='translate('+(40+i*((w.clientWidth-120)/5))+'px,'+(w.clientHeight-40)+'px)';cs.append(d);return d;});
 hStatus(0);
}
function hStatus(n){var s=hq('hStatus');s.classList.toggle('done',n>=HT.length);s.replaceChildren();
 var dots=hel('span','dots');AG.forEach(function(a){var i=hel('i');i.style.setProperty('--c',a.c);dots.append(i);});
 s.append(dots,hel('span',null,AG.length+' agentes'),hel('span',null,n+'/'+HT.length+' tareas'),hel('span','st',n>=HT.length?'día cerrado':'trabajando'));}
function hLog(a,text){var ms=performance.now()-H.t0;var li=hel('li');var t=hel('time',null,'00:'+String(Math.floor(ms/1000)).padStart(2,'0')+'.'+Math.floor(ms%1000/100));
 var w=hel('span','who',AG[a].n);w.style.setProperty('--c',AG[a].c);li.append(t,w,hel('span',null,text));var l=hq('hLog');l.prepend(li);while(l.children.length>4)l.lastChild.remove();}
function hChat(cls,text){var c=hq('hChat');c.append(hel('div','hm '+cls,text));while(c.children.length>5)c.firstChild.remove();}
function hBook(i,j,a,name){var s=hq('hs'+i+j);s.style.setProperty('--c',AG[a].c);s.textContent=name;s.classList.add('on');}
function hPay(name,v){var p=hq('hPay');var from=p._v,to=from+v,t0=performance.now();p._v=to;
 (function tick(t){var k=Math.min(1,(t-t0)/700);p.textContent=hMoney(from+(to-from)*k);if(k<1&&H.running)requestAnimationFrame(tick);else p.textContent=hMoney(to);})(t0);
 var li=hel('li');li.append(hel('span',null,name+' · '+hMoney(v)),hel('b',null,'Pagado'));var l=hq('hPayList');l.prepend(li);while(l.children.length>3)l.lastChild.remove();}
function hInv(i,to,low){var r=hq('hi'+i),x=HINV[i];r.querySelector('.bar i').style.width=Math.max(5,to/x[1]*100)+'%';r.querySelector('.q').textContent=to+' '+x[2];if(low){r.classList.add('low');hq('hInv').querySelector('.note').textContent='Pedido de '+x[0].toLowerCase()+' enviado al proveedor';}}
function hRep(text){hq('hRep').append(hel('li',null,text));}
// [ms, agente, mosaico, acción, registro]
var HT=[
 [300,0,'tChat',function(){hChat('c','¿Hay cancha mañana a las 6?');setTimeout(function(){hChat('b','Sí: cancha 2 a las 6:00 p. m. ¿Te la reservo?');},350);},'respondió en 3 s'],
 [700,1,'hs10',function(){hBook(1,0,1,'Andrés M.');},'reservó cancha 1, 6 p. m.'],
 [1100,2,'tPay',function(){hPay('Andrés M.',100000);},'cobró la reserva'],
 [1400,3,'hi0',function(){hInv(0,26);},'descontó pelotas'],
 [1900,5,'tChat',function(){hChat('c','¿Cuánto valen las clases?');setTimeout(function(){hChat('b','$40.000 por persona. Martes y jueves, 7 p. m.');},350);},'envió precios'],
 [2200,1,'hs21',function(){hBook(2,1,1,'Clase');},'abrió clase grupal'],
 [2700,0,'tChat',function(){hChat('c','Dale, resérvala');setTimeout(function(){hChat('b','Listo. Te envío el link de pago.');},350);},'cerró una reserva'],
 [2900,1,'hs01',function(){hBook(0,1,1,'Laura P.');},'reservó cancha 2, 5 p. m.'],
 [3300,2,'tPay',function(){hPay('Laura P.',100000);},'cobró la reserva'],
 [3500,3,'hi0',function(){hInv(0,8,true);},'pidió pelotas al proveedor'],
 [4000,5,'hs32',function(){hBook(3,2,5,'Torneo');},'vendió un torneo'],
 [4300,2,'tPay',function(){hPay('Torneo',240000);},'cobró el torneo'],
 [4700,1,'hs20',function(){hBook(2,0,1,'Juan D.');},'reservó cancha 1, 7 p. m.'],
 [5000,3,'hi2',function(){hInv(2,41);},'actualizó bebidas'],
 [5400,4,'tRep',function(){hRep('Ocupación de hoy: 82%');},'calculó la ocupación'],
 [5900,4,'tRep',function(){hRep('Ingresos: $440.000');},'sumó los ingresos'],
 [6400,4,'tRep',function(){hRep('Pelotas: pedido en camino');},'envió el reporte al dueño']];
function hTarget(id){var w=hq('ws').getBoundingClientRect(),t=hq(id);if(!t||!t.offsetParent)t=hq('tChat');var r=t.getBoundingClientRect();
 return [Math.min(r.left-w.left+r.width*(.35+Math.random()*.3),w.width-100),r.top-w.top+Math.min(r.height*.55,60+Math.random()*30)];}
function hRun(){hClear();H.running=true;hBuild();H.t0=performance.now();H.done=0;
 HT.forEach(function(t){
  H.timers.push(setTimeout(function(){var p=hTarget(t[2]);H.cursors[t[1]].style.transform='translate('+p[0]+'px,'+p[1]+'px)';},t[0]));
  H.timers.push(setTimeout(function(){var tile=hq(t[2]);var box=tile&&tile.classList.contains('tile')?tile:tile&&tile.closest('.tile');if(box){box.classList.add('sel');setTimeout(function(){box.classList.remove('sel');},500);}
   t[3]();hLog(t[1],t[4]);H.done++;hStatus(H.done);},t[0]+780));});
 H.timers.push(setTimeout(function(){if(H.visible)hRun();else H.running=false;},HT[HT.length-1][0]+6000));}
function hClear(){H.timers.forEach(clearTimeout);H.timers=[];}
function hFinal(){hClear();hBuild();H.t0=performance.now();HT.forEach(function(t){t[3]();});H.done=HT.length;hStatus(H.done);
 var l=hq('hLog');HT.slice(-4).forEach(function(t){hLog(t[1],t[4]);});hq('hCursors').replaceChildren();}
function heroStop(){hClear();H.running=false;}
function heroWake(){if(!hq('ws'))return;if(matchMedia('(prefers-reduced-motion: reduce)').matches){hFinal();return;}if(!H.running&&H.visible)hRun();}
(function(){if(!hq('ws'))return;
 if('IntersectionObserver' in window){new IntersectionObserver(function(e){H.visible=e[0].isIntersecting;if(H.visible&&!H.running&&!hq('home').hidden)heroWake();}).observe(hq('ws'));}
 document.addEventListener('visibilitychange',function(){if(document.hidden)heroStop();else heroWake();});})();

const $=id=>document.getElementById(id);
const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;};

/* ---------- Demo interactivo ---------- */
// Cada paso: mensaje del bot + opciones. Cada opción: lo que dice el cliente, la respuesta del bot y el paso siguiente (null = fin).
const S={
padel:{label:'Pádel',bot:'Club Pádel Norte',tags:['Cancha reservada','Pago confirmado','Recordatorio al jugador'],steps:[
 {bot:'¡Hola! Soy el asistente del Club Pádel Norte. ¿Qué necesitas?',opts:[
  {u:'Reservar cancha',b:'¡Claro! Hoy tengo libre a las 6:00 p. m. y a las 8:00 p. m. ¿Cuál prefieres?',n:1},
  {u:'Ver precios',b:'La hora vale $80.000 de lunes a jueves y $100.000 de viernes a domingo. ¿Quieres reservar?',n:1},
  {u:'Clases para principiantes',b:'Tenemos clases grupales martes y jueves a las 7:00 p. m. ¿Te agendo la primera?',n:2}]},
 {bot:null,opts:[
  {u:'6:00 p. m.',b:'Reservada: cancha 2, hoy de 6:00 a 7:30 p. m. Te envío el link para pagar y te recuerdo una hora antes.',n:null},
  {u:'8:00 p. m.',b:'Reservada: cancha 1, hoy de 8:00 a 9:30 p. m. Te envío el link para pagar y te recuerdo una hora antes.',n:null}]},
 {bot:null,opts:[
  {u:'Sí, el martes',b:'Listo, quedaste inscrito el martes a las 7:00 p. m. Llega 10 minutos antes; nosotros ponemos la raqueta.',n:null},
  {u:'Mejor el jueves',b:'Listo, quedaste inscrito el jueves a las 7:00 p. m. Te enviaré un recordatorio ese día.',n:null}]}]},
clinica:{label:'Clínica',bot:'Clínica Dental Sonrisa',tags:['Cita con el especialista','Datos del paciente','Recordatorio 24 h antes'],steps:[
 {bot:'Hola, bienvenido a Clínica Dental Sonrisa. ¿En qué te ayudo?',opts:[
  {u:'Agendar valoración',b:'Con gusto. Hay espacio el jueves a las 9:00 a. m. o el viernes a las 4:00 p. m. ¿Cuál te sirve?',n:1},
  {u:'Precio de limpieza',b:'La limpieza tiene un valor de $120.000 e incluye valoración. ¿Quieres agendarla?',n:1},
  {u:'Reprogramar mi cita',b:'Claro. Encontré tu cita del lunes a las 10:00 a. m. ¿Para cuándo la movemos?',n:1}]},
 {bot:null,opts:[
  {u:'Jueves 9:00 a. m.',b:'Listo, quedó tu cita el jueves a las 9:00 a. m. Te recordaré un día antes con la dirección.',n:null},
  {u:'Viernes 4:00 p. m.',b:'Listo, quedó tu cita el viernes a las 4:00 p. m. Te recordaré un día antes con la dirección.',n:null}]}]},
gym:{label:'Gimnasio',bot:'Gym Fuerza',tags:['Plan enviado','Prospecto registrado','Seguimiento al asesor'],steps:[
 {bot:'¡Hola! Bienvenido a Gym Fuerza. ¿Qué te interesa?',opts:[
  {u:'Precios',b:'Mensual $90.000, trimestral $240.000 y anual $850.000. Y la primera clase es gratis. ¿La quieres?',n:1},
  {u:'Horarios',b:'Abrimos de lunes a viernes de 5:00 a. m. a 10:00 p. m. y sábados de 7:00 a. m. a 2:00 p. m. ¿Quieres una clase gratis?',n:1}]},
 {bot:null,opts:[
  {u:'Sí, mañana temprano',b:'Tu clase gratis quedó para mañana a las 6:00 a. m. Un asesor te recibe en la entrada. ¡Te esperamos!',n:null},
  {u:'Ahora no, gracias',b:'¡Sin problema! Te escribo la próxima semana por si te animas. Que tengas buen día.',n:null}]}]},
pilates:{label:'Pilates',bot:'Estudio Pilates',tags:['Cupo reservado','Paquete descontado','Recordatorio programado'],steps:[
 {bot:'¡Hola! ¿Quieres reservar una clase de reformer?',opts:[
  {u:'Sí, mañana',b:'Mañana hay cupo a las 7:00 a. m., 3:00 p. m. y 5:30 p. m. ¿Cuál te sirve?',n:1},
  {u:'¿Qué paquetes hay?',b:'Clase suelta, paquete de 8 y paquete de 12 clases al mes. ¿Te reservo la primera?',n:1}]},
 {bot:null,opts:[
  {u:'5:30 p. m.',b:'Listo, quedaste inscrita mañana a las 5:30 p. m. Te queda 1 cupo menos en tu paquete y te recuerdo una hora antes.',n:null},
  {u:'7:00 a. m.',b:'Listo, quedaste inscrita mañana a las 7:00 a. m. Te recuerdo la noche anterior.',n:null}]}]},
resto:{label:'Restaurante',bot:'Restaurante La Brasa',tags:['Pedido a cocina','Domicilio asignado','Pago registrado'],steps:[
 {bot:'¡Hola! Bienvenido a La Brasa. ¿Pides para domicilio o reservas mesa?',opts:[
  {u:'Domicilio',b:'Te envío el menú. Hoy recomendamos la hamburguesa de la casa. ¿Qué te mando?',n:1},
  {u:'Reservar mesa',b:'¿Para cuántas personas y a qué hora? Hoy hay mesas desde las 7:00 p. m.',n:2}]},
 {bot:null,opts:[
  {u:'2 hamburguesas y 2 limonadas',b:'Pedido recibido y enviado a cocina: total $78.000. Llega en unos 35 minutos. ¿Pagas en efectivo o transferencia?',n:null},
  {u:'1 picada para 2',b:'Pedido recibido y enviado a cocina: total $62.000. Llega en unos 40 minutos.',n:null}]},
 {bot:null,opts:[
  {u:'4 personas, 8:00 p. m.',b:'Reservada mesa para 4 hoy a las 8:00 p. m. a tu nombre. ¡Te esperamos!',n:null}]}]},
tienda:{label:'Tienda',bot:'Ferretería Central',tags:['Pedido en Google Sheets','Stock verificado','Aviso a bodega'],steps:[
 {bot:'¡Buenas! Soy el asistente de Ferretería Central. ¿Qué necesitas?',opts:[
  {u:'Hacer un pedido',b:'Dime qué productos y cantidades necesitas.',n:1},
  {u:'¿Tienen disponible…?',b:'Escríbeme el producto y te digo si hay en stock.',n:1}]},
 {bot:null,opts:[
  {u:'4 tableros y 20 bisagras',b:'Hay disponibilidad de ambos. Tu pedido #1043 quedó registrado y te envío el total con el link de pago.',n:null},
  {u:'1 galón de pintura blanca',b:'Sí hay: quedan 12 galones. Pedido #1044 registrado; lo puedes recoger en 1 hora.',n:null}]}]},
pelu:{label:'Peluquería',bot:'Salón Bella',tags:['Cita con el estilista','Anticipo cobrado','Recordatorio programado'],steps:[
 {bot:'¡Hola! Bienvenida a Salón Bella. ¿Qué servicio quieres?',opts:[
  {u:'Corte y cepillado',b:'¡Perfecto! Con Laura hay espacio el sábado a las 10:00 a. m. o a las 2:00 p. m. ¿Cuál te sirve?',n:1},
  {u:'Uñas',b:'Manicure semipermanente: $45.000. Hay cupo hoy a las 4:00 p. m. o mañana a las 11:00 a. m. ¿Cuál prefieres?',n:1},
  {u:'Ver precios',b:'Te envío la lista de servicios con precios. ¿Quieres agendar algo?',n:1}]},
 {bot:null,opts:[
  {u:'La primera',b:'Listo, quedó tu cita. Te envío el link para el anticipo y te recuerdo un día antes.',n:null},
  {u:'La segunda',b:'Listo, quedó tu cita. Te envío el link para el anticipo y te recuerdo un día antes.',n:null}]}]},
fabrica:{label:'Fábrica',bot:'Muebles Roble',tags:['Cotización en PDF','Pedido a proveedor','Seguimiento en 2 días'],steps:[
 {bot:'Hola, bienvenido a Muebles Roble. ¿Qué mueble estás buscando?',opts:[
  {u:'Closet',b:'¿Lo quieres con puertas corredizas o batientes?',n:1},
  {u:'Cocina integral',b:'¿Cuántos metros lineales mide tu cocina, más o menos?',n:2}]},
 {bot:null,opts:[
  {u:'Corredizas, color roble',b:'Te acabo de enviar la cotización en PDF. Si la apruebas, pedimos el material hoy mismo.',n:null},
  {u:'Batientes, blanco',b:'Te envié la cotización en PDF. Un asesor te llama para agendar la toma de medidas.',n:null}]},
 {bot:null,opts:[
  {u:'Unos 3 metros',b:'Te envié una cotización estimada en PDF. Agendamos visita para tomar medidas exactas sin costo.',n:null}]}]}
};
const CH={wa:'WhatsApp',ig:'Instagram',tg:'Telegram'};
const UC={wa:'#2F55F5',ig:'#7A4DF5',tg:'#2A8BD8'};
let sector='clinica',channel='wa',step=0,busy=false,timer=null;
function bubble(who,text){const b=el('div','bub '+who,text);if(who==='u')b.style.background=UC[channel];$('chat').append(b);$('chat').scrollTop=$('chat').scrollHeight;}
function typing(cb,ms){busy=true;const t=el('div','bub b','escribiendo…');t.style.cssText='background:#22396E;color:#A9B8DA';$('chat').append(t);$('chat').scrollTop=$('chat').scrollHeight;timer=setTimeout(()=>{t.remove();busy=false;cb();},ms||900);}
function showOpts(){const o=$('opts');o.replaceChildren();const s=S[sector];if(step===null){$('tags').replaceChildren(...s.tags.map(x=>el('span','tag','✓ '+x)));const again=el('button','opt','Probar de nuevo');again.type='button';again.onclick=start;o.append(again);return;}
 s.steps[step].opts.forEach(op=>{const b=el('button','opt',op.u);b.type='button';b.onclick=()=>choose(op);o.append(b);});}
function choose(op){if(busy)return;$('opts').replaceChildren();bubble('u',op.u);typing(()=>{bubble('b',op.b);step=op.n;const nx=step!==null?S[sector].steps[step]:null;if(nx&&nx.bot){typing(()=>{bubble('b',nx.bot);showOpts();},700);}else showOpts();});}
function start(){clearTimeout(timer);busy=false;step=0;$('chat').replaceChildren();$('tags').replaceChildren();$('opts').replaceChildren();renderHeader();typing(()=>{bubble('b',S[sector].steps[0].bot);showOpts();},600);}
function renderHeader(){
 $('channels').replaceChildren(...Object.keys(CH).map(k=>{const b=el('button','chip',CH[k]);b.type='button';b.setAttribute('aria-pressed',k===channel);b.onclick=()=>{channel=k;renderHeader();document.querySelectorAll('.bub.u').forEach(x=>x.style.background=UC[k]);};return b;}));
 $('botName').textContent=S[sector].bot;$('channelName').textContent=CH[channel];}
$('say').onsubmit=e=>{e.preventDefault();const v=$('sayInput').value.trim();if(!v||busy)return;$('sayInput').value='';
 const norm=x=>x.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
 if(step===null){bubble('u',v);typing(()=>bubble('b','¡Gracias por escribir! Para probar otra conversación toca "Probar de nuevo" o elige otro negocio.'));return;}
 const opts=S[sector].steps[step].opts;const words=norm(v).split(/\W+/).filter(w=>w.length>2);
 const hit=opts.find(o=>words.some(w=>norm(o.u).includes(w)));
 if(hit){$('opts').replaceChildren();bubble('u',v);typing(()=>{bubble('b',hit.b);step=hit.n;const nx=step!==null?S[sector].steps[step]:null;if(nx&&nx.bot){typing(()=>{bubble('b',nx.bot);showOpts();},700);}else showOpts();});}
 else{bubble('u',v);typing(()=>{bubble('b','En la versión real te entendería con IA. En esta demo, elige una de las opciones de abajo.');});}};
const chatSector=k=>{sector=k;channel='wa';};
const startChat=()=>start();

/* ---------- Catálogo de automatizaciones ---------- */
const A={
'Ventas y atención':[['Atención 24/7','Responde preguntas frecuentes, precios y horarios a cualquier hora.'],['Cotizaciones automáticas','Arma y envía la cotización en PDF en segundos.'],['Pedidos por chat','Toma el pedido, confirma el stock y envía el link de pago.'],['Catálogo en WhatsApp','Muestra productos con foto y precio dentro del chat.'],['Seguimiento a prospectos','Escribe a quien preguntó y no compró, en el momento justo.'],['Clientes potenciales calificados','Identifica quién está listo para comprar y avisa al vendedor.'],['Carritos abandonados','Recuerda la compra a quien dejó productos sin pagar.'],['Paso a un humano','Transfiere la conversación a tu equipo cuando hace falta.']],
'Agenda y reservas':[['Citas y reservas','Agenda en Google Calendar según tu disponibilidad real.'],['Recordatorios','Avisa un día y una hora antes para reducir inasistencias.'],['Confirmar o reprogramar','El cliente mueve su cita sin llamar.'],['Lista de espera','Ofrece el cupo liberado al siguiente en la lista.'],['Cobro de anticipos','Envía el link de pago para asegurar la reserva.'],['Varias sedes o profesionales','Agenda por persona, servicio o sede.']],
'Operación y finanzas':[['Cobros y cartera','Recuerda pagos pendientes de forma amable y automática.'],['Lectura de facturas con IA','Extrae los datos de facturas y soportes que te envían.'],['Registro de gastos','Envías la foto del recibo y queda registrado.'],['Inventario y alertas','Avisa cuando un producto se está agotando.'],['Pedidos a proveedores','Genera la orden de compra cuando baja el stock.'],['Reporte diario al dueño','Ventas, citas y pendientes del día en un mensaje.'],['Registro en Google Sheets','Cada cliente, pedido o cita queda guardado solo.']],
'Marketing y redes':[['Respuesta a comentarios','Contesta comentarios y mensajes de Instagram.'],['Campañas por WhatsApp','Promociones a clientes que aceptaron recibirlas.'],['Publicaciones programadas','Deja listas las publicaciones de la semana.'],['Reseñas en Google','Pide la reseña después de cada compra o visita.'],['Encuestas de satisfacción','Mide qué tan contentos quedan tus clientes.'],['Fechas especiales','Saludos y descuentos en cumpleaños y aniversarios.']],
'Equipo interno':[['Asistente en Telegram','Tu equipo consulta precios, stock o agenda con un mensaje.'],['Notas de voz a texto','Transcribe audios y los convierte en tareas.'],['Resumen de correos','Te llega lo importante de tu bandeja cada mañana.'],['Ingreso de empleados','Envía documentos, accesos e instrucciones a los nuevos.'],['Tareas y pendientes','Asigna y recuerda tareas al equipo automáticamente.'],['Avisos entre áreas','Ventas avisa a bodega y bodega avisa a despacho, solos.']]};
let area=Object.keys(A)[0];
function renderAuto(){
 $('autoTabs').replaceChildren(...Object.keys(A).map(k=>{const b=el('button','tab',k+' ('+A[k].length+')');b.type='button';b.setAttribute('role','tab');b.setAttribute('aria-selected',k===area);b.onclick=()=>{area=k;renderAuto();};return b;}));
 $('autoGrid').replaceChildren(...A[area].map(([h,p])=>{const d=el('div','auto');d.append(el('h3',null,h),el('p',null,p));return d;}));}
renderAuto();

/* ---------- Calculadora ---------- */
const r=$('msgs');r.oninput=()=>{const m=+r.value,h=Math.round(m*2*30/60);$('msgsVal').textContent=m;$('hours').textContent=h;$('days').textContent=Math.round(h/8);};

/* ---------- Formulario de cotización (con protección anti-spam) ---------- */
const FORM_T0=Date.now();let lastSend=0;
$('quote').onsubmit=e=>{e.preventDefault();const f=e.target,msg=$('quoteMsg');
 const bad=[...f.querySelectorAll('[required]')].find(x=>x.type==='checkbox'?!x.checked:!x.value.trim()||(x.type==='email'&&!/^\S+@\S+\.\S+$/.test(x.value)));
 if(bad){msg.hidden=false;msg.textContent=bad.type==='checkbox'?'Debes aceptar la política de tratamiento de datos.':'Revisa los campos obligatorios (*).';msg.className='';bad.focus();return;}
 msg.hidden=true;const d=new FormData(f);if(d.get('sitio')||Date.now()-FORM_T0<4000||Date.now()-lastSend<30000){msg.hidden=false;msg.className='';msg.textContent='Espera unos segundos e inténtalo de nuevo.';return;}lastSend=Date.now();if(window.glysfEvent)glysfEvent('cotizacion_enviada',{sector:d.get('sector')||'sin dato'});const clean=v=>String(v||'').replace(/[\u0000-\u0008\u000B-\u001F\u007F]/g,'').slice(0,2000);const all=n=>d.getAll(n).join(', ')||'—';
 const body=`Nombre: ${clean(d.get('nombre'))}\nEmpresa: ${clean(d.get('empresa'))}\nCorreo: ${clean(d.get('correo'))}\nTeléfono: ${clean(d.get('telefono'))||'—'}\nTipo de negocio: ${clean(d.get('sector'))||'—'}\nMensajes al día: ${clean(d.get('volumen'))||'—'}\nCanales: ${all('canal')}\nQuiere automatizar: ${all('necesidad')}\n\nDetalle:\n${clean(d.get('detalle'))}\n\nAutorizó el tratamiento de datos: Sí`;
 location.href='mailto:grupolysf@gmail.com?subject='+encodeURIComponent('Cotización Glysf – '+clean(d.get('empresa')))+'&body='+encodeURIComponent(body);
 msg.hidden=false;msg.className='ok';msg.textContent='¡Listo! Se abrió tu correo con la solicitud. Dale enviar y te respondemos pronto.';};
/* ---------- Escenas de fondo por negocio (SVG ilustrado y animado) ---------- */
const SCENE={
padel:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#0D4F7A"/><g opacity=".9"><rect x="230" y="120" width="740" height="600" rx="6" fill="#1C6FA8" stroke="#fff" stroke-width="6"/><rect x="230" y="120" width="740" height="600" fill="none" stroke="#8FC3E6" stroke-width="22" opacity=".35"/><line x1="230" y1="420" x2="970" y2="420" stroke="#fff" stroke-width="8"/><g stroke="#fff" stroke-width="1" opacity=".5">${Array.from({length:37},(_,i)=>`<line x1="${230+i*20}" y1="408" x2="${230+i*20}" y2="432"/>`).join('')}</g><line x1="230" y1="250" x2="970" y2="250" stroke="#fff" stroke-width="5"/><line x1="230" y1="590" x2="970" y2="590" stroke="#fff" stroke-width="5"/><line x1="600" y1="250" x2="600" y2="590" stroke="#fff" stroke-width="5"/></g><g class="an-ball"><circle r="14" fill="#E4F25C"/><path d="M-10 -6 Q0 0 -10 6M10 -6 Q0 0 10 6" stroke="#fff" stroke-width="2" fill="none"/></g></svg>`,
clinica:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><pattern id="px" width="90" height="90" patternUnits="userSpaceOnUse"><path d="M40 30h10v10h10v10H50v10H40V50H30V40h10z" fill="#CFE7E3"/></pattern></defs><rect width="1200" height="800" fill="#E8F4F2"/><rect width="1200" height="800" fill="url(#px)"/><polyline class="an-beat" points="0,560 300,560 340,560 370,470 400,650 430,520 455,560 700,560 740,560 770,470 800,650 830,520 855,560 1200,560" fill="none" stroke="#0E9384" stroke-width="5" stroke-linejoin="round"/><circle class="an-float" cx="1020" cy="170" r="90" fill="#CFE7E3"/></svg>`,
gym:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#16181D"/><g fill="#262A33">${[[180,180,-20],[980,240,25],[300,640,15],[900,620,-30],[620,120,5]].map(([x,y,r],i)=>`<g class="an-lift" style="animation-delay:${i*.4}s" transform="translate(${x} ${y}) rotate(${r})"><rect x="-90" y="-8" width="180" height="16" rx="6"/><rect x="-110" y="-40" width="26" height="80" rx="6"/><rect x="84" y="-40" width="26" height="80" rx="6"/><rect x="-82" y="-28" width="16" height="56" rx="5"/><rect x="66" y="-28" width="16" height="56" rx="5"/></g>`).join('')}</g><circle class="an-pulse" cx="600" cy="420" r="160" fill="none" stroke="#FF6B2C" stroke-width="3"/></svg>`,
pilates:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#F3E8DC"/><circle class="an-float" cx="180" cy="160" r="140" fill="#EBD9C6"/><circle class="an-float" style="animation-delay:1.5s" cx="1060" cy="640" r="180" fill="#EBD9C6"/><g transform="translate(330 470)" fill="none" stroke="#D2B596" stroke-width="10" stroke-linecap="round"><rect x="0" y="40" width="560" height="44" rx="22" fill="#E4CDB4" stroke="none"/><line x1="30" y1="84" x2="30" y2="150"/><line x1="530" y1="84" x2="530" y2="150"/><rect class="an-carriage" x="120" y="10" width="170" height="34" rx="12" fill="#D2B596" stroke="none"/><line x1="540" y1="40" x2="540" y2="-70"/><path d="M540 -70 Q420 -40 290 18"/></g></svg>`,
resto:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#6B2A1B"/>${[[260,560],[620,600],[960,540]].map(([x,y])=>`<g transform="translate(${x} ${y})"><ellipse rx="150" ry="46" fill="#7E3622"/><ellipse rx="100" ry="30" fill="#8C4029"/>${[-40,0,40].map((dx,j)=>`<path class="an-steam" style="animation-delay:${j*.6}s" d="M${dx} -50 q-18 -30 0 -60 q18 -30 0 -60" stroke="#C9826B" stroke-width="6" fill="none" stroke-linecap="round"/>`).join('')}</g>`).join('')}</svg>`,
pelu:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#F0E4F6"/><g class="an-snip" transform="translate(930 260)" fill="none" stroke="#D8BEE8" stroke-width="16" stroke-linecap="round"><circle cx="-60" cy="120" r="44"/><circle cx="60" cy="120" r="44"/><line x1="-30" y1="86" x2="80" y2="-140"/><line x1="30" y1="86" x2="-80" y2="-140"/></g>${[[200,200],[420,620],[760,140],[1040,600],[140,520]].map(([x,y],i)=>`<path class="an-twinkle" style="animation-delay:${i*.5}s" transform="translate(${x} ${y})" d="M0 -26 L7 -7 L26 0 L7 7 L0 26 L-7 7 L-26 0 L-7 -7Z" fill="#D8BEE8"/>`).join('')}</svg>`,
tienda:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#0F4D33"/>${[220,420,620].map((y,r)=>`<rect x="80" y="${y}" width="1040" height="14" rx="4" fill="#1B6B49"/>${[0,1,2,3,4,5].map(c=>`<rect class="an-box" style="animation-delay:${(r*6+c)*.15}s" x="${120+c*165}" y="${y-90}" width="${110-(c%3)*14}" height="${90-(c%2)*20}" rx="8" fill="${['#17633F','#1E7A4E','#145A39'][(c+r)%3]}" transform="translate(0 ${(c%2)*20})"/>`).join('')}`).join('')}</svg>`,
fabrica:`<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><pattern id="bp" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#16316B" stroke-width="1.5"/></pattern></defs><rect width="1200" height="800" fill="#0B1F4B"/><rect width="1200" height="800" fill="url(#bp)"/><g stroke="#24458F" stroke-width="8" fill="none"><path d="M900 760V150M940 760V150M900 200L940 240M940 300L900 340M900 400L940 440M900 500L940 540M940 600L900 640"/></g><g class="an-jib" style="transform-origin:920px 150px"><path d="M600 150H1100M640 150L920 90L1100 150" stroke="#24458F" stroke-width="8" fill="none"/><line class="an-hook" x1="700" y1="150" x2="700" y2="380" stroke="#FFC53D" stroke-width="3"/><rect class="an-hook" x="670" y="380" width="60" height="40" fill="#FFC53D" opacity=".7"/></g>${[0,1,2].map(i=>`<rect x="${180+i*130}" y="${560-i*120}" width="120" height="${200+i*120}" fill="#14306A" stroke="#24458F" stroke-width="4"/>`).join('')}</svg>`};

/* ---------- Cada negocio: tema, textos y módulos que se ven en movimiento ---------- */
const SECT={
padel:{name:'Canchas de pádel',your:'tu club',form:'Canchas de pádel o fútbol',bg:'#0D4F7A',dark:1,acc:'#C8F560',
 title:'Tu club de pádel, en piloto automático',sub:'Reservas, pagos, profesores, nómina e inventario funcionando solos mientras tú juegas.',
 mods:[{t:'Bot de reservas',k:'chat'},
  {t:'Agenda de canchas',k:'agenda',d:{cols:['Cancha 1','Cancha 2','Cancha 3'],rows:['5:00 p. m.','6:00 p. m.','7:00 p. m.','8:00 p. m.','9:00 p. m.'],book:[[1,0,'Andrés M.'],[2,1,'Torneo'],[2,2,'Laura P.'],[3,0,'Clase grupal'],[3,1,'Juan D.'],[4,2,'Sofía R.']],toast:'El bot agendó la reserva y envió el link de pago'}},
  {t:'Pagos',k:'pagos',d:[['Andrés M.','Cancha 1 · 6:00 p. m.',100000,1],['Laura P.','Cancha 3 · 7:00 p. m.',100000,1],['Juan D.','Cancha 2 · 8:00 p. m.',100000,0],['Clase grupal','6 alumnos',240000,1]]},
  {t:'Profesores y clases',k:'equipo',d:[['Camilo R.','Profesor','Mar y Jue · 7:00 p. m.','6 alumnos'],['Valentina S.','Profesora','Sáb · 9:00 a. m.','4 alumnos'],['Mateo L.','Recepción','Lun a Vie · 3:00 p. m.','Turno tarde']],toast:'Cada profesor recibió su horario por WhatsApp'},
  {t:'Nómina',k:'nomina',d:[['Camilo R.','Profesor','32 clases',1920000],['Valentina S.','Profesora','12 clases',720000],['Mateo L.','Recepción','30 días',1750000]]},
  {t:'Inventario',k:'inventario',d:[['Tubos de pelotas',40,8,10,'tubos'],['Raquetas de alquiler',12,9,4,'und'],['Agua y bebidas',96,30,24,'und'],['Grips',30,22,8,'und']]},
  {t:'Reporte al dueño',k:'reporte',d:['Ocupación de hoy: 82% (23 de 28 turnos)','Ingresos: $2.340.000','Pagos pendientes: 1 (recordatorio enviado)','Inventario: pedido de pelotas enviado al proveedor','Mañana: 19 reservas y 2 clases']}]},
clinica:{name:'Clínica',your:'tu clínica',form:'Clínica o consultorio',bg:'#E8F4F2',dark:0,acc:'#0E9384',
 title:'Tu clínica organizada sin llamadas ni papeles',sub:'Citas por especialista, recordatorios, insumos, proveedores y pagos conectados entre sí.',
 mods:[{t:'Bot de citas',k:'chat'},
  {t:'Agenda por especialista',k:'agenda',d:{cols:['Dra. Pérez · Odontología','Dr. Gómez · Ortodoncia','Dra. Ruiz · Higiene'],rows:['8:00 a. m.','9:00 a. m.','10:00 a. m.','11:00 a. m.'],book:[[0,0,'Valoración'],[0,2,'Limpieza'],[1,1,'Control'],[2,0,'Resina'],[2,2,'Limpieza'],[3,1,'Valoración']],toast:'Cita confirmada: recordatorio programado 24 h antes'}},
  {t:'Especialistas y turnos',k:'equipo',d:[['Dra. Pérez','Odontología general','Lun a Vie · 8 a. m. a 12 m.','14 citas'],['Dr. Gómez','Ortodoncia','Mar y Jue · 8 a. m. a 1 p. m.','9 citas'],['Dra. Ruiz','Higiene oral','Lun a Sáb · 8 a. m. a 11 a. m.','11 citas']],toast:'Cada especialista recibió su agenda del día'},
  {t:'Insumos',k:'inventario',d:[['Guantes de nitrilo',20,4,5,'cajas'],['Anestesia',60,38,15,'cartuchos'],['Resinas',25,6,8,'jeringas'],['Eyectores',500,320,100,'und']]},
  {t:'Proveedores',k:'pipeline',d:{item:'Pedido #318 · Guantes x 20 cajas y resinas x 15',steps:['Stock bajo detectado','Cotización al proveedor','Orden de compra enviada','Entregado en clínica'],toast:'Insumos recibidos y sumados al inventario'}},
  {t:'Pagos',k:'pagos',d:[['María L.','Limpieza',120000,1],['Jorge T.','Ortodoncia · cuota 4',250000,1],['Ana C.','Resina',180000,0],['Pedro V.','Valoración',60000,1]]},
  {t:'Reporte al dueño',k:'reporte',d:['Citas de hoy: 34 atendidas, 2 reprogramadas','Inasistencias: 1 (antes eran 6 por semana)','Ingresos: $3.120.000','Insumos: pedido de guantes en camino','Reseñas nuevas en Google: 3']}]},
gym:{name:'Gimnasio',your:'tu gimnasio',form:'Gimnasio',bg:'#16181D',dark:1,acc:'#FF6B2C',
 title:'Tu gimnasio cobra, agenda y vende solo',sub:'Mensualidades, instructores, nómina y tienda de suplementos sin perseguir a nadie.',
 mods:[{t:'Bot de ventas',k:'chat'},
  {t:'Mensualidades',k:'pagos',d:[['Daniela R.','Plan mensual',90000,1],['Felipe A.','Plan trimestral',240000,1],['Carlos M.','Plan mensual · vence hoy',90000,0],['Paula G.','Plan anual',850000,1],['Sergio L.','Plan mensual · vencido',90000,0]]},
  {t:'Instructores y clases',k:'equipo',d:[['Kevin P.','Funcional','Lun, Mié, Vie · 6:00 a. m.','18 inscritos'],['Natalia C.','Spinning','Mar y Jue · 7:00 p. m.','22 inscritos'],['Andrés V.','Pesas','Lun a Vie · 5:00 p. m.','Piso']],toast:'Clases publicadas y cupos abiertos en el bot'},
  {t:'Nómina',k:'nomina',d:[['Kevin P.','Instructor','48 clases',1680000],['Natalia C.','Instructora','24 clases',960000],['Andrés V.','Entrenador de piso','30 días',1850000],['Diana M.','Recepción','30 días',1750000]]},
  {t:'Tienda de suplementos',k:'inventario',d:[['Proteína 2 lb',24,5,6,'und'],['Creatina',18,11,5,'und'],['Bebidas',120,48,30,'und'],['Guantes',15,12,4,'pares']]},
  {t:'Reporte al dueño',k:'reporte',d:['Socios activos: 312','Mensualidades cobradas hoy: $2.150.000','Por vencer esta semana: 18 (recordatorios enviados)','Clases de prueba agendadas: 7','Stock bajo: proteína, pedido enviado']}]},
pilates:{name:'Pilates y yoga',your:'tu estudio',form:'Pilates o yoga',bg:'#F3E8DC',dark:0,acc:'#B86A4B',
 title:'Tu estudio con cupos llenos y cero cuadernos',sub:'Reservas por clase, paquetes, instructoras y pagos en orden.',
 mods:[{t:'Bot de reservas',k:'chat'},
  {t:'Cupos por clase',k:'agenda',d:{cols:['Lunes','Martes','Miércoles'],rows:['7:00 a. m.','9:00 a. m.','5:30 p. m.','6:30 p. m.'],book:[[0,0,'5/5 lleno'],[0,1,'4/5'],[1,2,'3/5'],[2,0,'5/5 lleno'],[2,1,'5/5 lleno'],[3,2,'2/5']],toast:'Cupo reservado y descontado del paquete'}},
  {t:'Paquetes y pagos',k:'pagos',d:[['Camila T.','Paquete 12 clases',380000,1],['Juliana P.','Paquete 8 clases',280000,1],['Mariana S.','Clase suelta',45000,0],['Lorena V.','Paquete 12 clases',380000,1]]},
  {t:'Instructoras',k:'equipo',d:[['Sara M.','Reformer','Lun a Vie · 7:00 a. m.','25 clases/mes'],['Daniela F.','Mat y yoga','Mar y Jue · 6:30 p. m.','9 clases/mes'],['Isabel G.','Reformer','Sáb · 9:00 a. m.','4 clases/mes']],toast:'Horarios enviados a cada instructora'},
  {t:'Nómina',k:'nomina',d:[['Sara M.','Instructora','25 clases',1250000],['Daniela F.','Instructora','9 clases',450000],['Isabel G.','Instructora','4 clases',200000]]},
  {t:'Reporte al dueño',k:'reporte',d:['Ocupación de la semana: 91%','Clases con lista de espera: 4','Paquetes por vencer: 6 (recordatorio enviado)','Ingresos de hoy: $1.085.000']}]},
resto:{name:'Restaurante',your:'tu restaurante',form:'Restaurante',bg:'#6B2A1B',dark:1,acc:'#FFB547',
 title:'Tu restaurante recibe pedidos sin perder ninguno',sub:'Pedidos directo a cocina, domicilios, inventario, proveedores y turnos del personal.',
 mods:[{t:'Bot de pedidos',k:'chat'},
  {t:'Pedido a cocina',k:'pipeline',d:{item:'Pedido #1287 · 2 hamburguesas, 2 limonadas',steps:['Pedido recibido por WhatsApp','En preparación','Domiciliario asignado','Entregado'],toast:'Cliente avisado en cada paso del pedido'}},
  {t:'Inventario de cocina',k:'inventario',d:[['Carne de res',30,7,8,'kg'],['Pan de hamburguesa',120,46,40,'und'],['Papa',50,31,15,'kg'],['Limones',200,60,50,'und']]},
  {t:'Proveedores',k:'pipeline',d:{item:'Orden #77 · Carne 25 kg y pan 100 und',steps:['Stock bajo detectado','Pedido al proveedor','Confirmado para mañana 7 a. m.','Recibido en cocina'],toast:'Inventario actualizado al recibir el pedido'}},
  {t:'Nómina y turnos',k:'nomina',d:[['Luis H.','Chef','26 turnos',2400000],['Marcela O.','Auxiliar de cocina','26 turnos',1600000],['Brayan S.','Mesero','22 turnos',1450000],['Óscar P.','Domiciliario','24 turnos',1500000]]},
  {t:'Reporte al dueño',k:'reporte',d:['Pedidos de hoy: 86 (41 domicilios)','Ventas: $3.870.000','Plato más vendido: hamburguesa de la casa','Pedido de carne confirmado para mañana']}]},
pelu:{name:'Peluquería y spa',your:'tu salón',form:'Peluquería o spa',bg:'#F0E4F6',dark:0,acc:'#8E44C2',
 title:'Tu salón con la agenda llena y sin huecos',sub:'Citas por estilista, anticipos, comisiones y productos en orden.',
 mods:[{t:'Bot de citas',k:'chat'},
  {t:'Agenda por estilista',k:'agenda',d:{cols:['Laura · Corte y color','Andrea · Uñas','Felipe · Barbería'],rows:['9:00 a. m.','10:30 a. m.','2:00 p. m.','4:00 p. m.'],book:[[0,0,'Color'],[0,1,'Semipermanente'],[1,2,'Corte y barba'],[2,0,'Cepillado'],[2,1,'Pedicure'],[3,2,'Corte']],toast:'Cita agendada con anticipo y recordatorio'}},
  {t:'Anticipos y pagos',k:'pagos',d:[['Valeria G.','Color · anticipo',60000,1],['Natalia R.','Uñas semipermanente',45000,1],['Kevin T.','Corte y barba',35000,0],['Mónica A.','Keratina · anticipo',100000,1]]},
  {t:'Comisiones',k:'nomina',d:[['Laura','Estilista · 40%','$4.200.000 en servicios',1680000],['Andrea','Manicurista · 40%','$2.100.000 en servicios',840000],['Felipe','Barbero · 40%','$2.600.000 en servicios',1040000]]},
  {t:'Productos',k:'inventario',d:[['Tinte 7.1',18,3,4,'und'],['Esmaltes',60,41,15,'und'],['Shampoo profesional',12,7,3,'und'],['Keratina',8,2,2,'kits']]},
  {t:'Reporte al dueño',k:'reporte',d:['Citas de hoy: 27','Ingresos: $1.940.000','Huecos libres mañana: 3 (ofrecidos a clientes frecuentes)','Producto por agotarse: tinte 7.1, pedido enviado']}]},
tienda:{name:'Tienda o ferretería',your:'tu tienda',form:'Tienda o ferretería',bg:'#0F4D33',dark:1,acc:'#C8F560',
 title:'Tu tienda vende por chat y nunca se queda sin stock',sub:'Pedidos, inventario, proveedores, cartera y nómina conectados.',
 mods:[{t:'Bot de ventas',k:'chat'},
  {t:'Inventario',k:'inventario',d:[['Tableros de melamina',60,9,12,'und'],['Bisagras',500,260,100,'und'],['Pintura blanca',40,12,10,'galones'],['Tornillos 1"',3000,800,500,'und']]},
  {t:'Proveedores',k:'pipeline',d:{item:'Orden #540 · Tableros x 50',steps:['Stock bajo detectado','Orden de compra enviada','Despachado por el proveedor','Recibido en bodega'],toast:'Stock actualizado y vendedores avisados'}},
  {t:'Cartera',k:'pagos',d:[['Muebles El Roble','Factura 2201',1250000,1],['Obra Calle 80','Factura 2207',3400000,0],['Carpintería JM','Factura 2210',780000,1],['Constructora Lince','Factura 2214',2150000,0]]},
  {t:'Nómina',k:'nomina',d:[['Ricardo P.','Vendedor','30 días',1900000],['Yuli C.','Caja','30 días',1750000],['Edwin M.','Bodega','30 días',1750000]]},
  {t:'Reporte al dueño',k:'reporte',d:['Ventas de hoy: $6.420.000','Pedidos por WhatsApp: 38','Cartera vencida: $5.550.000 (recordatorios enviados)','Orden de tableros en camino']}]},
fabrica:{name:'Constructora o fábrica',your:'tu empresa',form:'Fábrica o constructora',bg:'#0B1F4B',dark:1,acc:'#FFC53D',
 title:'Tu obra controlada desde el celular',sub:'Cotizaciones, proveedores, materiales, cuadrillas y nómina de obra sin hojas sueltas.',
 mods:[{t:'Bot de cotizaciones',k:'chat'},
  {t:'Proveedores y materiales',k:'pipeline',d:{item:'Orden #912 · Cemento x 120 bultos, varilla 1/2" x 80',steps:['Solicitud desde la obra','3 cotizaciones comparadas','Orden al mejor precio','Entregado en obra'],toast:'Material recibido y descontado del presupuesto'}},
  {t:'Materiales en bodega',k:'inventario',d:[['Cemento',200,35,40,'bultos'],['Varilla 1/2"',300,140,60,'und'],['Ladrillo',8000,2600,1500,'und'],['Arena',30,9,8,'m³']]},
  {t:'Cuadrillas y obras',k:'equipo',d:[['Cuadrilla A','Obra Calle 80','Estructura · piso 4','8 personas'],['Cuadrilla B','Casa Los Pinos','Mampostería','5 personas'],['Cuadrilla C','Bodega Norte','Acabados','6 personas']],toast:'Cada maestro recibió las tareas del día'},
  {t:'Nómina de obra',k:'nomina',d:[['Cuadrilla A','8 personas','Quincena',9600000],['Cuadrilla B','5 personas','Quincena',6000000],['Cuadrilla C','6 personas','Quincena',7200000],['Residente de obra','Ingeniero','Quincena',2800000]]},
  {t:'Anticipos y cartera',k:'pagos',d:[['Familia Ruiz','Anticipo 30%',27000000,1],['Inversiones Sol','Corte de obra 2',45000000,0],['Bodega Norte S.A.S.','Corte de obra 1',38000000,1]]},
  {t:'Reporte al dueño',k:'reporte',d:['Avance Obra Calle 80: 62%','Material entregado hoy: cemento y varilla','Gasto vs. presupuesto: 48% usado','Cuenta por cobrar: $45.000.000 (recordatorio enviado)']}]}};

/* ---------- Utilidades de animación ---------- */
const money=n=>'$'+Math.round(n).toLocaleString('es-CO');
let runId=0;
const later=(id,ms,fn)=>setTimeout(()=>{if(id===runId)fn();},ms);
function countUp(node,to,id,ms=1200){const t0=performance.now();const step=t=>{if(id!==runId)return;const k=Math.min(1,(t-t0)/ms);node.textContent=money(to*k);if(k<1)requestAnimationFrame(step);};requestAnimationFrame(step);}
function toast(stage,text,id,ms){later(id,ms,()=>{const t=el('div','toast','✓ '+text);stage.append(t);});}
function row(cols,cls){const r=el('div','mrow'+(cls?' '+cls:''));cols.forEach(c=>{const x=typeof c==='string'?el('div',null,c):c;r.append(x);});return r;}

/* ---------- Módulos ---------- */
const MOD={
agenda(stage,d,id){const g=el('div','agenda');g.style.gridTemplateColumns=`90px repeat(${d.cols.length},minmax(0,1fr))`;
 g.append(el('div'));d.cols.forEach(c=>g.append(el('div','ahead',c)));
 const cells={};d.rows.forEach((r,i)=>{g.append(el('div','atime',r));d.cols.forEach((_,j)=>{const c=el('div','acell','Libre');cells[i+'-'+j]=c;g.append(c);});});
 stage.append(g);d.book.forEach(([i,j,n],k)=>later(id,500+k*550,()=>{const c=cells[i+'-'+j];c.textContent=n;c.classList.add('booked');}));
 toast(stage,d.toast,id,600+d.book.length*550);},
pagos(stage,d,id){const tot=el('div','bigsum');tot.innerHTML='<span>Recaudado</span><strong>$0</strong>';stage.append(tot);
 let sum=0;d.forEach(([n,c,v,ok],k)=>later(id,400+k*600,()=>{const st=el('span','badge '+(ok?'ok':'warn'),ok?'Pagado ✓':'Pendiente');
  stage.insertBefore(row([el('strong',null,n),c,el('span','num',money(v)),st]),tot);
  if(ok){sum+=v;countUp(tot.querySelector('strong'),sum,id,500);}else later(id,900,()=>{st.textContent='Recordatorio enviado';st.className='badge info';});}));},
nomina(stage,d,id){const tot=el('div','bigsum');tot.innerHTML='<span>Total nómina</span><strong>$0</strong>';
 const rows=d.map(([n,c,b,v])=>{const val=el('span','num','Calculando…');const st=el('span','badge','En cola');const r=row([el('strong',null,n),c,b,val,st]);r._v=v;r._val=val;r._st=st;stage.append(r);return r;});stage.append(tot);
 let sum=0;rows.forEach((r,k)=>later(id,500+k*700,()=>{r._val.textContent=money(r._v);r._st.textContent='Pagado ✓';r._st.className='badge ok';sum+=r._v;countUp(tot.querySelector('strong'),sum,id,500);}));
 toast(stage,'Desprendibles de pago enviados a cada persona por WhatsApp',id,700+rows.length*700);},
inventario(stage,d,id){d.forEach(([n,from,to,min,u],k)=>{const bar=el('div','bar');const fill=el('i');bar.append(fill);const q=el('span','num',from+' '+u);
  const r=row([el('strong',null,n),bar,q]);r.classList.add('inv');stage.append(r);fill.style.width='100%';
  later(id,400+k*250,()=>{fill.style.width=Math.max(4,to/from*100)+'%';let t0=performance.now();const tick=t=>{if(id!==runId)return;const kk=Math.min(1,(t-t0)/1600);q.textContent=Math.round(from-(from-to)*kk)+' '+u;if(kk<1)requestAnimationFrame(tick);};requestAnimationFrame(tick);
   if(to<=min)later(id,1700,()=>{bar.classList.add('low');toast(stage,'Stock bajo de '+n.toLowerCase()+': pedido automático enviado al proveedor',id,200);});});});},
pipeline(stage,d,id){stage.append(el('p','pitem',d.item));const p=el('div','pipe');const st=d.steps.map((s,i)=>{const x=el('div','pstep');x.append(el('span','pdot',String(i+1)),el('span',null,s));p.append(x);return x;});stage.append(p);
 st.forEach((x,i)=>later(id,500+i*900,()=>{st.forEach(y=>y.classList.remove('now'));x.classList.add('done','now');}));toast(stage,d.toast,id,600+st.length*900);},
equipo(stage,d,id){d.forEach(([n,r,h,x],k)=>{const b=el('span','badge','Asignando…');stage.append(row([el('strong',null,n),r,h,x,b]));later(id,500+k*600,()=>{b.textContent='Asignado ✓';b.className='badge ok';});});
 toast(stage,d.toast||'Horarios enviados a cada persona',id,700+d.length*600);},
reporte(stage,d,id){const ph=el('div','phone');const hd=el('div','phead');hd.innerHTML='<b>Glysf · Asistente</b><small>Reporte diario · 8:00 p. m.</small>';ph.append(hd);stage.append(ph);
 const msg=el('div','bub b');msg.style.cssText='max-width:100%;white-space:pre-line';ph.append(msg);msg.textContent='Hola, este es el resumen de hoy:';
 d.forEach((l,k)=>later(id,600+k*650,()=>{msg.textContent+='\n• '+l;}));}};

/* ---------- Vista de negocio ---------- */
let cur='padel',modIx=0;
function openSector(k,ix){cur=k;modIx=ix||0;const s=SECT[k];chatSector(k);
 $('home').hidden=true;const v=$('sectorView');v.hidden=false;
 v.style.setProperty('--bg',s.bg);v.style.setProperty('--acc',s.acc);v.classList.toggle('dark',!!s.dark);
 const sc=$('scene');sc.classList.remove('in');void sc.offsetWidth;sc.innerHTML=SCENE[k];sc.classList.add('in');
 $('svTabs').replaceChildren(...Object.keys(SECT).map(x=>{const a=el('a','svtab',SECT[x].name);a.href='#/negocio/'+x;if(x===k)a.setAttribute('aria-current','page');return a;}));
 const hero=$('svHero');hero.classList.remove('rise');void hero.offsetWidth;hero.classList.add('rise');
 $('svTitle').textContent=s.title;$('svSub').textContent=s.sub;$('svCta').textContent='Pide tu cotización';
 renderMods();window.scrollTo({top:0});document.title='Glysf para '+s.your.replace('tu ','')+' · Automatización con IA';heroStop();}
function renderMods(){const s=SECT[cur];
 $('modTabs').replaceChildren(...s.mods.map((m,i)=>{const b=el('button','mtab',m.t);b.type='button';b.setAttribute('role','tab');b.setAttribute('aria-selected',i===modIx);b.onclick=()=>{modIx=i;renderMods();};return b;}));
 runId++;const id=runId;const m=s.mods[modIx];const stage=$('modStage');stage.classList.remove('rise');void stage.offsetWidth;stage.classList.add('rise');
 $('modTitle').textContent=m.t;$('chatBox').hidden=m.k!=='chat';$('modBody').hidden=m.k==='chat';
 if(m.k==='chat'){startChat();}else{const b=$('modBody');b.replaceChildren();MOD[m.k](b,m.d,id);}
 $('modNext').textContent=modIx<s.mods.length-1?'Siguiente: '+s.mods[modIx+1].t:'Ver otro negocio';}
$('modNext').onclick=()=>{const s=SECT[cur];if(modIx<s.mods.length-1){modIx++;renderMods();}else{const ks=Object.keys(SECT);location.hash='#/negocio/'+ks[(ks.indexOf(cur)+1)%ks.length];}};
$('modReplay').onclick=()=>renderMods();
$('svCta').onclick=e=>{e.preventDefault();location.hash='#cotizar';setTimeout(()=>{const sel=document.querySelector('#quote select[name=sector]');sel.value=SECT[cur].form;},50);};

/* ---------- Tarjetas de negocios en el inicio ---------- */
$('bizGrid').replaceChildren(...Object.keys(SECT).map(k=>{const s=SECT[k];const a=el('a','biz'+(s.dark?' dark':''));a.href='#/negocio/'+k;
 const bg=el('div','bizbg');bg.innerHTML=SCENE[k];const tx=el('div','biztx');tx.append(el('strong',null,s.name),el('span',null,s.mods.length+' automatizaciones en la demo'));a.append(bg,tx);return a;}));

/* ---------- Navegación ---------- */
function route(){const h=location.hash;const m=h.match(/^#\/negocio\/(\w+)/);
 if(m&&SECT[m[1]]){openSector(m[1]);return;}
 runId++;$('sectorView').hidden=true;$('home').hidden=false;document.title='Glysf · Automatización con IA para empresas';heroWake();
 if(h&&h.length>1){const t=document.getElementById(h.slice(1));if(t)setTimeout(()=>t.scrollIntoView(),0);}}
window.addEventListener('hashchange',route);route();

