#!/usr/bin/env python3
"""Genera una página inmersiva por tipo de negocio (padel.html, clinica.html, …) desde una sola plantilla.

Uso:  python3 herramientas/generar_negocios.py
Edita los textos en NEGOCIOS y vuelve a ejecutar. Todas las páginas comparten negocio.css y negocio.js.
Fotos: Unsplash (licencia libre), se cargan desde su CDN por id.
"""
import html, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
WA_SVG = re.search(r'<svg viewBox="0 0 32 32".*?</svg>', (RAIZ / 'index.html').read_text(encoding='utf-8'), re.S).group(0)
MAIL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'

# ---------- Objetos de la portada (SVG 200×200) ----------
OBJ = {
'pelota': '''<svg viewBox="0 0 200 200"><defs><radialGradient id="o1" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#F6FF8A"/><stop offset=".55" stop-color="#D9EE2C"/><stop offset="1" stop-color="#7E9410"/></radialGradient></defs><circle cx="100" cy="100" r="96" fill="url(#o1)"/><path d="M28 40 C78 70 78 130 28 162M172 40 C122 70 122 130 172 162" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".9"/></svg>''',
'diente': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#E4F3F0"/><stop offset="1" stop-color="#9CC9C1"/></linearGradient></defs><path d="M100 30c-14-10-46-14-62 6-16 20-10 52 0 70 8 14 10 40 16 62 4 14 18 14 22 0 6-22 8-40 24-40s18 18 24 40c4 14 18 14 22 0 6-22 8-48 16-62 10-18 16-50 0-70-16-20-48-16-62-6z" fill="url(#o2)"/><path d="M70 52c8-6 20-6 28 0" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none" opacity=".9"/><circle cx="150" cy="44" r="16" fill="#7EE0C3"/><path d="M150 36v16M142 44h16" stroke="#06302A" stroke-width="4" stroke-linecap="round"/></svg>''',
'pesa': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A505C"/><stop offset="1" stop-color="#15171C"/></linearGradient><linearGradient id="o3b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6E9EF"/><stop offset="1" stop-color="#8C94A3"/></linearGradient></defs><g transform="rotate(-20 100 100)"><rect x="40" y="92" width="120" height="16" rx="6" fill="url(#o3b)"/><rect x="18" y="58" width="30" height="84" rx="9" fill="url(#o3)"/><rect x="152" y="58" width="30" height="84" rx="9" fill="url(#o3)"/><rect x="6" y="70" width="16" height="60" rx="6" fill="url(#o3)"/><rect x="178" y="70" width="16" height="60" rx="6" fill="url(#o3)"/><rect x="22" y="64" width="6" height="72" rx="3" fill="#FF8A4C" opacity=".9"/><rect x="172" y="64" width="6" height="72" rx="3" fill="#FF8A4C" opacity=".9"/></g></svg>''',
'aro': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o4" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FBE3CF"/><stop offset="1" stop-color="#C98B67"/></linearGradient></defs><circle cx="100" cy="100" r="78" fill="none" stroke="url(#o4)" stroke-width="16"/><rect x="12" y="84" width="26" height="32" rx="10" fill="#F2C6A0"/><rect x="162" y="84" width="26" height="32" rx="10" fill="#F2C6A0"/><circle cx="100" cy="100" r="78" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="40 460" opacity=".7"/></svg>''',
'campana': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o5" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF3D6"/><stop offset=".5" stop-color="#E3C27A"/><stop offset="1" stop-color="#8A6326"/></linearGradient></defs><path d="M26 138a74 74 0 0 1 148 0z" fill="url(#o5)"/><circle cx="100" cy="58" r="10" fill="url(#o5)"/><rect x="14" y="138" width="172" height="14" rx="7" fill="#C9A15A"/><path d="M58 96c10-16 26-24 42-26" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none" opacity=".75"/></svg>''',
'tijeras': '''<svg viewBox="0 0 200 200"><g fill="none" stroke-linecap="round"><path d="M88 108 172 26" stroke="#E9E4F2" stroke-width="12"/><path d="M112 108 28 26" stroke="#C9C1D8" stroke-width="12"/><circle cx="66" cy="150" r="28" stroke="#E3B5FF" stroke-width="12"/><circle cx="134" cy="150" r="28" stroke="#E3B5FF" stroke-width="12"/></g><circle cx="100" cy="104" r="8" fill="#fff"/></svg>''',
'caja': '''<svg viewBox="0 0 200 200"><path d="M100 22 176 60v82l-76 38-76-38V60z" fill="#C9935A"/><path d="M100 22 176 60l-76 38-76-38z" fill="#E2B27C"/><path d="M100 98v82l-76-38V60z" fill="#B07A44"/><path d="M62 41l76 38v26" stroke="#F3D4A7" stroke-width="12" fill="none"/><rect x="118" y="128" width="40" height="18" rx="3" transform="skewY(-26)" fill="#C8F560" opacity=".9"/></svg>''',
'casco': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o8" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE38A"/><stop offset=".55" stop-color="#FFC53D"/><stop offset="1" stop-color="#B07E0A"/></linearGradient></defs><path d="M30 132a70 70 0 0 1 140 0z" fill="url(#o8)"/><path d="M84 66h32v66H84z" fill="#FFD460"/><rect x="14" y="128" width="172" height="20" rx="10" fill="#E2A91F"/><path d="M52 112c4-22 16-38 30-44" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none" opacity=".7"/></svg>''',
}

OBJ.update({'calculadora': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o9" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A4766"/><stop offset="1" stop-color="#0E1530"/></linearGradient></defs><rect x="44" y="14" width="112" height="172" rx="16" fill="url(#o9)"/><rect x="58" y="30" width="84" height="34" rx="6" fill="#B8F2D9"/><text x="134" y="55" text-anchor="end" font-family="monospace" font-size="18" fill="#0B1F4B">2.340</text><g fill="#5B6A90">''' + ''.join(f'<rect x="{58+c*30}" y="{78+r*26}" width="22" height="18" rx="5"/>' for r in range(4) for c in range(3)) + '''</g><rect x="148" y="78" width="0" height="0"/><rect x="118" y="156" width="22" height="18" rx="5" fill="#9BE7C4"/></svg>''',
'balanza': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o10" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF1C9"/><stop offset=".6" stop-color="#D9B25C"/><stop offset="1" stop-color="#8A6A22"/></linearGradient></defs><g fill="none" stroke="url(#o10)" stroke-width="8" stroke-linecap="round"><path d="M100 26v140M30 52h140M30 52 12 112M30 52l18 60M170 52l-18 60M170 52l18 60"/></g><path d="M8 112a22 12 0 0 0 44 0z" fill="url(#o10)"/><path d="M148 112a22 12 0 0 0 44 0z" fill="url(#o10)"/><rect x="66" y="166" width="68" height="14" rx="7" fill="url(#o10)"/><circle cx="100" cy="26" r="9" fill="url(#o10)"/></svg>''',
'camion': '''<svg viewBox="0 0 200 200"><rect x="10" y="62" width="112" height="80" rx="8" fill="#E8EEF9"/><rect x="10" y="62" width="112" height="16" rx="6" fill="#7FD4F5"/><path d="M122 86h38l26 28v28h-64z" fill="#7FD4F5"/><path d="M134 94h22l16 18h-38z" fill="#0B1F4B" opacity=".55"/><circle cx="46" cy="148" r="17" fill="#141A2E"/><circle cx="46" cy="148" r="7" fill="#C9D3E6"/><circle cx="156" cy="148" r="17" fill="#141A2E"/><circle cx="156" cy="148" r="7" fill="#C9D3E6"/><path d="M26 100h50M26 116h34" stroke="#9FB2D6" stroke-width="7" stroke-linecap="round"/></svg>''',
'engranaje': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o12" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F6FA"/><stop offset="1" stop-color="#8E97A8"/></linearGradient></defs><g fill="url(#o12)">''' + ''.join(f'<rect x="88" y="10" width="24" height="40" rx="5" transform="rotate({a} 100 100)"/>' for a in range(0,360,45)) + '''<circle cx="100" cy="100" r="62"/></g><circle cx="100" cy="100" r="26" fill="#0B1530"/><circle cx="100" cy="100" r="62" fill="none" stroke="#FFB347" stroke-width="4" stroke-dasharray="30 360" opacity=".9"/></svg>''',
'bolsa': '''<svg viewBox="0 0 200 200"><defs><linearGradient id="o13" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFC6E4"/><stop offset="1" stop-color="#C24C8C"/></linearGradient></defs><path d="M70 66V52a30 30 0 0 1 60 0v14" fill="none" stroke="#F7D9EA" stroke-width="10" stroke-linecap="round"/><path d="M34 66h132l-10 112H44z" fill="url(#o13)"/><path d="M62 96c8 22 68 22 76 0" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".85"/></svg>'''
})


# ---------- Iconos de marca: mismo trazo redondeado de la "g" y un nodo de color (var(--acc)) ----------
def _ic(paths, nodes):
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--acc)"/>' for x, y, r in nodes)
    return (f'<svg viewBox="0 0 200 200"><g fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round">{paths}</g>{dots}</svg>')
OBJ = {
 'pelota': _ic('<g transform="rotate(-35 92 84)"><ellipse cx="92" cy="74" rx="46" ry="54"/><path d="M92 128v44"/><path d="M76 52h.1M92 52h.1M108 52h.1M68 72h.1M84 72h.1M100 72h.1M116 72h.1M76 92h.1M92 92h.1M108 92h.1" stroke-width="9"/></g>', [(160,52,15)]),
 'diente': _ic('<path d="M100 54c-12-10-38-14-52 2-14 16-8 44 0 60 7 13 9 33 14 50 4 12 15 12 18 0 5-18 7-32 20-32s15 14 20 32c3 12 14 12 18 0 5-17 7-37 14-50 8-16 14-44 0-60-14-16-40-12-52-2z"/>', [(156,46,13)]),
 'pesa': _ic('<path d="M66 100h68M44 64v72M64 76v48M136 76v48M156 64v72"/>', [(180,100,12),(20,100,12)]),
 'aro': _ic('<circle cx="100" cy="104" r="58"/><path d="M30 92v24M170 92v24"/>', [(100,46,13)]),
 'campana': _ic('<path d="M38 140a62 62 0 0 1 124 0M24 140h152M100 78v-6"/>', [(100,58,13)]),
 'tijeras': _ic('<circle cx="66" cy="148" r="22"/><circle cx="134" cy="148" r="22"/><path d="M80 131 152 40M120 131 48 40"/>', [(100,98,12)]),
 'caja': _ic('<path d="M100 32 164 64v72l-64 32-64-32V64z"/><path d="M36 64l64 32 64-32M100 96v72"/>', [(164,64,13)]),
 'casco': _ic('<path d="M42 134a58 58 0 0 1 116 0M28 134h144M100 76V58"/><path d="M76 92c4-8 10-13 16-15" stroke-width="7" opacity=".55"/>', [(100,46,13)]),
 'calculadora': _ic('<rect x="54" y="26" width="92" height="148" rx="18"/><path d="M76 60h48"/><path d="M78 98h.1M100 98h.1M122 98h.1M78 122h.1M100 122h.1M122 122h.1M78 146h.1M100 146h.1" stroke-width="15"/>', [(122,146,10)]),
 'balanza': _ic('<path d="M100 44v112M64 158h72M40 66h120M40 66 22 112h36zM160 66l-18 46h36z"/>', [(100,40,13)]),
 'camion': _ic('<path d="M22 64h96v72H22zM118 90h34l24 26v20h-58"/><circle cx="54" cy="146" r="16"/><circle cx="148" cy="146" r="16"/>', [(176,116,11)]),
 'engranaje': _ic('<circle cx="100" cy="100" r="46"/><path d="M100 40v-8M100 160v8M40 100h-8M160 100h8M57 57l-6-6M143 143l6 6M143 57l6-6M57 143l-6 6" stroke-width="24"/>', [(100,100,16)]),
 'navegador': _ic('<rect x="26" y="40" width="148" height="120" rx="16"/><path d="M26 72h148M58 104h60M58 128h36"/><path d="M44 56h.1M58 56h.1" stroke-width="10"/>', [(140,128,13)]),
 'bolsa': _ic('<path d="M44 72h112l-10 100H54zM74 72V60a26 26 0 0 1 52 0v12"/><path d="M78 104c8 14 36 14 44 0"/>', [(122,104,10)]),
}

# ---------- Contenido por negocio ----------
# chat: (quién, texto) con quién = u (cliente), b (bot) o pay (aviso de pago "Texto|Valor")
# cards: (etiqueta, título, [(hora, ocupado)], precio, posición de la foto)
# ops: tarjetas (título, [(texto, estado, clase, cambia_a)]) o ('inv', título, [(nombre, porcentaje, texto, cambia_a)])
OBJ['balon'] = _ic('<circle cx="100" cy="100" r="62"/><path d="M100 76l23 17-9 27H86l-9-27z"/><path d="M100 76V40M123 93l32-12M114 120l20 28M86 120l-20 28M77 93l-32-12"/>', [(160,42,13)])
OBJ['voleibol'] = _ic('<circle cx="100" cy="100" r="62"/><path d="M100 38c-22 32-22 78 0 124"/><path d="M42 84c38 4 76 28 100 70"/><path d="M58 146c18-34 52-58 100-64"/>', [(164,40,13)])

NEGOCIOS = {
'padel': dict(nombre='Canchas de pádel', archivo='padel', palabra='PÁDEL', obj='pelota', acc='#D9EE2C', su='tu club',
  foto='1709587825135-80b00570c355', foto2='1673266893352-6de89e258064', foto3='1612534847738-b3af9bc31f0c',
  seo='Automatización para clubes de pádel', desc='Reservas por WhatsApp 24/7, cobros, recordatorios, profesores, inventario y el reporte del día de tu club de pádel.',
  kicker='Glysf para clubes de pádel', hero=('Canchas que se reservan solas,', 'de día y de noche.'),
  bot_t=('El bot reserva', 'mientras tú juegas.'), bot_sub='Responde por WhatsApp en segundos, ofrece la cancha libre y cobra el anticipo.', bot_nombre='Club Pádel Norte',
  chat=[('u','Hola, ¿hay cancha hoy a las 7?'),('b','¡Hola! A las 7:00 p. m. está libre la cancha 2. ¿1 hora o 90 minutos?'),('u','90 min, somos 4'),('b','Listo: cancha 2, hoy de 7:00 a 8:30 p. m. Te envío el link para asegurar tu turno.'),('pay','Pago recibido|$100.000'),('b','Pago confirmado. Te recuerdo una hora antes.')],
  cards_t=('Tus canchas,', 'siempre llenas.'), cards_num='02 · Agenda',
  cards=[('Cancha 1 · Panorámica','Vidrio y LED',[('5 p. m.',1),('6 p. m.',1),('7 p. m.',1),('8 p. m.',1)],'$100.000','1709587825135-80b00570c355'),
         ('Cancha 2 · Cubierta','Juega aunque llueva',[('5 p. m.',1),('6 p. m.',1),('7 p. m.',1),('8 p. m.',0)],'$90.000','1646649853703-7645147474ba'),
         ('Cancha 3 · Clases','Escuela y torneos',[('5 p. m.',1),('6 p. m.',0),('7 p. m.',1),('8 p. m.',1)],'$80.000','1657704358775-ed705c7388d2')],
  meter=(82,'% de ocupación hoy ·',23,'de 28 turnos'),
  ops_t=('Cobros, profesores e inventario','en orden.'),
  ops=[('Pagos de hoy',[('Andrés M. · Cancha 1','Pagado','ok',''),('Laura P. · Cancha 3','Pagado','ok',''),('Juan D. · Cancha 2','Pendiente','warn','Recordatorio enviado')]),
       ('Profesores',[('Camilo R. · Mar y Jue 7 p. m.','Asignado','ok',''),('Valentina S. · Sáb 9 a. m.','Asignado','ok',''),('Nómina del mes','Calculando…','ok','Pagada')]),
       ('inv','Inventario',[('Tubos de pelotas',20,'40 tubos','Pedido enviado al proveedor'),('Grips',70,'22 und','')])],
  reporte=['Ocupación: 82% (23 de 28 turnos)','Ingresos: $2.340.000','Pagos pendientes: 1, recordatorio enviado','Pedido de pelotas enviado al proveedor','Mañana: 19 reservas y 2 clases'],
  final=('Cada gran noche','empieza con un buen golpe.')),

'futbol': dict(nombre='Canchas de fútbol', archivo='futbol', palabra='FÚTBOL', obj='balon', acc='#5BE37D', su='tu complejo',
  foto='1487466365202-1afdb86c764e',
  seo='Automatización para canchas sintéticas de fútbol', desc='Reservas de fútbol 5 y 8 por WhatsApp 24/7, anticipos, recordatorios, torneos, árbitros e inventario de tu complejo deportivo.',
  kicker='Glysf para canchas de fútbol', hero=('Canchas sintéticas reservadas,', 'sin contestar el celular.'),
  bot_t=('El bot arma el partido', 'mientras tú atiendes.'), bot_sub='Muestra la cancha libre, cobra el anticipo y le recuerda al equipo antes del partido.', bot_nombre='Complejo La Sintética',
  chat=[('u','Buenas, ¿hay cancha de fútbol 5 el jueves a las 8?'),('b','¡Hola! El jueves a las 8:00 p. m. está libre la cancha 3 (fútbol 5). ¿Te la aparto?'),('u','Sí, somos 10'),('b','Listo: cancha 3, jueves de 8:00 a 9:00 p. m. Te envío el link del anticipo para dejarla separada.'),('pay','Anticipo recibido|$60.000'),('b','Anticipo confirmado. Le recuerdo al equipo el jueves a las 6 p. m.')],
  cards_t=('Tus canchas,', 'llenas toda la semana.'), cards_num='02 · Agenda',
  cards=[('Cancha 1 · Fútbol 8','Grama sintética',[('6 p. m.',1),('7 p. m.',1),('8 p. m.',1),('9 p. m.',1)],'$180.000','center 40%'),
         ('Cancha 2 · Fútbol 5','Cubierta',[('6 p. m.',1),('7 p. m.',1),('8 p. m.',0),('9 p. m.',1)],'$120.000','left 50%'),
         ('Cancha 3 · Fútbol 5','Torneo nocturno',[('6 p. m.',0),('7 p. m.',1),('8 p. m.',1),('9 p. m.',1)],'$120.000','right 50%')],
  meter=(88,'% de ocupación hoy ·',14,'de 16 turnos'),
  ops_t=('Anticipos, torneos y árbitros','en orden.'),
  ops=[('Anticipos de hoy',[('Los Parceros · Cancha 1','Pagado','ok',''),('Oficina Andina · Cancha 2','Pagado','ok',''),('Deportivo 10 · Cancha 3','Pendiente','warn','Link de pago reenviado')]),
       ('Torneo nocturno',[('Fecha 4 · 8 equipos','Programada','ok',''),('Árbitro del jueves','Asignado','ok',''),('Inscripción Real Barrio','Pendiente','warn','Recordatorio enviado')]),
       ('inv','Inventario',[('Balones',20,'6 und','Pedido enviado al proveedor'),('Petos',70,'40 und','')])],
  reporte=['Ocupación: 88% (14 de 16 turnos)','Ingresos: $1.860.000','Anticipos pendientes: 1, link reenviado','Torneo: fecha 4 programada con árbitro','Mañana: 15 reservas'],
  final=('Cada partido,','agendado sin una llamada.')),

'voley': dict(nombre='Canchas de vóley', archivo='voley', palabra='VÓLEY', obj='voleibol', acc='#FF9F5A', su='tu club',
  foto='1547347298-4074fc3086f0',
  seo='Automatización para canchas y escuelas de vóley', desc='Reservas de cancha, inscripciones a la escuela, mensualidades, entrenadores y torneos de vóley, funcionando solos.',
  kicker='Glysf para canchas de vóley', hero=('Tu cancha de vóley organizada,', 'sin perseguir a nadie.'),
  bot_t=('El bot inscribe', 'mientras tú entrenas.'), bot_sub='Reserva la cancha, inscribe en la escuela y cobra la mensualidad por WhatsApp.', bot_nombre='Club Vóley Altamira',
  chat=[('u','Hola, ¿tienen escuela de vóley para mi hija de 12?'),('b','¡Hola! Sí: categoría infantil, martes y jueves de 4:00 a 5:30 p. m. Quedan 3 cupos.'),('u','¿Cuánto vale el mes?'),('b','$150.000 al mes. Te envío el link para inscribirla y apartar el cupo.'),('pay','Mensualidad recibida|$150.000'),('b','¡Listo, quedó inscrita! Te recuerdo la primera clase el martes.')],
  cards_t=('Cancha y escuela,', 'sin cruces de horario.'), cards_num='02 · Horarios',
  cards=[('Cancha principal','Duela · cubierta',[('4 p. m.',1),('5 p. m.',1),('6 p. m.',1),('7 p. m.',0)],'$90.000','center 40%'),
         ('Escuela infantil','Martes y jueves',[('Cupo 1',1),('Cupo 2',1),('Cupo 3',0),('Cupo 4',0)],'$150.000/mes','left 50%'),
         ('Vóley playa','Arena',[('8 a. m.',1),('9 a. m.',0),('10 a. m.',1),('11 a. m.',1)],'$70.000','right 50%')],
  meter=(76,'% de ocupación hoy ·',42,'alumnos inscritos'),
  ops_t=('Mensualidades, entrenadores y torneos','en orden.'),
  ops=[('Mensualidades',[('Sofía R. · Infantil','Pagado','ok',''),('Mateo G. · Juvenil','Pagado','ok',''),('Valeria P. · Infantil','Vence hoy','warn','Link de pago enviado')]),
       ('Entrenadores',[('Carolina M. · Infantil','Asignada','ok',''),('Andrés V. · Juvenil','Asignado','ok',''),('Nómina del mes','Calculando…','ok','Pagada')]),
       ('inv','Inventario',[('Balones',20,'8 und','Pedido enviado al proveedor'),('Mallas',80,'3 und','')])],
  reporte=['Ocupación de cancha: 76%','Alumnos activos: 42','Mensualidades pendientes: 1, link enviado','Torneo intercolegial: 6 equipos inscritos'],
  final=('Cada punto,','organizado desde antes.')),

'clinica': dict(nombre='Clínica o consultorio', archivo='clinica', palabra='CLÍNICA', obj='diente', acc='#7EE0C3', su='tu clínica',
  foto='1629909613654-28e377c37b09',
  seo='Automatización para clínicas y consultorios', desc='Citas por especialista, recordatorios, insumos, proveedores y pagos de tu clínica, funcionando solos.',
  kicker='Glysf para clínicas y consultorios', hero=('Pacientes que llegan a tiempo,', 'sin llamadas.'),
  bot_t=('El bot agenda', 'mientras tú atiendes.'), bot_sub='Agenda con el especialista correcto, confirma y recuerda la cita un día antes.', bot_nombre='Clínica Dental Sonrisa',
  chat=[('u','Buenas, quiero una cita de valoración'),('b','Con gusto. Hay espacio el jueves 9:00 a. m. con la Dra. Pérez o el viernes 4:00 p. m. ¿Cuál prefieres?'),('u','El jueves'),('b','Listo, jueves 9:00 a. m. ¿Me confirmas tu nombre y documento?'),('pay','Cita confirmada|Jue 9:00'),('b','Te recuerdo un día antes con la dirección. ¡Te esperamos!')],
  cards_t=('Cada especialista,', 'con su agenda llena.'), cards_num='02 · Agenda',
  cards=[('Odontología general','Dra. Pérez',[('8 a. m.',1),('9 a. m.',1),('10 a. m.',1),('11 a. m.',0)],'14 citas','center 30%'),
         ('Ortodoncia','Dr. Gómez',[('8 a. m.',0),('9 a. m.',1),('10 a. m.',1),('11 a. m.',1)],'9 citas','left 60%'),
         ('Higiene oral','Dra. Ruiz',[('8 a. m.',1),('9 a. m.',1),('10 a. m.',0),('11 a. m.',1)],'11 citas','right 40%')],
  meter=(1,' inasistencia esta semana ·',34,'citas atendidas hoy'),
  ops_t=('Insumos, proveedores y pagos','sin papeles.'),
  ops=[('Pagos de hoy',[('María L. · Limpieza','Pagado','ok',''),('Jorge T. · Ortodoncia cuota 4','Pagado','ok',''),('Ana C. · Resina','Pendiente','warn','Recordatorio enviado')]),
       ('Proveedores',[('Pedido #318 · Guantes y resinas','Stock bajo','warn','Orden enviada'),('Laboratorio · Corona','En proceso','ok','Entregada'),('Agenda de mañana','Armando…','ok','Confirmada')]),
       ('inv','Insumos',[('Guantes de nitrilo',18,'20 cajas','Pedido automático al proveedor'),('Anestesia',64,'38 cartuchos','')])],
  reporte=['Citas de hoy: 34 atendidas, 2 reprogramadas','Inasistencias de la semana: 1','Ingresos: $3.120.000','Pedido de guantes en camino','Reseñas nuevas en Google: 3'],
  final=('Más pacientes atendidos,','menos tiempo al teléfono.')),

'gym': dict(nombre='Gimnasio', archivo='gimnasio', palabra='FUERZA', obj='pesa', acc='#FF8A4C', su='tu gimnasio',
  foto='1620188540300-c156a625c6fc',
  seo='Automatización para gimnasios', desc='Mensualidades, renovaciones, instructores, nómina y tienda de suplementos de tu gimnasio, funcionando solos.',
  kicker='Glysf para gimnasios', hero=('Tu gimnasio cobra, agenda y vende', 'sin perseguir a nadie.'),
  bot_t=('El bot vende', 'mientras entrenas.'), bot_sub='Responde precios y horarios, agenda la clase de prueba y le escribe al que no se inscribió.', bot_nombre='Gym Fuerza',
  chat=[('u','¿Cuánto vale la mensualidad?'),('b','Mensual $90.000, trimestral $240.000 y anual $850.000. La primera clase es gratis, ¿la quieres?'),('u','Sí, mañana temprano'),('b','Listo: clase gratis mañana 6:00 a. m. Un entrenador te recibe en la entrada.'),('pay','Prospecto registrado|Asesor avisado'),('b','Te escribo después de la clase para contarte los planes.')],
  cards_t=('Clases e instructores,', 'siempre organizados.'), cards_num='02 · Clases',
  cards=[('Funcional · Kevin P.','Lun, Mié, Vie',[('5 a. m.',1),('6 a. m.',1),('7 p. m.',1),('8 p. m.',0)],'18 inscritos','center 40%'),
         ('Spinning · Natalia C.','Mar y Jue',[('6 a. m.',1),('7 a. m.',0),('6 p. m.',1),('7 p. m.',1)],'22 inscritos','left 50%'),
         ('Pesas · Andrés V.','Lun a Vie',[('5 p. m.',1),('6 p. m.',1),('7 p. m.',1),('8 p. m.',1)],'Piso','right 50%')],
  meter=(312,' socios activos ·',18,'renovaciones esta semana'),
  ops_t=('Mensualidades, nómina y tienda','en orden.'),
  ops=[('Mensualidades',[('Daniela R. · Mensual','Pagado','ok',''),('Felipe A. · Trimestral','Pagado','ok',''),('Carlos M. · Vence hoy','Pendiente','warn','Link de pago enviado')]),
       ('Nómina',[('Kevin P. · 48 clases','Calculando…','ok','Pagado'),('Natalia C. · 24 clases','Calculando…','ok','Pagado'),('Desprendibles','En cola','ok','Enviados por WhatsApp')]),
       ('inv','Tienda de suplementos',[('Proteína 2 lb',20,'24 und','Pedido enviado al proveedor'),('Creatina',60,'18 und','')])],
  reporte=['Socios activos: 312','Mensualidades cobradas hoy: $2.150.000','Por vencer esta semana: 18, recordatorios enviados','Clases de prueba agendadas: 7','Stock bajo: proteína, pedido enviado'],
  final=('Más socios entrenando,','cobros automáticos.')),

'pilates': dict(nombre='Pilates y yoga', archivo='pilates', palabra='PILATES', obj='aro', acc='#F2C6A0', su='tu estudio',
  foto='1717500252709-05a73fc4f1da',
  seo='Automatización para estudios de pilates y yoga', desc='Reservas por clase, paquetes, instructoras, pagos y recordatorios de tu estudio de pilates o yoga.',
  kicker='Glysf para estudios de pilates y yoga', hero=('Cupos llenos', 'y cero cuadernos.'),
  bot_t=('El bot reserva', 'mientras tú das clase.'), bot_sub='Reserva el cupo, descuenta la clase del paquete y avisa cuando hay lista de espera.', bot_nombre='Estudio Pilates',
  chat=[('u','Hola, ¿hay cupo de reformer mañana en la tarde?'),('b','Mañana hay cupo a las 5:30 p. m. y 6:30 p. m. ¿Cuál te sirve?'),('u','5:30 porfa'),('b','Listo, quedaste inscrita. Te quedan 7 clases en tu paquete.'),('pay','Clase descontada|7 restantes'),('b','Te recuerdo una hora antes. ¡Nos vemos!')],
  cards_t=('Cada clase,', 'con su cupo exacto.'), cards_num='02 · Cupos',
  cards=[('Reformer · Sara M.','Lunes',[('7 a. m.',1),('9 a. m.',1),('5:30 p. m.',1),('6:30 p. m.',0)],'5/5 lleno','center 50%'),
         ('Mat y yoga · Daniela F.','Martes',[('7 a. m.',0),('9 a. m.',1),('5:30 p. m.',1),('6:30 p. m.',1)],'4/5','left 50%'),
         ('Reformer · Isabel G.','Sábado',[('8 a. m.',1),('9 a. m.',1),('10 a. m.',1),('11 a. m.',1)],'Lista de espera','right 50%')],
  meter=(91,'% de ocupación ·',4,'clases con lista de espera'),
  ops_t=('Paquetes, pagos e instructoras','en orden.'),
  ops=[('Paquetes y pagos',[('Camila T. · Paquete 12','Pagado','ok',''),('Juliana P. · Paquete 8','Pagado','ok',''),('Mariana S. · Clase suelta','Pendiente','warn','Recordatorio enviado')]),
       ('Instructoras',[('Sara M. · 25 clases','Calculando…','ok','Pagada'),('Daniela F. · 9 clases','Calculando…','ok','Pagada'),('Horarios de la semana','Armando…','ok','Enviados')]),
       ('inv','Paquetes por vencer',[('Esta semana',30,'6 alumnas','Recordatorio de renovación enviado'),('Clases sueltas',60,'12 hoy','')])],
  reporte=['Ocupación de la semana: 91%','Clases con lista de espera: 4','Paquetes por vencer: 6, recordatorio enviado','Ingresos de hoy: $1.085.000'],
  final=('Más alumnas en clase,','menos mensajes por responder.')),

'resto': dict(nombre='Restaurante', archivo='restaurante', palabra='SABOR', obj='campana', acc='#FFB547', su='tu restaurante',
  foto='1760169799369-2b8574466735',
  seo='Automatización para restaurantes', desc='Pedidos por WhatsApp directo a cocina, domicilios, reservas, inventario, proveedores y turnos de tu restaurante.',
  kicker='Glysf para restaurantes', hero=('Pedidos que llegan a cocina', 'sin que nadie los copie.'),
  bot_t=('El bot toma pedidos', 'mientras tú cocinas.'), bot_sub='Envía el menú, toma el pedido completo, lo manda a cocina y avisa cuando sale el domicilio.', bot_nombre='Restaurante La Brasa',
  chat=[('u','Hola, ¿me envías el menú?'),('b','Claro, aquí está el menú de hoy. ¿Domicilio o para recoger?'),('u','Domicilio: 2 hamburguesas y 2 limonadas'),('b','Pedido recibido y enviado a cocina. Total $78.000. Llega en unos 35 minutos.'),('pay','Transferencia recibida|$78.000'),('b','Tu pedido salió. El domiciliario va en camino.')],
  cards_t=('Cada pedido,', 'de la cocina a la mesa.'), cards_num='02 · Cocina',
  cards=[('Pedido #1287 · Domicilio','2 hamburguesas',[('Recibido',1),('Cocina',1),('En camino',1),('Entregado',0)],'$78.000','center 40%'),
         ('Mesa 4 · Reserva','4 personas, 8 p. m.',[('Reservada',1),('Llegaron',1),('Pidieron',0),('Pagó',0)],'Hoy','left 50%'),
         ('Pedido #1288 · Recoger','1 picada',[('Recibido',1),('Cocina',1),('Listo',1),('Entregado',1)],'$62.000','right 50%')],
  meter=(86,' pedidos hoy ·',41,'domicilios'),
  ops_t=('Inventario, proveedores y turnos','en orden.'),
  ops=[('Proveedores',[('Carne · 25 kg','Stock bajo','warn','Pedido enviado'),('Pan · 100 und','Confirmado','ok',''),('Entrega mañana 7 a. m.','Programada','ok','')]),
       ('Turnos y nómina',[('Luis H. · Chef','Asignado','ok',''),('Brayan S. · Mesero','Asignado','ok',''),('Quincena','Calculando…','ok','Pagada')]),
       ('inv','Inventario de cocina',[('Carne de res',22,'30 kg','Pedido automático al proveedor'),('Papa',62,'50 kg','')])],
  reporte=['Pedidos de hoy: 86 (41 domicilios)','Ventas: $3.870.000','Plato más vendido: hamburguesa de la casa','Pedido de carne confirmado para mañana'],
  final=('Más pedidos servidos,','ninguno perdido en el chat.')),

'pelu': dict(nombre='Peluquería y spa', archivo='peluqueria', palabra='ESTILO', obj='tijeras', acc='#E3B5FF', su='tu salón',
  foto='1781450090585-1a511b7066d9',
  seo='Automatización para peluquerías y spas', desc='Citas por estilista, anticipos, recordatorios, comisiones y productos de tu peluquería o spa.',
  kicker='Glysf para peluquerías y spas', hero=('La agenda llena', 'y sin huecos.'),
  bot_t=('El bot agenda', 'mientras tú atiendes.'), bot_sub='Agenda con cada estilista según el servicio, cobra el anticipo y recuerda la cita.', bot_nombre='Salón Bella',
  chat=[('u','Hola, quiero corte y cepillado el sábado'),('b','Con Laura hay espacio el sábado a las 10:00 a. m. o a las 2:00 p. m. ¿Cuál te sirve?'),('u','10 am'),('b','Listo. Te envío el link del anticipo para asegurar tu cita.'),('pay','Anticipo recibido|$30.000'),('b','Cita confirmada. Te recuerdo el viernes.')],
  cards_t=('Cada estilista,', 'con su agenda llena.'), cards_num='02 · Agenda',
  cards=[('Corte y color','Laura',[('9 a. m.',1),('10:30',1),('2 p. m.',1),('4 p. m.',0)],'6 citas','center 50%'),
         ('Uñas','Andrea',[('9 a. m.',1),('10:30',0),('2 p. m.',1),('4 p. m.',1)],'5 citas','left 50%'),
         ('Barbería','Felipe',[('9 a. m.',1),('10:30',1),('2 p. m.',1),('4 p. m.',1)],'7 citas','right 50%')],
  meter=(27,' citas hoy ·',3,'huecos de mañana ofrecidos'),
  ops_t=('Anticipos, comisiones y productos','en orden.'),
  ops=[('Anticipos',[('Valeria G. · Color','Pagado','ok',''),('Natalia R. · Uñas','Pagado','ok',''),('Kevin T. · Corte','Pendiente','warn','Recordatorio enviado')]),
       ('Comisiones',[('Laura · 40%','Calculando…','ok','$1.680.000'),('Andrea · 40%','Calculando…','ok','$840.000'),('Felipe · 40%','Calculando…','ok','$1.040.000')]),
       ('inv','Productos',[('Tinte 7.1',16,'18 und','Pedido enviado al proveedor'),('Esmaltes',68,'60 und','')])],
  reporte=['Citas de hoy: 27','Ingresos: $1.940.000','Huecos libres mañana: 3, ofrecidos a clientas frecuentes','Tinte 7.1 por agotarse, pedido enviado'],
  final=('Más clientes en la silla,','menos mensajes sin responder.')),

'tienda': dict(nombre='Tienda o ferretería', archivo='tienda', palabra='STOCK', obj='caja', acc='#C8F560', su='tu tienda',
  foto='1631856956334-35db20cb7748',
  seo='Automatización para tiendas y ferreterías', desc='Ventas por WhatsApp, inventario, alertas de stock, pedidos a proveedores y cartera de tu tienda o ferretería.',
  kicker='Glysf para tiendas y ferreterías', hero=('Vende por chat', 'y nunca te quedes sin stock.'),
  bot_t=('El bot vende', 'mientras tú despachas.'), bot_sub='Revisa el stock, toma el pedido, envía el total y avisa a bodega.', bot_nombre='Ferretería Central',
  chat=[('u','Buenas, necesito 4 tableros de melamina y 20 bisagras'),('b','Hay disponibilidad de ambos. ¿Recoges o te lo enviamos?'),('u','Envío a la calle 10 # 5-20'),('b','Pedido #1043 registrado. Te envío el total y el link de pago.'),('pay','Pago recibido|$486.000'),('b','Listo, bodega ya está alistando tu pedido.')],
  cards_t=('Cada pedido,', 'de la bodega a la puerta.'), cards_num='02 · Pedidos',
  cards=[('Pedido #1043','Tableros y bisagras',[('Recibido',1),('Pagado',1),('Alistado',1),('Enviado',0)],'$486.000','center 50%'),
         ('Pedido #1044','Pintura blanca',[('Recibido',1),('Pagado',1),('Alistado',1),('Recogido',1)],'$95.000','left 50%'),
         ('Pedido #1045','Tornillería',[('Recibido',1),('Pagado',0),('Alistado',0),('Enviado',0)],'$38.000','right 50%')],
  meter=(38,' pedidos por WhatsApp hoy ·',6,'proveedores conectados'),
  ops_t=('Inventario, proveedores y cartera','en orden.'),
  ops=[('Cartera',[('Muebles El Roble · F-2201','Pagado','ok',''),('Obra Calle 80 · F-2207','Vencida','warn','Recordatorio enviado'),('Carpintería JM · F-2210','Pagado','ok','')]),
       ('Proveedores',[('Orden #540 · Tableros x 50','Stock bajo','warn','Orden enviada'),('Despacho del proveedor','Esperando','ok','En camino'),('Recibido en bodega','—','ok','Stock actualizado')]),
       ('inv','Inventario',[('Tableros de melamina',15,'60 und','Pedido automático al proveedor'),('Bisagras',52,'500 und','')])],
  reporte=['Ventas de hoy: $6.420.000','Pedidos por WhatsApp: 38','Cartera vencida: $5.550.000, recordatorios enviados','Orden de tableros en camino'],
  final=('Más ventas por chat,','cero productos agotados.')),

'fabrica': dict(nombre='Construcción', archivo='constructora', palabra='OBRA', obj='casco', acc='#FFC53D', su='tu empresa',
  foto='1684497404598-6e844dff9cde',
  seo='Automatización para constructoras y fábricas', desc='Venta de proyectos con render interactivo, alquiler de maquinaria, proveedores, materiales, cuadrillas, nómina de obra y cartera de tu constructora.',
  kicker='Glysf para constructoras y fábricas', hero=('Tu obra controlada', 'desde el celular.'),
  bot_t=('El bot cotiza', 'mientras tú construyes.'), bot_sub='Arma la cotización con tus precios, la envía en PDF y le hace seguimiento.', bot_nombre='Constructora Roble',
  chat=[('u','Buenas, ¿cuánto vale un closet de 2 metros en madera?'),('b','Con gusto. ¿Puertas corredizas o batientes, y en qué color?'),('u','Corredizas, color roble'),('b','Te acabo de enviar la cotización en PDF. Si la apruebas, pedimos el material hoy.'),('pay','Cotización enviada|PDF'),('b','Te escribo en 2 días por si tienes dudas.')],
  cards_t=('Cada obra,', 'con su avance a la vista.'), cards_num='02 · Obras',
  cards=[('Obra Calle 80','Estructura · piso 4',[('Cimientos',1),('Estructura',1),('Mampostería',0),('Acabados',0)],'62%','center 40%'),
         ('Casa Los Pinos','Mampostería',[('Cimientos',1),('Estructura',1),('Mampostería',1),('Acabados',0)],'78%','left 50%'),
         ('Bodega Norte','Acabados',[('Cimientos',1),('Estructura',1),('Mampostería',1),('Acabados',1)],'95%','right 50%')],
  meter=(3,' obras activas ·',19,'personas en cuadrillas'),
  ops_t=('Materiales, cuadrillas y nómina','en orden.'),
  ops=[('Alquiler de maquinaria',[('Retroexcavadora · Obra Calle 40','Alquilada','ok','Devuelve el viernes'),('Mezcladora de 1 bulto','Disponible','ok',''),('Andamio x 20 · Torre B','Vence hoy','warn','Cobro enviado al cliente')]),
       ('Proveedores',[('Orden #912 · Cemento x 120','3 cotizaciones','warn','Orden al mejor precio'),('Varilla 1/2" x 80','Confirmado','ok',''),('Entrega en obra','Programada','ok','Recibido')]),
       ('Nómina de obra',[('Cuadrilla A · 8 personas','Calculando…','ok','Pagada'),('Cuadrilla B · 5 personas','Calculando…','ok','Pagada'),('Residente de obra','Calculando…','ok','Pagada')]),
       ('inv','Materiales en bodega',[('Cemento',18,'200 bultos','Pedido automático al proveedor'),('Ladrillo',45,'8.000 und','')])],
  reporte=['Avance Obra Calle 80: 62%','Maquinaria: 1 alquiler vence hoy, cobro enviado','Torre Roble: 3 aptos separados esta semana','Material entregado hoy: cemento y varilla','Gasto vs. presupuesto: 48% usado','Cuenta por cobrar: $45.000.000, recordatorio enviado'],
  final=('Más obra avanzando,','menos hojas sueltas.')),
'muebleria': dict(nombre='Mueblerías', archivo='muebleria', palabra='MUEBLES', obj='caja', acc='#E8B98A', su='tu mueblería',
  foto='1703250151890-9d299b88e886',
  seo='Automatización para mueblerías', desc='Catálogo por WhatsApp, cotizaciones a la medida, pedidos a fábrica, entregas con instalación y cartera de tu mueblería.',
  kicker='Glysf para mueblerías', hero=('Muebles que se venden', 'mientras duermes.'),
  bot_t=('El bot muestra el catálogo', 'y cierra la venta.'), bot_sub='Envía fotos y medidas, cotiza en minutos y agenda la entrega con el cliente.', bot_nombre='Muebles Nogal',
  chat=[('u','Hola, ¿tienen sofás en L grises?'),('b','¡Hola! Sí: el sofá Oslo en L, gris claro, de 2,80 x 1,70 m, a $3.290.000. Te envío fotos y medidas.'),('u','¿Lo pueden entregar esta semana?'),('b','Hay 2 en bodega. Te lo entregamos el viernes con instalación. ¿Te envío el link para separarlo con el 30%?'),('pay','Anticipo recibido|$987.000'),('b','¡Listo! Entrega el viernes entre 9 y 12. Te escribo el día anterior.')],
  cards_t=('Cada pedido,', 'de la fábrica a la sala.'), cards_num='02 · Pedidos',
  cards=[('Pedido #2041 · Sofá Oslo','Entrega el viernes',[('Pagado',1),('Fábrica',1),('Despacho',1),('Instalado',0)],'$3.290.000','center 50%'),
         ('Pedido #2042 · Comedor','A la medida, 6 puestos',[('Pagado',1),('Fábrica',1),('Despacho',0),('Instalado',0)],'$4.150.000','left 50%'),
         ('Pedido #2043 · Cama King','Con base y cabecero',[('Pagado',1),('Fábrica',1),('Despacho',1),('Instalado',1)],'$2.480.000','right 50%')],
  meter=(14,' pedidos activos ·',9,'entregas esta semana'),
  ops_t=('Fábrica, entregas y cartera','en orden.'),
  ops=[('Entregas de hoy',[('Sofá Oslo · Cedritos','En camino','ok','Entregado'),('Comedor Roble · Chía','Programada','ok',''),('Cama King · Suba','Reprogramar','warn','Cliente confirmó el sábado')]),
       ('Cartera',[('Pedido #2038 · Saldo 70%','Pagado','ok',''),('Pedido #2040 · Saldo 70%','Vence hoy','warn','Link de pago enviado'),('Pedido #2036 · Saldo 70%','Pagado','ok','')]),
       ('inv','Inventario en bodega',[('Sofá Oslo gris',20,'2 und','Orden enviada a fábrica'),('Sillas Nórdica',65,'24 und','')])],
  reporte=['Ventas de hoy: $8.420.000','Anticipos recibidos: 3','Entregas: 2 hechas, 1 reprogramada','Saldo por cobrar: $2.900.000, link enviado'],
  final=('Más muebles vendidos,','menos chats sin responder.')),

'admin': dict(nombre='Administración de conjuntos', archivo='administracion', palabra='CONJUNTO', obj='caja', acc='#8EC5FF', su='tu conjunto',
  foto='1657383543368-7d929944be6a',
  seo='Automatización para administradores de conjuntos y edificios', desc='Cuotas de administración, reservas de zonas comunes, PQRS, mantenimiento y comunicados de tu conjunto o edificio, funcionando solos.',
  kicker='Glysf para administradores', hero=('Tu conjunto administrado,', 'sin mensajes a las 11 p. m.'),
  bot_t=('El bot atiende a los residentes', 'mientras tú administras.'), bot_sub='Responde PQRS, reserva zonas comunes, envía el recibo y le recuerda la cuota a cada apartamento.', bot_nombre='Conjunto Altos del Bosque',
  chat=[('u','Hola, quiero reservar el BBQ el sábado'),('b','¡Hola! El BBQ está libre el sábado de 12:00 a 6:00 p. m. ¿Lo reservo a nombre del apto 502 de la torre 2?'),('u','Sí, porfa'),('b','Listo, quedó reservado. El depósito es de $50.000; te envío el link.'),('pay','Depósito recibido|$50.000'),('b','Confirmado. Te recuerdo el sábado y te devolvemos el depósito al revisar la zona.')],
  cards_t=('Zonas comunes,', 'sin cruces ni papeles.'), cards_num='02 · Reservas',
  cards=[('Salón social','Capacidad 40',[('Vie',1),('Sáb',1),('Dom',0),('Lun',0)],'$120.000','center 50%'),
         ('BBQ','Terraza torre 2',[('Vie',0),('Sáb',1),('Dom',1),('Lun',0)],'$50.000','left 50%'),
         ('Cancha múltiple','Por turnos',[('6 p. m.',1),('7 p. m.',1),('8 p. m.',1),('9 p. m.',0)],'Sin costo','right 50%')],
  meter=(87,'% de cuotas al día ·',212,'de 244 apartamentos'),
  ops_t=('Cuotas, PQRS y mantenimiento','en orden.'),
  ops=[('Cuotas de administración',[('Torre 1 · 104','Pagado','ok',''),('Torre 2 · 502','Pagado','ok',''),('Torre 3 · 1103','En mora','warn','Recordatorio y acuerdo enviados')]),
       ('PQRS',[('Filtración baño · T2-704','Asignada','ok','Plomero el jueves'),('Ruido · T1-302','Respondida','ok',''),('Parqueadero ocupado · T3','Abierta','warn','Aviso a vigilancia')]),
       ('Mantenimiento',[('Ascensores · revisión mensual','Programado','ok',''),('Piscina · químicos','Hecho','ok',''),('Planta eléctrica','Vence hoy','warn','Proveedor notificado')])],
  reporte=['Recaudo del mes: 87% (212 de 244)','Reservas de zonas comunes: 6 esta semana','PQRS abiertas: 1, asignada','Mantenimiento: planta eléctrica programada'],
  final=('Un conjunto tranquilo','empieza con respuestas a tiempo.')),

'inmobiliaria': dict(nombre='Inmobiliarias y agentes', archivo='inmobiliaria', palabra='HOGAR', obj='caja', acc='#F2A65A', su='tu inmobiliaria',
  foto='1741156386380-0236c72eb6f9',
  seo='Automatización para inmobiliarias y agentes inmobiliarios', desc='Leads de portales y WhatsApp respondidos al instante, visitas agendadas, seguimiento, contratos, arriendos y cobros de tu inmobiliaria.',
  kicker='Glysf para inmobiliarias', hero=('Más visitas agendadas,', 'menos leads perdidos.'),
  bot_t=('El bot filtra al cliente', 'y agenda la visita.'), bot_sub='Responde cada lead en segundos, pregunta presupuesto y zona, envía opciones y agenda la visita con el asesor.', bot_nombre='Inmobiliaria Cumbre',
  chat=[('u','Hola, vi el apto de Cedritos en Finca Raíz, ¿sigue disponible?'),('b','¡Hola! Sí: 3 habitaciones, 2 baños, 86 m², $2.400.000 de arriendo. ¿Para cuándo lo necesitas?'),('u','Para diciembre, ¿lo puedo ver mañana?'),('b','Claro. Mañana hay visita a las 10:00 a. m. o a las 4:00 p. m. con Laura, tu asesora. ¿Cuál te sirve?'),('u','A las 4'),('b','Listo, quedó agendada. Te envío la ubicación y te recuerdo una hora antes.')],
  cards_t=('Cada inmueble,', 'con sus visitas a la vista.'), cards_num='02 · Inmuebles',
  cards=[('Apto Cedritos · Arriendo','3 hab · 86 m²',[('Lead',1),('Visita',1),('Oferta',0),('Contrato',0)],'$2.400.000','center 50%'),
         ('Casa Chía · Venta','4 hab · 180 m²',[('Lead',1),('Visita',1),('Oferta',1),('Contrato',0)],'$890.000.000','left 50%'),
         ('Apto Chapinero · Venta','2 hab · 64 m²',[('Lead',1),('Visita',1),('Oferta',1),('Contrato',1)],'$420.000.000','right 50%')],
  meter=(36,' leads esta semana ·',14,'visitas agendadas'),
  ops_t=('Leads, contratos y arriendos','en orden.'),
  ops=[('Leads de hoy',[('Finca Raíz · Apto Cedritos','Visita agendada','ok',''),('Instagram · Casa Chía','Calificado','ok',''),('WhatsApp · Local Usaquén','Sin respuesta','warn','Seguimiento enviado')]),
       ('Arriendos',[('Apto 302 · Canon diciembre','Pagado','ok',''),('Casa 14 · Canon diciembre','Pagado','ok',''),('Apto 1101 · Canon diciembre','Vence hoy','warn','Recordatorio enviado')]),
       ('Contratos',[('Promesa · Apto Chapinero','Firmada','ok',''),('Arriendo · Apto Cedritos','En revisión','ok','Enviado a firma'),('Renovación · Local 2','Vence en 30 días','warn','Aviso al propietario')])],
  reporte=['Leads nuevos: 9, todos respondidos','Visitas agendadas mañana: 4','Cánones pendientes: 1, recordatorio enviado','Promesa de compraventa firmada: Apto Chapinero'],
  final=('Cada lead,','respondido antes que la competencia.')),

'contable': dict(nombre='Firmas contables', archivo='contable', palabra='CIERRE', obj='calculadora', acc='#9BE7C4', su='tu firma',
  foto='1772588627474-ae6acc69ac42',
  seo='Automatización para firmas contables', desc='Recepción de soportes por WhatsApp, causación, conciliaciones, recordatorios de impuestos y preparación del cierre para firmas contables.',
  kicker='', hero=('El cierre del mes', 'sin perseguir soportes.'),
  bot_t=('El bot recibe soportes', 'mientras tú concilias.'), bot_sub='Tus clientes envían facturas por WhatsApp; la IA las lee, las clasifica y las deja listas para causar.', bot_nombre='Contadores Asociados',
  chat=[('u','Hola, te envío las facturas de compra de octubre'),('b','Recibidas 12 facturas. Leí NIT, fecha, base e IVA de cada una. Falta la de Ferretería Central, ¿la tienes?'),('u','Ya te la mando'),('b','Listo, completas. Quedaron en la carpeta de octubre y en la hoja de causación.'),('pay','Soportes completos|13/13'),('b','Te recuerdo: la declaración de IVA vence el 15.')],
  cards_t=('Cada cliente,', 'con su cierre al día.'), cards_num='',
  cards=[('Comercial Andina','Cierre de octubre',[('Soportes',1),('Causación',1),('Conciliación',1),('Informe',0)],'92%','center 40%'),
         ('Clínica Sonrisa','Cierre de octubre',[('Soportes',1),('Causación',1),('Conciliación',0),('Informe',0)],'64%','left 50%'),
         ('Gym Fuerza','Cierre de octubre',[('Soportes',1),('Causación',0),('Conciliación',0),('Informe',0)],'31%','right 50%')],
  meter=(48,' clientes activos ·',412,'facturas leídas este mes'),
  ops_t=('Conciliaciones, causaciones y vencimientos','en orden.'),
  ops=[('Conciliación bancaria',[('Bancolombia · octubre','Cruzando…','ok','148 de 150 cruzados'),('Davivienda · octubre','Cruzando…','ok','Conciliado'),('Partidas sin soporte','2','warn','Pedido al cliente')]),
       ('Vencimientos',[('IVA bimestral · 15 nov','Pendiente','warn','Recordatorio enviado'),('Retención en la fuente','Presentada','ok',''),('ICA Bogotá','Preparando','ok','Lista para firmar')]),
       ('inv','Avance del cierre',[('Soportes recibidos',96,'412 de 430','Faltantes pedidos por WhatsApp'),('Causaciones',70,'301 de 430','')])],
  reporte=['Clientes con cierre listo: 31 de 48','Facturas leídas hoy: 64','Partidas por conciliar: 2, pedidas al cliente','Vencimientos de la semana: 5, recordatorios enviados'],
  final=('Más clientes atendidos,','menos soportes perdidos.')),

'abogados': dict(nombre='Firmas de abogados', archivo='abogados', palabra='LEX', obj='balanza', acc='#E8C77A', su='tu firma',
  foto='1752697589029-0fd0ce96a395',
  seo='Automatización para firmas de abogados', desc='Atención de consultas, agendamiento, expedientes, borradores con IA, términos y seguimiento de casos para firmas de abogados.',
  kicker='', hero=('Expedientes en orden', 'y ningún término vencido.'),
  bot_t=('El bot atiende consultas', 'mientras tú litigas.'), bot_sub='Filtra cada consulta, recoge los datos del caso y agenda la cita con el abogado correcto.', bot_nombre='Rojas & Asociados',
  chat=[('u','Buenas, necesito asesoría por un despido sin justa causa'),('b','Con gusto. ¿Cuándo fue el despido y tenías contrato a término fijo o indefinido?'),('u','Hace 2 semanas, indefinido'),('b','Gracias. Te agendo con la Dra. Rojas, laboral: jueves 10:00 a. m. Te pido la carta de despido por aquí.'),('pay','Caso creado|LAB-0231'),('b','Documento recibido y guardado en tu expediente.')],
  cards_t=('Cada caso,', 'con su próximo paso a la vista.'), cards_num='',
  cards=[('LAB-0231 · Laboral','Despido sin justa causa',[('Consulta',1),('Poder',1),('Demanda',0),('Audiencia',0)],'Jue 10 a. m.','center 40%'),
         ('CIV-0118 · Civil','Cobro de pagaré',[('Consulta',1),('Poder',1),('Demanda',1),('Audiencia',0)],'Término: 5 días','left 50%'),
         ('FAM-0092 · Familia','Sucesión',[('Consulta',1),('Poder',1),('Demanda',1),('Audiencia',1)],'Sentencia','right 50%')],
  meter=(37,' casos activos ·',0,'términos vencidos'),
  ops_t=('Términos, borradores y honorarios','bajo control.'),
  ops=[('Términos',[('CIV-0118 · Contestación','5 días','warn','Alerta enviada al abogado'),('LAB-0207 · Recurso','Presentado','ok',''),('Audiencias de la semana','3','ok','En el calendario')]),
       ('Borradores con IA',[('Poder especial · LAB-0231','Generando…','ok','Listo para revisión'),('Derecho de petición','Generando…','ok','Listo para revisión'),('Resumen del expediente','Generando…','ok','Listo')]),
       ('inv','Honorarios',[('Cobrado del mes',72,'$18.400.000',''),('Por cobrar',28,'$7.100.000','Recordatorios enviados')])],
  reporte=['Consultas nuevas hoy: 9 (4 agendadas)','Términos en los próximos 7 días: 6','Borradores listos para revisión: 3','Honorarios por cobrar: $7.100.000, recordatorios enviados'],
  final=('Más casos atendidos,','ningún término olvidado.')),

'logistica': dict(nombre='Logística', archivo='logistica', palabra='RUTA', obj='camion', acc='#7FD4F5', su='tu operación',
  foto='1645736315000-6f788915923b',
  seo='Automatización para empresas de logística', desc='Pedidos, rutas, entregas, novedades y avisos a clientes de tu operación logística, funcionando solos.',
  kicker='', hero=('Cada pedido rastreado,', 'cada cliente avisado.'),
  bot_t=('El bot informa entregas', 'mientras tú despachas.'), bot_sub='Tus clientes preguntan por su pedido y el bot responde con el estado real, sin llamar a nadie.', bot_nombre='Envíos Rápidos',
  chat=[('u','Hola, ¿dónde va mi pedido 8842?'),('b','Tu pedido 8842 salió a las 9:20 a. m. en la ruta Norte. Vas de tercera parada, llega entre 11:00 y 11:30.'),('u','Perfecto, ¿pueden dejarlo en portería?'),('b','Listo, le avisé al conductor: entrega en portería.'),('pay','Entregado|11:14 a. m.'),('b','Tu pedido fue entregado. Aquí está la foto de la entrega.')],
  cards_t=('Cada ruta,', 'en tiempo real.'), cards_num='',
  cards=[('Ruta Norte · Camión 12','14 entregas',[('Cargue',1),('En ruta',1),('Entregas',1),('Cierre',0)],'11 de 14','center 50%'),
         ('Ruta Sur · Camión 07','9 entregas',[('Cargue',1),('En ruta',1),('Entregas',0),('Cierre',0)],'3 de 9','left 50%'),
         ('Ruta Centro · Moto 03','22 entregas',[('Cargue',1),('En ruta',1),('Entregas',1),('Cierre',1)],'22 de 22','right 50%')],
  meter=(94,'% de entregas a tiempo ·',45,'pedidos en ruta'),
  ops_t=('Novedades, flota y cobros','en orden.'),
  ops=[('Novedades',[('8851 · Dirección errada','Novedad','warn','Cliente contactado'),('8860 · Nadie en casa','Novedad','warn','Reprogramado mañana'),('8842 · Entregado','Con foto','ok','')]),
       ('Flota',[('Camión 12 · Revisión','Pendiente','warn','Agendada'),('Camión 07 · SOAT','Vigente','ok',''),('Moto 03 · Combustible','Registrado','ok','')]),
       ('inv','Bodega',[('Pedidos por despachar',30,'18 pedidos','Ruta asignada'),('Capacidad del día',76,'45 de 60','')])],
  reporte=['Entregas hoy: 42 de 45 (94% a tiempo)','Novedades: 3, clientes contactados','Rutas cerradas: 2 de 3','Mañana: 51 pedidos programados'],
  final=('Más entregas a tiempo,','menos llamadas de "¿dónde va mi pedido?".')),

'manufactura': dict(nombre='Manufactura', archivo='manufactura', palabra='TURNO', obj='engranaje', acc='#FFB347', su='tu planta',
  foto='1787422429941-b1966d776195',
  seo='Automatización para manufactura', desc='Reportes de producción, relevos de turno, órdenes, materias primas y mantenimiento de tu planta, funcionando solos.',
  kicker='', hero=('Cada turno reportado', 'sin papeles.'),
  bot_t=('El bot recibe el reporte', 'mientras la línea produce.'), bot_sub='El supervisor reporta por WhatsApp o nota de voz; la IA lo ordena y lo deja en el tablero.', bot_nombre='Planta Industrial',
  chat=[('u','Reporte turno mañana: línea 2 hizo 1.180 unidades, 22 defectuosas, paro de 15 min por cambio de molde'),('b','Registrado. Eficiencia línea 2: 92%. ¿El cambio de molde estaba programado?'),('u','Sí, programado'),('b','Listo. Relevo enviado al supervisor de la tarde con los pendientes.'),('pay','Turno cerrado|1.180 und'),('b','Aviso: la resina PP está por debajo del mínimo.')],
  cards_t=('Cada línea,', 'con su meta a la vista.'), cards_num='',
  cards=[('Línea 1 · Inyección','OP-3021',[('6 a. m.',1),('10 a. m.',1),('2 p. m.',1),('6 p. m.',0)],'1.240 und','center 50%'),
         ('Línea 2 · Ensamble','OP-3022',[('6 a. m.',1),('10 a. m.',1),('2 p. m.',0),('6 p. m.',0)],'1.180 und','left 50%'),
         ('Línea 3 · Empaque','OP-3023',[('6 a. m.',1),('10 a. m.',1),('2 p. m.',1),('6 p. m.',1)],'2.300 und','right 50%')],
  meter=(91,'% de eficiencia ·',3,'órdenes en producción'),
  ops_t=('Relevos, materias primas y mantenimiento','en orden.'),
  ops=[('Relevo de turno',[('Pendiente · Molde línea 2','Abierto','warn','Entregado al turno tarde'),('Calidad · 22 defectuosas','Registrado','ok',''),('Paros del turno','15 min','ok','Con causa')]),
       ('Mantenimiento',[('Inyectora 1 · Preventivo','Jue 6 a. m.','ok','Programado'),('Compresor · Ruido','Reportado','warn','Orden de trabajo creada'),('Banda línea 3','Al día','ok','')]),
       ('inv','Materias primas',[('Resina PP',16,'1.200 kg','Pedido automático al proveedor'),('Cajas de empaque',64,'3.400 und','')])],
  reporte=['Producción de hoy: 4.720 unidades (91% de eficiencia)','Defectuosas: 0,9%','Paros: 2, con causa registrada','Resina PP: pedido enviado al proveedor'],
  final=('Más producción medida,','reportes automáticos.')),

'ecommerce': dict(nombre='eCommerce', archivo='ecommerce', palabra='CARRITO', obj='bolsa', acc='#FF9FD0', su='tu tienda online',
  foto='1781899710894-f9ecfea088f3',
  seo='Automatización para tiendas online (eCommerce)', desc='Catálogo, pedidos, pagos, carritos abandonados, guías de envío y respuestas a clientes de tu tienda online.',
  kicker='', hero=('Vende de día y de noche,', 'con respuestas automáticas.'),
  bot_t=('El bot vende', 'mientras tú empacas.'), bot_sub='Responde por WhatsApp e Instagram, muestra el catálogo, cobra y genera la guía de envío.', bot_nombre='Tienda Nube',
  chat=[('u','Hola, ¿tienen el buzo negro en talla M?'),('b','Sí, quedan 4 en talla M. Precio $89.000 con envío gratis a Bogotá. ¿Te lo separo?'),('u','Sí, de una'),('b','Listo. Te envío el link de pago; apenas pagues genero tu guía.'),('pay','Pago aprobado|$89.000'),('b','Guía 7781 creada. Te aviso cuando la transportadora lo recoja.')],
  cards_t=('Cada pedido,', 'del carrito a la puerta.'), cards_num='',
  cards=[('Pedido #2041','Buzo negro · M',[('Pagado',1),('Empacado',1),('Guía',1),('Entregado',0)],'$89.000','center 50%'),
         ('Carrito abandonado','Tenis blancos · 40',[('Recordatorio',1),('Descuento',1),('Pagado',0),('Enviado',0)],'$159.000','left 50%'),
         ('Pedido #2042','Gorra + medias',[('Pagado',1),('Empacado',1),('Guía',1),('Entregado',1)],'$64.000','right 50%')],
  meter=(63,' pedidos hoy ·',9,'carritos recuperados'),
  ops_t=('Pagos, envíos e inventario','en orden.'),
  ops=[('Pagos',[('#2041 · Buzo negro','Aprobado','ok',''),('#2043 · Chaqueta','Pendiente','warn','Recordatorio enviado'),('#2044 · Jean','Aprobado','ok','')]),
       ('Envíos',[('Guías del día','Generando…','ok','18 creadas'),('Recogida transportadora','3 p. m.','ok','Programada'),('Devoluciones','1','warn','Etiqueta enviada')]),
       ('inv','Inventario',[('Buzo negro · M',12,'4 und','Alerta de reposición enviada'),('Tenis blancos',58,'31 und','')])],
  reporte=['Ventas de hoy: $5.230.000 (63 pedidos)','Carritos recuperados: 9','Guías generadas: 18','Buzo negro M por agotarse, reposición pedida'],
  final=('Más ventas cerradas,','ningún mensaje sin respuesta.')),
'web': dict(nombre='Páginas web', archivo='paginas-web', palabra='WEB', obj='navegador', acc='#8FB3FF', su='tu empresa',
  foto='1680016661694-1cd3faf31c3a',
  seo='Diseño de páginas web con chatbot y automatización', desc='Páginas web a la medida con chatbot, reservas, pedidos y pagos en línea, conectadas a tu CRM y a tus procesos.',
  kicker='', hero=('Tu página web', 'trabaja mientras duermes.'),
  bot_t=('Tu web atiende', 'aunque nadie esté conectado.'), bot_sub='El chatbot de tu página responde, agenda o vende, y cada contacto llega a tu equipo con todos sus datos.', bot_nombre='Tu empresa',
  chat=[('u','Hola, ¿hacen envíos a Medellín?'),('b','¡Sí! Enviamos a todo el país. ¿Qué producto te interesa?'),('u','El plan empresarial'),('b','Te dejo los detalles del plan. ¿Quieres que un asesor te llame hoy?'),('pay','Contacto nuevo|En tu CRM'),('b','Listo, un asesor te contactará esta tarde.')],
  cards_t=('Cada página,', 'hecha a tu medida.'), cards_num='',
  cards=[('Página corporativa','Tu empresa en línea',[('Diseño',1),('Contenido',1),('Desarrollo',1),('En línea',1)],'Con chatbot','center 40%'),
         ('Reservas y citas','Agenda en tu web',[('Diseño',1),('Calendario',1),('Pagos',1),('En línea',0)],'Con anticipos','left 50%'),
         ('Tienda online','Catálogo y pagos',[('Diseño',1),('Catálogo',1),('Pagos',0),('En línea',0)],'Con envíos','right 50%')],
  meter=(100,'% adaptada al celular ·',24,'horas al día atendiendo'),
  ops_t=('Formularios, pagos y contactos','conectados a tus procesos.'),
  ops=[('Contactos de hoy',[('Formulario · Plan empresarial','Nuevo','warn','Asignado a ventas'),('Chatbot · Envíos','Respondido','ok',''),('WhatsApp · Cotización','Enviada','ok','')]),
       ('Lo que incluye',[('Dominio y certificado de seguridad','Configurando…','ok','Listo'),('Hosting a tu nombre','Configurando…','ok','Listo'),('Posicionamiento básico en Google','Configurando…','ok','Listo')]),
       ('inv','Visitas del mes',[('Desde Google',62,'1.840 visitas',''),('Desde redes sociales',38,'1.120 visitas','Reporte enviado')])],
  reporte=['Visitas de hoy: 214','Contactos nuevos: 9, todos en tu CRM','Reservas o pedidos en línea: 6','Página más vista: Servicios'],
  final=('Una página que vende,','no solo una que se ve bien.')),
}

E = lambda s: html.escape(str(s), quote=True)
import unicodedata
dominio = lambda t: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', t.lower().replace('&', 'y')).encode('ascii', 'ignore').decode())

# Botón principal de la página web de ejemplo, según el negocio
WEB_CTA = {'web':('Tu empresa en línea','Contáctanos'),'muebleria':('Muebles para toda la vida','Ver catálogo'),'admin':('Tu conjunto, en orden','Portal de residentes'),'inmobiliaria':('Encuentra tu próximo hogar','Ver inmuebles'),'futbol':('Arma tu partido','Reservar cancha'),'voley':('Juega, entrena, compite','Reservar cancha'),'padel':('Reserva tu cancha','Reservar cancha'),'clinica':('Tu sonrisa, en buenas manos','Agendar cita'),'gym':('Entrena sin excusas','Clase gratis'),
 'pilates':('Muévete con calma','Reservar clase'),'resto':('Del fuego a tu mesa','Pedir a domicilio'),'pelu':('Tu mejor versión','Agendar cita'),
 'tienda':('Todo para tu obra','Ver catálogo'),'fabrica':('Construimos lo que imaginas','Cotizar obra'),'contable':('Tus cuentas, claras','Enviar soportes'),
 'abogados':('Defendemos lo tuyo','Agendar consulta'),'logistica':('Tu carga, a tiempo','Rastrear pedido'),'manufactura':('Producción a tu medida','Solicitar cotización'),
 'ecommerce':('Nueva colección','Comprar ahora')}


def contacto(n, extra=''):
    wa_txt = f"Hola, vi el ejemplo de {n['nombre'].lower()} en glysf.com y quiero cotizar."
    return f'''<div class="contact-row{extra}">
<a class="pill-btn wa big" data-wa="{E(wa_txt)}" href="https://wa.me/573103102908?text={E(wa_txt)}" target="_blank" rel="noopener">{WA_SVG}Escríbenos por WhatsApp</a>
<a class="pill-btn ghost big" href="mailto:grupolysf@gmail.com?subject={E('Cotización Glysf – ' + n['nombre'])}">{MAIL_SVG}Escríbenos un correo</a>
</div>'''

# ---------- Panel de muestra (mismo estilo que el panel de Cuore) ----------
_IC = {
 'inicio':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'agenda':'<rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4M7.5 13.5h3M7.5 17h6"/>',
 'dinero':'<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>',
 'personas':'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16 4.8a3.3 3.3 0 0 1 0 6.4M18.5 14.8c1.7.8 2.7 2.5 3 5.2"/>',
 'caja':'<path d="M12 2.8 20.5 7.5v9L12 21.2 3.5 16.5v-9z"/><path d="M3.8 7.6 12 12.2l8.2-4.6M12 12.2v8.8"/>',
 'camion':'<path d="M2.5 6.5h11v10h-11zM13.5 10h4l3 3.2v3.3h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
 'reloj':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 'lista':'<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3.5 6 1.2 1.2L7 5M3.5 12l1.2 1.2L7 11M3.5 18l1.2 1.2L7 17"/>',
 'reporte':'<path d="M6 2.5h8l4.5 4.5v14.5H6z"/><path d="M14 2.5V7h4.5M9 12h6M9 15.5h6M9 19h3"/>',
 'chat':'<path d="M20.5 12a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.1-4.2A8.5 8.5 0 1 1 20.5 12z"/><path d="M8.5 10.5h7M8.5 14h4.5"/>',
 'mas':'<path d="M12 5v14M5 12h14"/>',
}
def ic(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_IC[k]}</svg>'
def ic_op(t):
    t = t.lower()
    for ws, k in ((('pago','cobro','mensualidad','anticipo','cartera','honorario','paquete','comisi'),'dinero'),
                  (('profesor','instructor','nómina','turno','cuadrilla','flota','relevo','equipo'),'personas'),
                  (('inventario','insumo','tienda','producto','materia','material','bodega','suplement'),'caja'),
                  (('proveedor','envío','envio','novedad'),'camion'),
                  (('vencimiento','término','termino','mantenimiento'),'reloj')):
        if any(w in t for w in ws): return k
    return 'lista'

def panel(k, n):
    m = n['meter']
    agenda = n['cards_num'].split('· ')[-1] if n['cards_num'] else 'Hoy'
    def lab(x):
        x = x.strip().rstrip('·').strip()
        return ('%', x[1:].strip()) if x.startswith('%') else ('', x)
    u1, l1 = lab(m[1]); u2, l2 = lab(m[3])
    sigla = ''.join(w[0] for w in re.findall(r'[A-ZÁÉÍÓÚÑ]\S*', n['bot_nombre']))[:3] or n['bot_nombre'][:2]
    mods = [('ag', agenda, 'agenda', f"{n['cards_t'][0]} {n['cards_t'][1]}", f'{m[0]}{u1} {l1}', f'{m[2]} {l2}', '')]
    vistas = []
    cards = []
    for tag, tit, slots, precio, img in n['cards']:
        sl = ''.join(f'<span class="{"on" if ok else ""}">{E(h)}</span>' for h, ok in slots)
        ocup = sum(1 for _, ok in slots if ok)
        cards.append(f'<div class="cp-slotcard"><p class="cp-sc-h"><b>{ocup}/{len(slots)}</b><span>{E(tag)}</span></p><p class="cp-sc-t">{E(tit)}</p><div class="cp-slots">{sl}</div><p class="cp-sc-f">{E(precio)}</p></div>')
    vistas.append(('ag', agenda,
        f'<div class="cp-kpis rev"><div><b class="acc">{m[0]}{u1}</b><small>{E(l1)}</small></div><div><b>{m[2]}{u2}</b><small>{E(l2)}</small></div><div><b>24/7</b><small>atención por WhatsApp</small></div></div>'
        f'<div class="cp-slotgrid">{"".join(cards)}</div>'))
    for j, o in enumerate(n['ops']):
        vid = f'o{j}'
        if o[0] == 'inv':
            tit, items = o[1], o[2]
            bajos = sum(1 for it in items if it[1] <= 25)
            mods.append((vid, tit, ic_op(tit), 'Existencias, avance y alertas', f'{len(items)} en seguimiento', f'{bajos} por reponer' if bajos else 'Todo en orden', 'warn' if bajos else ''))
            filas = ''.join(
                f'<tr><td><b>{E(a)}</b></td><td class="cp-bar-td"><i class="cp-bar"><i style="width:{pct}%"' + (' class="low"' if pct <= 25 else '') + f'></i></i></td><td class="cp-num">{E(tx)}</td>'
                f'<td><span class="cp-pill {"warn" if pct <= 25 else "ok"}">{E(sw) if sw else ("Por reponer" if pct <= 25 else "En orden")}</span></td></tr>'
                for a, pct, tx, sw in items)
            body = (f'<div class="cp-kpis"><div><small>En seguimiento</small><b>{len(items)}</b></div><div><small>Alertas</small><b class="{"warn" if bajos else "ok"}">{bajos}</b></div><div><small>Pedidos automáticos</small><b class="ok">Activos</b></div></div>'
                    f'<div class="cp-table"><table><thead><tr><th>Elemento</th><th>Nivel</th><th class="cp-num">Cantidad</th><th>Estado</th></tr></thead><tbody>{filas}</tbody></table></div>')
        else:
            tit, rows = o
            okn = sum(1 for r in rows if r[2] == 'ok'); wn = len(rows) - okn
            mods.append((vid, tit, ic_op(tit), 'Se registra y se avisa solo', f'{okn} de {len(rows)} al día', (f'{wn} pendiente' + ('s' if wn > 1 else '') + ', aviso enviado') if wn else 'Todo al día', 'warn' if wn else ''))
            filas = ''.join(f'<tr><td><b>{E(a)}</b></td><td><span class="cp-pill {cl}">{E(st)}</span></td><td class="cp-muted">{E(sw) if sw else "—"}</td></tr>' for a, st, cl, sw in rows)
            body = (f'<div class="cp-kpis"><div><small>Registros de hoy</small><b>{len(rows)}</b></div><div><small>Al día</small><b class="ok">{okn}</b></div><div><small>Pendientes</small><b class="{"warn" if wn else "ok"}">{wn}</b></div></div>'
                    f'<div class="cp-table"><table><thead><tr><th>Detalle</th><th>Estado</th><th>Lo que hizo el asistente</th></tr></thead><tbody>{filas}</tbody></table></div>')
        vistas.append((vid, tit, body))
    rep = ''.join(f'<li>{E(l)}</li>' for l in n['reporte'])
    mods.append(('rp', 'Reportes', 'reporte', 'Resumen automático del día', f"{len(n['reporte'])} datos clave", 'Cada noche por WhatsApp', ''))
    vistas.append(('rp', 'Reportes', f'<div class="cp-report"><div class="cp-msg"><p class="cp-msg-h"><b>Glysf · Asistente</b><small>Hoy, 10:00 p. m.</small></p><ul>{rep}</ul></div><p class="cp-muted">El asistente lee la agenda, los pagos y el inventario y te envía este resumen cada noche, sin que nadie lo arme.</p></div>'))
    nav = ''.join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == "in" else "false"}">{ic(i)}<span>{E(t)}</span></button>'
                  for v, t, i in [('in', 'Inicio', 'inicio')] + [(md[0], md[1], md[2]) for md in mods])
    tiles = ''.join(f'<button type="button" class="cp-tile" data-v="{v}" data-at="{.08 + i * .06:.2f}"><span class="cp-ic">{ic(icn)}</span><span class="cp-tt">{E(t)}</span><span class="cp-td">{E(d)}</span><span class="cp-tv">{E(val)}</span><span class="cp-ts {cls}">{E(det)}</span></button>'
                    for i, (v, t, icn, d, val, det, cls) in enumerate(mods))
    wa = f'Hola, vi el panel de ejemplo de {n["nombre"].lower()} en glysf.com y quiero cotizar uno para mi negocio.'
    tiles += (f'<a class="cp-tile hl" data-at="{.08 + len(mods) * .06:.2f}" href="https://wa.me/573103102908" data-wa="{E(wa)}" target="_blank" rel="noopener">'
              f'<span class="cp-ic">{ic("chat")}</span><span class="cp-tt">Asistente</span><span class="cp-td">Atiende WhatsApp y llena este panel</span><span class="cp-tv">En línea 24/7</span></a>')
    hoy = ''.join(f'<li>{E(l)}</li>' for l in n['reporte'][:3])
    inicio = (f'<div class="cp-greet"><p class="cp-g1">Buenas tardes</p><p class="cp-muted">¿Qué quieres revisar hoy?</p></div><div class="cp-tiles">{tiles}</div>'
              f'<div class="cp-today" data-at=".6"><p class="cp-today-h"><b>Hoy en {E(n["su"])}</b><button type="button" data-v="rp">Ver reporte</button></p><ul>{hoy}</ul></div>')
    views = f'<div class="cp-view" data-view="in" data-title="Inicio">{inicio}</div>' + ''.join(f'<div class="cp-view" data-view="{v}" data-title="{E(t)}" hidden>{b}</div>' for v, t, b in vistas)
    return (f'<div class="cp" role="region" aria-label="Panel de ejemplo de {E(n["bot_nombre"])}">'
            f'<aside class="cp-side"><div class="cp-logo"><span>{E(sigla)}</span></div><nav class="cp-nav" aria-label="Secciones del panel de ejemplo">{nav}</nav>'
            f'<p class="cp-user"><span>{E(n["bot_nombre"])}</span><small>Datos de ejemplo</small></p></aside>'
            f'<div class="cp-main"><div class="cp-top"><div><p class="cp-h" aria-live="polite">Inicio</p><p class="cp-muted">Hoy · actualizado hace 1 min</p></div>'
            f'<span class="cp-btn">{ic("mas")}Registrar</span><i class="cp-dot" title="En línea"></i></div>{views}</div></div>')

# ---------- Construcción: render interactivo del proyecto (elige el apto y míralo por dentro) ----------
PJ_FOTOS = [('Sala', '1751945965597-71171ec7a458'), ('Cocina', '1737898415581-7dea57a1905b'), ('Habitación', '1784653548504-c0928cd4737e')]
PJ_PLANOS = {
 'A': [('Sala-comedor',0,0,130,100),('Cocina',130,0,60,55),('Baño',190,0,50,55),('Hab. 3',130,55,110,45),('Balcón',0,100,50,70),('Hab. principal',50,100,110,70),('Hab. 2',160,100,80,70)],
 'B': [('Sala-comedor',0,0,140,100),('Cocina',140,0,100,50),('Baño',140,50,100,50),('Balcón',0,100,50,70),('Hab. principal',50,100,110,70),('Hab. 2',160,100,80,70)],
}
def _plano(t):
    r = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/><text x="{x + w / 2}" y="{y + h / 2 + 4}">{E(n)}</text>' for n, x, y, w, h in PJ_PLANOS[t])
    return f'<svg class="pj-plan" data-plan="{t}" viewBox="-6 -6 252 182" role="img" aria-label="Plano del apartamento tipo {t}"{"" if t == "A" else " hidden"}>{r}</svg>'

def proyecto(n):
    FOTO_TORRE = '1744983672789-86703806e626'
    PISOS = 8
    # Franjas medidas sobre la foto (coordenadas del viewBox 1200x1500)
    FRANJA_Y = {8: (399, 501), 7: (501, 603), 6: (603, 705), 5: (705, 807), 4: (807, 909), 3: (909, 1011), 2: (1011, 1113)}
    FRANJA_X = [(0, 396), (396, 703), (703, 1009), (1009, 1200)]
    hot = []
    estados = 'dvdsddvdvdddsdvddsdvdddvsddvdsdddvdsd'
    pisos_html, aptos, i = [], [], 0
    for piso in range(PISOS, 1, -1):
        chips = []
        for u in range(1, 5):
            t = 'A' if u in (1, 4) else 'B'
            est = {'d': 'disponible', 'v': 'vendido', 's': 'separado'}[estados[(piso * 4 + u) % len(estados)]]
            num = piso * 100 + u
            area, hab, ban = (84, 3, 2) if t == 'A' else (62, 2, 2)
            precio = (420 + piso * 6) if t == 'A' else (310 + piso * 4.5)
            precio = f"${int(precio * 1_000_000):,}".replace(',', '.')
            vista = 'Esquina · vista a los cerros' if u == 4 else ('Esquina · vista al parque' if u == 1 else ('Vista al parque' if u == 2 else 'Vista a los cerros'))
            aptos.append((num, est))
            (y0, y1), (x0, x1) = FRANJA_Y[piso], FRANJA_X[u - 1]
            hot.append(f'<rect class="hs {est}" x="{x0 + 6}" y="{y0 + 4}" width="{x1 - x0 - 12}" height="{y1 - y0 - 8}" rx="10" data-apto="{num}" data-piso="{piso}" role="button" tabindex="0" aria-label="Apto {num}, piso {piso}, {est}"><title>Apto {num} · {est}</title></rect>')
            chips.append(f'<button type="button" class="apt {est}" aria-label="Apto {num}, {est}" data-apto="{num}" data-piso="{piso}" data-tipo="{t}" data-area="{area}" data-hab="{hab}" data-banos="{ban}" data-precio="{precio}" data-estado="{est}" data-vista="{vista}"><b>{num}</b><small>{area} m²</small></button>')
        libres = sum(1 for c in chips if 'apt disponible' in c)
        pisos_html.append((piso, libres, ''.join(chips)))
    cuenta = {e: sum(1 for _, x in aptos if x == e) for e in ('disponible', 'separado', 'vendido')}
    torre = ''.join(f'<button type="button" class="pj-floor" data-floor="{p}" aria-pressed="false"><span>Piso {p}</span><small>{l} libre{"s" if l != 1 else ""}</small></button>' for p, l, _ in pisos_html)
    filas = ''.join(f'<div class="pj-units" data-units="{p}" hidden>{c}</div>' for p, _, c in pisos_html)
    thumbs = ''.join(f'<button type="button" data-img="{pid}"' + (' aria-pressed="true"' if j == 0 else ' aria-pressed="false"') + f'>{E(nm)}</button>' for j, (nm, pid) in enumerate(PJ_FOTOS))
    guia = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="1500"/><text x="{x + 6}" y="40">{x}</text>' for x in range(100, 1200, 100)) + ''.join(f'<line x1="0" y1="{y}" x2="1200" y2="{y}"/><text x="8" y="{y - 8}">{y}</text>' for y in range(100, 1500, 100))
    wa = 'Hola, vi el render interactivo de proyectos en glysf.com y quiero uno para mi constructora.'
    return f'''<section class="s-proyecto" aria-labelledby="t-pj">
<div class="pj-wrap">
<div class="copy center">
<h2 id="t-pj" class="h2">Vende tu proyecto <em>antes de terminarlo.</em></h2>
<p class="sub">Tus clientes pasan el dedo por la fachada, eligen su apartamento, ven el plano y cómo es por dentro, y el bot les ayuda a separarlo.</p>
</div>
<div class="pj">
<div class="pj-stage">
<svg class="pj-shot" viewBox="0 0 1200 1500" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Fotografía de la Torre Roble"><image href="https://images.unsplash.com/photo-{FOTO_TORRE}?auto=format&amp;fit=crop&amp;w=1200&amp;h=1500&amp;q=75" width="1200" height="1500" preserveAspectRatio="xMidYMid slice"/><g class="pj-hot">{"".join(hot)}</g><g class="pj-guia" aria-hidden="true">{guia}</g></svg>
<div class="pj-shade"></div>
<div class="pj-top"><b>Torre Roble</b><span>Chapinero Alto · Entrega 2028</span></div>
<div class="pj-bottom">
<p class="pj-bl">Apartamentos del <span data-f="pisolbl">piso 8</span></p>
{filas}
<ul class="pj-legend"><li><button type="button" class="pj-toggle" aria-pressed="false">Ver disponibilidad</button></li><li class="disponible">{cuenta['disponible']} disponibles</li><li class="separado">{cuenta['separado']} separados</li><li class="vendido">{cuenta['vendido']} vendidos</li></ul>
</div>
</div>
<div class="pj-card" aria-live="polite">
<h3 class="pj-t">Apto <span data-f="apto">704</span></h3>
<p class="pj-sub">Torre Roble · Piso <span data-f="piso">7</span> · <span data-f="vista"></span></p>
<p><span class="pj-pill" data-f="estado">Disponible</span></p>
<dl class="pj-dl"><div><dt>Área</dt><dd><span data-f="area">84</span> m²</dd></div><div><dt>Habitaciones</dt><dd data-f="hab">3</dd></div><div><dt>Baños</dt><dd data-f="banos">2</dd></div><div><dt>Precio</dt><dd data-f="precio"></dd></div></dl>
<div class="pj-tabs" role="tablist" aria-label="Ver el apartamento"><button type="button" role="tab" aria-selected="false" data-pt="plano">Plano</button><button type="button" role="tab" aria-selected="true" data-pt="interior">Por dentro</button></div>
<div class="pj-view" data-pv="plano" hidden>{_plano('A')}{_plano('B')}</div>
<div class="pj-view" data-pv="interior"><div class="pj-photo" role="img" aria-label="Interior de ejemplo"></div><div class="pj-thumbs">{thumbs}</div></div>
<button type="button" class="pj-cta">Separar este apto</button>
<p class="pj-note" hidden>En tu proyecto real, aquí el bot de WhatsApp toma los datos del cliente, envía el link de la separación y te avisa.</p>
<a class="pj-own" href="https://wa.me/573103102908" data-wa="{E(wa)}" target="_blank" rel="noopener">Quiero esto para mi proyecto</a>
</div>
</div>
</div>
</section>

'''

def pagina(k, n):
    at = lambda i, base, step: f'{base + i * step:.2f}'
    foto = n['foto']; foto2 = n.get('foto2', foto); foto3 = n.get('foto3', foto)
    msgs = []
    for i, (w, t) in enumerate(n['chat']):
        a = at(i, .12, .14)
        if w == 'pay':
            x, y = t.split('|'); msgs.append(f'<p class="m pay" data-at="{a}"><span>{E(x)}</span><strong>{E(y)}</strong></p>')
        else:
            msgs.append(f'<p class="m {w}" data-at="{a}">{E(t)}</p>')
    cards = []
    for i, (tag, tit, slots, precio, img) in enumerate(n['cards']):
        if re.match(r'^\d{10,}-', img): fondo = f'data-src="{img}"'
        else: fondo = f'data-src="{foto}" style="background-position:{img}"'
        sl = ''.join(f'<span data-at="{.2 + i * .06 + j * .12:.2f}">{E(h)}</span>' if ok else f'<span>{E(h)}</span>' for j, (h, ok) in enumerate(slots))
        cards.append(f'''<article class="court" data-at="{.05 + i * .07:.2f}">
<div class="c-img" {fondo}></div>
<div class="c-body"><p class="c-tag">{E(tag)}</p><h3>{E(tit)}</h3>
<div class="slots">{sl}</div>
<div class="c-foot"><b>{E(precio)}</b><span class="tgl" data-at="{.6 + i * .06:.2f}"></span></div></div>
</article>''')
    ops = []; t0 = .08
    for c in n['ops']:
        if c[0] == 'inv':
            filas = ''.join(f'<div class="inv"><span>{E(a)}</span><i class="bar"><i data-fill="{p}" data-at="{t0 + .08 + j * .04:.2f}"></i></i><small' + (f' data-swap="{t0 + .2:.2f}" data-to="{E(sw)}"' if sw else '') + f'>{E(tx)}</small></div>' for j, (a, p, tx, sw) in enumerate(c[2]))
            ops.append(f'<div class="g-card" data-at="{t0:.2f}"><p class="g-t">{E(c[1])}</p>{filas}</div>')
        else:
            filas = ''.join(f'<li data-at="{t0 + .06 * (j + 1):.2f}"><span>{E(a)}</span><b class="{cl}"' + (f' data-swap="{t0 + .3:.2f}" data-to="{E(sw)}"' if sw else '') + f'>{E(st)}</b></li>' for j, (a, st, cl, sw) in enumerate(c[1]))
            ops.append(f'<div class="g-card" data-at="{t0:.2f}"><p class="g-t">{E(c[0])}</p><ul class="rows">{filas}</ul></div>')
        t0 += .22
    rep = ''.join(f'<li data-at="{.15 + i * .15:.2f}">{E(l)}</li>' for i, l in enumerate(n['reporte']))
    m = n['meter']
    agenda = n['cards_num'].split('· ')[-1] if n['cards_num'] else 'Hoy'
    def kpi(v, lab, at):
        lab = lab.strip().rstrip('·').strip(); u = ''
        if lab.startswith('%'): u, lab = '%', lab[1:].strip()
        return f'<div class="kpi" data-at="{at}"><b><span data-count="{v}">0</span>{u}</b><small>{E(lab)}</small></div>'
    kpis = kpi(m[0], m[1], '.05') + kpi(m[2], m[3], '.12') + '<div class="kpi" data-at=".19"><b>24/7</b><small>atención por WhatsApp</small></div>'
    side = ''.join(f'<span' + (' class="cur"' if i == 0 else '') + f'>{E(t)}</span>' for i, t in enumerate(['Resumen', agenda] + [o[1] if o[0] == 'inv' else o[0] for o in n['ops']] + ['Reportes']))
    tabs = ''.join(f'<a href="/{v["archivo"]}.html"' + (' aria-current="page"' if kk == k else '') + f'>{E(v["nombre"])}</a>' for kk, v in NEGOCIOS.items())
    obj_cls = 'ball obj'
    return f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(n['seo'])} · Glysf</title>
<meta name="description" content="{E(n['desc'])}">
<link rel="canonical" href="https://glysf.com/{n['archivo']}.html">
<meta property="og:title" content="{E(n['seo'])} · Glysf">
<meta property="og:description" content="{E(n['desc'])}">
<meta property="og:image" content="https://glysf.com/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&amp;family=Geist:wght@400;500;600&amp;family=Geist+Mono:wght@500&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&amp;text=lysf&amp;display=swap">
<link rel="stylesheet" href="/negocio.css?v=12">
<script src="/negocio.js?v=12" defer></script>
<script src="/site.js?v=3" defer></script>
</head>
<body style="--acc:{n['acc']}">
<!-- Página generada por herramientas/generar_negocios.py: edita allá, no aquí. -->
<svg width="0" height="0" class="sr" aria-hidden="true"><symbol id="g" viewBox="164 120 234 380"><circle cx="280" cy="262" r="92" fill="none" stroke="currentColor" stroke-width="44"/><path d="M372 168 V 372 Q372 462 280 462 H 236" fill="none" stroke="currentColor" stroke-width="44" stroke-linecap="round"/><circle cx="372" cy="150" r="22" fill="currentColor"/><circle cx="214" cy="462" r="22" fill="currentColor"/></symbol></svg>

<header class="topbar">
<a href="/" class="wordmark" aria-label="Glysf, inicio"><svg aria-hidden="true"><use href="#g"/></svg><span aria-hidden="true">lysf</span></a>
<nav aria-label="Principal">
<a href="/#negocios" class="navlink">Otros negocios</a>
<a href="https://wa.me/573103102908" data-wa="Hola, quiero cotizar automatizaciones para {E(n['su'])} ({E(n['nombre'].lower())})." target="_blank" rel="noopener" class="pill-btn">Cotizar por WhatsApp</a>
</nav>
</header>
<nav class="biztabs" aria-label="Tipos de negocio">{tabs}</nav>

<main>
<section class="scene s-hero" data-scene aria-labelledby="t-hero">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto}"></div><div class="veil"></div></div>
<h1 id="t-hero" class="giant" aria-label="{E(n['nombre'])}">{E(n['palabra'])}</h1>
<p class="hero-line"><em>{E(n['hero'][0])}</em> {E(n['hero'][1])}</p>
<p class="scroll-hint" aria-hidden="true">Desliza</p>
</div>
</section>

<section class="scene s-bot" data-scene aria-labelledby="t-bot">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto2}" style="background-position:30% 50%"></div><div class="veil"></div></div>
<div class="split">
<div class="copy">
<h2 id="t-bot" class="h2">{E(n['bot_t'][0])} <em>{E(n['bot_t'][1])}</em></h2>
<p class="sub">{E(n['bot_sub'])}</p>
</div>
<div class="phone" role="img" aria-label="Ejemplo de conversación por WhatsApp con el asistente de {E(n['bot_nombre'])}.">
<div class="ph-head"><span class="ph-av"><svg aria-hidden="true"><use href="#g"/></svg></span><span><b>{E(n['bot_nombre'])}</b><small>en línea · WhatsApp</small></span></div>
<div class="msgs">
{chr(10).join(msgs)}
</div>
</div>
</div>
</div>
</section>

<section class="scene s-panel flow" data-scene aria-labelledby="t-panel">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto3}" style="background-position:70% 50%"></div><div class="veil strong"></div></div>
<div class="panel-wrap">
<div class="copy center">
<h2 id="t-panel" class="h2">{E(n['cards_t'][0])} <em>{E(n['cards_t'][1])}</em></h2>
<p class="sub">{E(n['ops_t'][0])} {E(n['ops_t'][1])} Todo {E(n['su'])} en un panel que se actualiza solo. Toca cada sección para explorarlo.</p>
</div>
{panel(k, n)}
</div>
</div>
</section>

{proyecto(n) if k == 'fabrica' else ''}<section class="scene s-web flow" data-scene aria-labelledby="t-web">
<div class="sticky">
<div class="bg dark-solid"></div>
<div class="web-wrap">
<div class="copy">
<h2 id="t-web" class="h2">¿Necesitas página web? <em>También la creamos.</em></h2>
<ul class="web-list">
<li data-at=".2">Diseño a la medida de {E(n['su'])}</li>
<li data-at=".3">Se ve perfecta en el celular</li>
<li data-at=".4">Tu chatbot y el botón de WhatsApp integrados</li>
<li data-at=".5">Reservas, pedidos o pagos en línea</li>
<li data-at=".6">Dominio, hosting y certificado de seguridad</li>
</ul>
</div>
<div class="browser" role="img" aria-label="Ejemplo de página web para {E(n['bot_nombre'])} con botón de {E(WEB_CTA[k][1].lower())} y chat integrado.">
<div class="br-bar"><i></i><i></i><i></i><span>{dominio(n['bot_nombre'])}.com</span></div>
<div class="br-page">
<div class="br-hero" data-src="{foto}">
<div class="br-nav"><b>{E(n['bot_nombre'])}</b><span>Inicio</span><span>Servicios</span><span>Contacto</span></div>
<div class="br-copy"><p class="br-h" data-at=".15">{E(WEB_CTA[k][0])}</p><span class="br-btn" data-at=".3">{E(WEB_CTA[k][1])}</span></div>
</div>
<div class="br-row"><span data-at=".4"></span><span data-at=".48"></span><span data-at=".56"></span></div>
<div class="br-chat" data-at=".65"><b>Asistente</b><p>¡Hola! ¿En qué te ayudo?</p></div>
</div>
</div>
</div>
</div>
</section>

<section class="final" aria-labelledby="t-final">
<div class="bg"><div class="photo still" data-src="{foto}"></div><div class="veil strong"></div></div>
<div class="final-in">
<h2 id="t-final" class="giant-2"><em>{E(n['final'][0])}</em> {E(n['final'][1])}</h2>
<p class="sub">Guíate por este ejemplo: dinos qué parte quieres para {E(n['su'])} y te enviamos la cotización.</p>
{contacto(n)}
<p class="note">Datos de ejemplo. Fotos: <a href="https://unsplash.com" rel="noopener">Unsplash</a>.</p>
</div>
</section>
</main>

<footer class="foot">
<a href="/" class="wordmark small" aria-label="Glysf, inicio"><svg aria-hidden="true"><use href="#g"/></svg><span aria-hidden="true">lysf</span></a>
<a href="mailto:grupolysf@gmail.com">grupolysf@gmail.com</a>
<a href="/privacidad.html">Política de tratamiento de datos</a>
<span>© 2026 Glysf, Colombia</span>
</footer>
<a id="waBtn" class="wa-float" href="https://wa.me/573103102908" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{WA_SVG}</a>
</body>
</html>
'''

if __name__ == '__main__':
    for k, n in NEGOCIOS.items():
        out = pagina(k, n)
        if k == 'web':  # la página de páginas web no repite '¿Necesitas página web?'
            out = re.sub(r'\n<section class="scene s-web flow".*?</section>\n', '\n', out, flags=re.S)
        (RAIZ / f"{n['archivo']}.html").write_text(out, encoding='utf-8')
        print('ok', n['archivo'] + '.html')
