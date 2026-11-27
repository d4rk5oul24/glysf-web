# Seguridad de glysf.com

## Lo que ya trae la web (en este repo)

- **Página 100 % estática.** No hay base de datos, ni panel de login, ni código en el servidor que se pueda explotar. El formulario abre el correo del cliente; no envía nada a nuestro servidor.
- **nginx endurecido** (`nginx.conf` y `seguridad-headers.conf`):
  - Límite de 15 peticiones por segundo por IP (ráfagas de hasta 60) y máximo 30 conexiones por IP. Quien abuse recibe un error 429.
  - Tiempos de espera cortos contra ataques de conexiones lentas (slowloris).
  - Solo se aceptan GET y HEAD; cualquier otro método recibe un 405.
  - No se sirven archivos ocultos (`.git`, `.env`) ni respaldos.
  - No se muestra la versión del servidor.
- **Cabeceras de seguridad:** CSP estricta (solo se ejecuta nuestro propio `app.js`), HSTS, anti-clickjacking (`X-Frame-Options`), `nosniff`, `Referrer-Policy`, `Permissions-Policy` y aislamiento entre orígenes.
- **HTTPS forzado:** todo lo que llegue por http se redirige a https, y www.glysf.com a glysf.com.
- **Formulario:** campo trampa contra bots, bloqueo de envíos hechos en menos de 4 segundos o repetidos en menos de 30, límites de longitud y limpieza de caracteres de control.
- **Analítica con consentimiento:** Google Analytics solo se carga si el visitante acepta el aviso de cookies.
- **Contenedor:** archivos de la web en solo lectura y chequeo de salud.

Puedes comprobar las cabeceras en https://securityheaders.com cuando esté publicada.

## Lo que hay que hacer fuera del código (en orden de importancia)

### 1. Cloudflare gratis delante de glysf.com (es lo que evita que la tumben)
1. Crea una cuenta en cloudflare.com y agrega `glysf.com` (plan Free).
2. Cloudflare te da dos *nameservers*. En Hostinger cambia los nameservers del dominio por esos dos.
3. En Cloudflare, en DNS, deja el registro `A` de `glysf.com` (y `www`) apuntando a la IP del VPS, con la **nube naranja activada** (proxy).
4. SSL/TLS → modo **Full (strict)**. Activa "Always Use HTTPS". No uses el modo "Flexible": la web ya fuerza HTTPS y con "Flexible" entraría en un bucle de redirecciones.
5. Security → activa **Bot Fight Mode**. Deja el nivel de seguridad en "Medium".
6. Security → WAF → crea una regla de límite de peticiones (Rate limiting), por ejemplo 100 peticiones cada 10 s por IP → bloquear.
7. Si un día los atacan: Security → **"I'm Under Attack Mode"**.

Con esto Cloudflare absorbe los ataques DDoS antes de que lleguen al VPS y la IP real del servidor queda oculta.

### 2. Proteger el VPS (Hostinger)
- Activa la verificación en dos pasos (2FA) en la cuenta de Hostinger.
- Entra por SSH solo con llave, no con contraseña (`PasswordAuthentication no` en `/etc/ssh/sshd_config`).
- Firewall: abre solo 22 (SSH), 80 y 443. En Hostinger hay un firewall en el panel del VPS.
- Instala `fail2ban` para bloquear a quien intente adivinar contraseñas por SSH.
- Activa los respaldos automáticos (snapshots) del VPS en Hostinger.
- Mantén el sistema actualizado (`apt update && apt upgrade`) una vez al mes.

### 3. Proteger Easypanel
- Contraseña larga y única, y 2FA activado.
- Entra al panel por un dominio con HTTPS (por ejemplo `panel.glysf.com`), no por `IP:3000`. Después cierra el puerto 3000 en el firewall.
- Actualiza Easypanel cuando salga una versión nueva.

### 4. GitHub y correo
- 2FA en GitHub y en grupolysf@gmail.com.
- El repo es **público**: nunca subas contraseñas, tokens de API ni archivos `.env`.

### Opcional, más adelante
- Bloquear en el firewall del VPS todo el tráfico 80/443 que no venga de las IPs de Cloudflare, para que nadie pueda saltárselo atacando la IP directamente.
