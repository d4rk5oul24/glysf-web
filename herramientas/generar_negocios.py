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

# ---------- Contenido por negocio ----------
# chat: (quién, texto) con quién = u (cliente), b (bot) o pay (aviso de pago "Texto|Valor")
# cards: (etiqueta, título, [(hora, ocupado)], precio, posición de la foto)
# ops: tarjetas (título, [(texto, estado, clase, cambia_a)]) o ('inv', título, [(nombre, porcentaje, texto, cambia_a)])
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
  final=('Más socios entrenando,','menos cobros a mano.')),

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

'fabrica': dict(nombre='Constructora o fábrica', archivo='constructora', palabra='OBRA', obj='casco', acc='#FFC53D', su='tu empresa',
  foto='1684497404598-6e844dff9cde',
  seo='Automatización para constructoras y fábricas', desc='Cotizaciones, proveedores, materiales, cuadrillas, nómina de obra y cartera de tu constructora o fábrica.',
  kicker='Glysf para constructoras y fábricas', hero=('Tu obra controlada', 'desde el celular.'),
  bot_t=('El bot cotiza', 'mientras tú construyes.'), bot_sub='Arma la cotización con tus precios, la envía en PDF y le hace seguimiento.', bot_nombre='Constructora Roble',
  chat=[('u','Buenas, ¿cuánto vale un closet de 2 metros en madera?'),('b','Con gusto. ¿Puertas corredizas o batientes, y en qué color?'),('u','Corredizas, color roble'),('b','Te acabo de enviar la cotización en PDF. Si la apruebas, pedimos el material hoy.'),('pay','Cotización enviada|PDF'),('b','Te escribo en 2 días por si tienes dudas.')],
  cards_t=('Cada obra,', 'con su avance a la vista.'), cards_num='02 · Obras',
  cards=[('Obra Calle 80','Estructura · piso 4',[('Cimientos',1),('Estructura',1),('Mampostería',0),('Acabados',0)],'62%','center 40%'),
         ('Casa Los Pinos','Mampostería',[('Cimientos',1),('Estructura',1),('Mampostería',1),('Acabados',0)],'78%','left 50%'),
         ('Bodega Norte','Acabados',[('Cimientos',1),('Estructura',1),('Mampostería',1),('Acabados',1)],'95%','right 50%')],
  meter=(3,' obras activas ·',19,'personas en cuadrillas'),
  ops_t=('Materiales, cuadrillas y nómina','en orden.'),
  ops=[('Proveedores',[('Orden #912 · Cemento x 120','3 cotizaciones','warn','Orden al mejor precio'),('Varilla 1/2" x 80','Confirmado','ok',''),('Entrega en obra','Programada','ok','Recibido')]),
       ('Nómina de obra',[('Cuadrilla A · 8 personas','Calculando…','ok','Pagada'),('Cuadrilla B · 5 personas','Calculando…','ok','Pagada'),('Residente de obra','Calculando…','ok','Pagada')]),
       ('inv','Materiales en bodega',[('Cemento',18,'200 bultos','Pedido automático al proveedor'),('Ladrillo',45,'8.000 und','')])],
  reporte=['Avance Obra Calle 80: 62%','Material entregado hoy: cemento y varilla','Gasto vs. presupuesto: 48% usado','Cuenta por cobrar: $45.000.000, recordatorio enviado'],
  final=('Más obra avanzando,','menos hojas sueltas.')),
}

E = lambda s: html.escape(str(s), quote=True)

def contacto(n, extra=''):
    wa_txt = f"Hola, vi la demo de {n['nombre'].lower()} en glysf.com y quiero información."
    return f'''<div class="contact-row{extra}">
<a class="pill-btn wa big" data-wa="{E(wa_txt)}" href="https://wa.me/573103102908?text={E(wa_txt)}" target="_blank" rel="noopener">{WA_SVG}Escríbenos por WhatsApp</a>
<a class="pill-btn ghost big" href="mailto:grupolysf@gmail.com?subject={E('Cotización Glysf – ' + n['nombre'])}">{MAIL_SVG}Escríbenos un correo</a>
</div>'''

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
    tabs = ''.join(f'<a href="/{v["archivo"]}.html"' + (' aria-current="page"' if kk == k else '') + f'>{E(v["nombre"])}</a>' for kk, v in NEGOCIOS.items())
    obj_cls = 'ball' if n['obj'] == 'pelota' else 'ball obj'
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
<link rel="stylesheet" href="/negocio.css?v=2">
<script src="/negocio.js?v=2" defer></script>
<script src="/site.js?v=3" defer></script>
</head>
<body style="--acc:{n['acc']}">
<!-- Página generada por herramientas/generar_negocios.py: edita allá, no aquí. -->
<svg width="0" height="0" class="sr" aria-hidden="true"><symbol id="g" viewBox="164 120 234 380"><circle cx="280" cy="262" r="92" fill="none" stroke="currentColor" stroke-width="44"/><path d="M372 168 V 372 Q372 462 280 462 H 236" fill="none" stroke="currentColor" stroke-width="44" stroke-linecap="round"/><circle cx="372" cy="150" r="22" fill="currentColor"/><circle cx="214" cy="462" r="22" fill="currentColor"/></symbol></svg>

<header class="topbar">
<a href="/" class="wordmark" aria-label="Glysf, inicio"><svg aria-hidden="true"><use href="#g"/></svg><span aria-hidden="true">lysf</span></a>
<nav aria-label="Principal">
<a href="/#negocios" class="navlink">Otros negocios</a>
<a href="/#cotizar" class="pill-btn">Cotizar para {E(n['su'])}</a>
</nav>
</header>
<nav class="biztabs" aria-label="Tipos de negocio">{tabs}</nav>

<main>
<section class="scene s-hero" data-scene aria-labelledby="t-hero">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto}"></div><div class="veil"></div></div>
<p class="kicker">{E(n['kicker'])}</p>
<h1 id="t-hero" class="giant" aria-label="{E(n['nombre'])}">{E(n['palabra'])}</h1>
<div class="{obj_cls}" aria-hidden="true">{OBJ[n['obj']]}</div>
<p class="hero-line"><em>{E(n['hero'][0])}</em> {E(n['hero'][1])}</p>
<p class="scroll-hint" aria-hidden="true">Desliza</p>
</div>
</section>

<section class="scene s-bot" data-scene aria-labelledby="t-bot">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto2}" style="background-position:30% 50%"></div><div class="veil"></div></div>
<div class="split">
<div class="copy">
<p class="num">01 · Atención 24/7</p>
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

<section class="scene s-courts" data-scene aria-labelledby="t-courts">
<div class="sticky">
<div class="bg dark-solid"></div>
<div class="courts-wrap">
<div class="copy center">
<p class="num">{E(n['cards_num'])}</p>
<h2 id="t-courts" class="h2">{E(n['cards_t'][0])} <em>{E(n['cards_t'][1])}</em></h2>
</div>
<div class="courts">
{chr(10).join(cards)}
</div>
<p class="meter"><span data-count="{m[0]}">0</span>{E(m[1])} <span data-count="{m[2]}">0</span> {E(m[3])}</p>
</div>
</div>
</section>

<section class="scene s-ops" data-scene aria-labelledby="t-ops">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto3}" style="background-position:70% 50%"></div><div class="veil strong"></div></div>
<div class="ops">
<div class="copy">
<p class="num">03 · Operación</p>
<h2 id="t-ops" class="h2">{E(n['ops_t'][0])} <em>{E(n['ops_t'][1])}</em></h2>
</div>
<div class="cards">
{chr(10).join(ops)}
</div>
</div>
</div>
</section>

<section class="scene s-report" data-scene aria-labelledby="t-report">
<div class="sticky">
<div class="bg"><div class="photo" data-src="{foto2}" style="background-position:50% 30%"></div><div class="veil strong"></div></div>
<div class="report">
<p class="num">04 · Reporte</p>
<h2 id="t-report" class="h2 center">Cada noche, <em>{E(n['su'])} en un mensaje.</em></h2>
<div class="msg-card">
<p class="mc-h"><b>Glysf · Asistente</b><small>Hoy, 10:00 p. m.</small></p>
<ul>{rep}</ul>
</div>
</div>
</div>
</section>

<section class="final" aria-labelledby="t-final">
<div class="bg"><div class="photo still" data-src="{foto}"></div><div class="veil strong"></div></div>
<div class="final-in">
<h2 id="t-final" class="giant-2"><em>{E(n['final'][0])}</em> {E(n['final'][1])}</h2>
<p class="sub">Te mostramos esta demo funcionando con los datos de {E(n['su'])}. Sin costo.</p>
{contacto(n)}
<a href="/#cotizar" class="navlink">O llena el formulario de cotización →</a>
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
        (RAIZ / f"{n['archivo']}.html").write_text(pagina(k, n), encoding='utf-8')
        print('ok', n['archivo'] + '.html')
