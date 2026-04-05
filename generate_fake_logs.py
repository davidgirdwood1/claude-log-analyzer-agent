import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT_DIR = Path("generated_logs")
OUT_DIR.mkdir(exist_ok=True)

BASE_TIME = datetime(2026, 3, 31, 9, 0, 0)
NUM_LINES = 250

IPS = [
    "10.0.0.10",
    "10.0.0.11",
    "172.16.0.5",
    "192.168.1.22",
    "185.22.44.91",
    "203.0.113.5",
    "198.51.100.77",
]

USER_AGENTS = [
    '"Mozilla/5.0"',
    '"curl/8.5.0"',
    '"python-requests/2.32.0"',
    '"PostmanRuntime/7.37.0"',
]

PATHS = [
    "/",
    "/health",
    "/api/products",
    "/api/products/42",
    "/api/cart",
    "/api/orders",
    "/api/checkout",
    "/login",
    "/admin",
    "/wp-login.php",
]

METHODS = ["GET", "POST"]

APACHE_LEVELS = ["[core:error]", "[php:warn]", "[proxy:error]", "[ssl:error]", "[mpm_event:notice]"]
NGINX_LEVELS = ["error", "warn", "crit", "notice"]
APP_SERVICES = ["auth-service", "checkout-service", "product-service", "api-gateway", "redis", "db-primary"]
SYSLOG_SERVICES = ["sshd", "systemd", "CRON", "kernel", "docker", "sudo"]
KUBE_COMPONENTS = ["ingress", "checkout-pod", "auth-pod", "redis-pod", "db-proxy"]


def ts(offset_seconds: int) -> datetime:
    return BASE_TIME + timedelta(seconds=offset_seconds)


def apache_access_line(t: datetime) -> str:
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    proto = "HTTP/1.1"
    status = random.choices([200, 200, 200, 302, 404, 500, 503], weights=[50, 50, 50, 10, 8, 5, 3])[0]
    size = random.randint(120, 5600)
    referer = '"-"'
    ua = random.choice(USER_AGENTS)
    stamp = t.strftime("%d/%b/%Y:%H:%M:%S +0000")
    return f'{ip} - - [{stamp}] "{method} {path} {proto}" {status} {size} {referer} {ua}'


def apache_error_line(t: datetime) -> str:
    level = random.choice(APACHE_LEVELS)
    pid = random.randint(1000, 9999)
    client = random.choice(IPS)
    messages = [
        "File does not exist: /var/www/html/favicon.ico",
        "script timed out before returning headers: index.php",
        "AH01071: Got error 'PHP message: Undefined array key'",
        "AH00126: Invalid URI in request",
        "server reached MaxRequestWorkers setting, consider raising the MaxRequestWorkers setting",
    ]
    stamp = t.strftime("%a %b %d %H:%M:%S.%f %Y")[:-3]
    return f'[{stamp}] {level} [pid {pid}] [client {client}:0] {random.choice(messages)}'


def nginx_access_line(t: datetime) -> str:
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    status = random.choices([200, 200, 301, 404, 499, 500, 502, 504], weights=[55, 55, 8, 8, 4, 4, 3, 2])[0]
    body_bytes = random.randint(100, 8000)
    req_time = round(random.uniform(0.01, 2.8), 3)
    upstream_time = round(max(0.0, req_time - random.uniform(0, 0.2)), 3)
    stamp = t.strftime("%d/%b/%Y:%H:%M:%S +0000")
    return (
        f'{ip} - - [{stamp}] "{method} {path} HTTP/1.1" {status} {body_bytes} "-" '
        f'{random.choice(USER_AGENTS)} rt={req_time} uct="0.005" uht="{upstream_time}" urt="{upstream_time}"'
    )


def nginx_error_line(t: datetime) -> str:
    level = random.choice(NGINX_LEVELS)
    pid = random.randint(1000, 9999)
    conn = random.randint(100, 999)
    messages = [
        'upstream timed out (110: Connection timed out) while reading response header from upstream',
        'connect() failed (111: Connection refused) while connecting to upstream',
        'client intended to send too large body',
        'limiting requests, excess: 12.440 by zone "api_limit"',
        'open() "/usr/share/nginx/html/robots.txt" failed (2: No such file or directory)',
    ]
    stamp = t.strftime("%Y/%m/%d %H:%M:%S")
    return f'{stamp} [{level}] {pid}#0: *{conn} {random.choice(messages)}, client: {random.choice(IPS)}, server: example.com, request: "GET /api/checkout HTTP/1.1", upstream: "http://127.0.0.1:8080/api/checkout", host: "example.com"'


def app_json_line(t: datetime) -> str:
    service = random.choice(APP_SERVICES)
    level = random.choices(["INFO", "WARN", "ERROR"], weights=[75, 18, 7])[0]
    request_id = f"req_{random.randint(100000, 999999)}"
    messages = {
        "auth-service": ["login success", "token refresh success", "invalid bearer token", "permission denied"],
        "checkout-service": ["checkout completed", "retrying payment provider", "database connection timeout", "payment provider timeout"],
        "product-service": ["product lookup success", "cache miss", "slow query detected"],
        "api-gateway": ["request complete", "upstream 502", "request timeout"],
        "redis": ["command timeout", "eviction cycle completed", "connection restored"],
        "db-primary": ["query completed", "slow query", "remaining connection slots are reserved for superuser connections"],
    }
    msg = random.choice(messages[service])
    latency = random.randint(5, 5000)
    user_id = random.choice(["anon", 104, 122, 650, 713, 980, 4821])
    return f'{t.isoformat()}Z {level} {service} request_id={request_id} user_id={user_id} latency_ms={latency} msg="{msg}"'


def syslog_line(t: datetime) -> str:
    host = "demo-host"
    service = random.choice(SYSLOG_SERVICES)
    pid = random.randint(100, 9999)
    messages = {
        "sshd": ["Failed password for invalid user admin from 185.22.44.91 port 54822 ssh2", "Accepted publickey for deploy from 10.0.0.11 port 52118 ssh2"],
        "systemd": ["Started Daily Cleanup of Temporary Directories.", "Failed to start Demo Background Worker."],
        "CRON": ["(root) CMD (/usr/local/bin/backup.sh)", "(www-data) CMD (/usr/local/bin/rotate_logs.sh)"],
        "kernel": ["Out of memory: Killed process 2213 (python3) total-vm:2048000kB", "TCP: Possible SYN flooding on port 443. Sending cookies."],
        "docker": ["container checkout-service restarted", "health check failed for redis container"],
        "sudo": ["deploy : TTY=pts/0 ; PWD=/srv/app ; USER=root ; COMMAND=/bin/systemctl restart nginx"],
    }
    stamp = t.strftime("%b %d %H:%M:%S")
    return f'{stamp} {host} {service}[{pid}]: {random.choice(messages[service])}'


def kube_line(t: datetime) -> str:
    component = random.choice(KUBE_COMPONENTS)
    level = random.choice(["INFO", "WARN", "ERROR"])
    messages = [
        "readiness probe failed",
        "Back-off restarting failed container",
        "scaled deployment from 3 to 5 replicas",
        "OOMKilled",
        "Successfully pulled image",
        "Liveness probe failed: HTTP probe failed with statuscode: 500",
    ]
    return f'{t.isoformat()}Z {level} {component} namespace=prod pod={component}-{random.randint(1,9)} msg="{random.choice(messages)}"'


def inject_interesting_events(lines: list[str], style: str) -> None:
    if style == "apache_error":
        lines.extend([
            '[Tue Mar 31 09:15:07.330 2026] [proxy:error] [pid 3012] [client 203.0.113.5:0] AH00957: FCGI: attempt to connect to 127.0.0.1:9000 failed',
            '[Tue Mar 31 09:15:08.551 2026] [proxy:error] [pid 3015] [client 198.51.100.77:0] AH01079: failed to make connection to backend: 127.0.0.1',
            '[Tue Mar 31 09:15:12.100 2026] [core:error] [pid 3020] [client 185.22.44.91:0] server reached MaxRequestWorkers setting, consider raising the MaxRequestWorkers setting',
        ])
    elif style == "nginx_error":
        lines.extend([
            '2026/03/31 09:15:07 [error] 2012#0: *411 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 203.0.113.5, server: example.com, request: "POST /api/checkout HTTP/1.1", upstream: "http://127.0.0.1:8080/api/checkout", host: "example.com"',
            '2026/03/31 09:15:12 [crit] 2014#0: *427 connect() failed (111: Connection refused) while connecting to upstream, client: 198.51.100.77, server: example.com, request: "POST /api/checkout HTTP/1.1", upstream: "http://127.0.0.1:8080/api/checkout", host: "example.com"',
            '2026/03/31 09:15:18 [warn] 2015#0: *439 limiting requests, excess: 22.400 by zone "api_limit", client: 185.22.44.91, server: example.com, request: "GET /admin HTTP/1.1", host: "example.com"',
        ])
    elif style == "app_json":
        lines.extend([
            '2026-03-31T09:15:07.330000Z ERROR checkout-service request_id=req_500001 user_id=650 latency_ms=4201 msg="database connection timeout"',
            '2026-03-31T09:15:07.551000Z ERROR db-primary request_id=req_500001 user_id=650 latency_ms=5 msg="remaining connection slots are reserved for superuser connections"',
            '2026-03-31T09:15:22.993000Z ERROR checkout-service request_id=req_500002 user_id=713 latency_ms=4671 msg="database connection timeout"',
            '2026-03-31T09:15:23.144000Z ERROR db-primary request_id=req_500002 user_id=713 latency_ms=6 msg="remaining connection slots are reserved for superuser connections"',
            '2026-03-31T09:15:24.820000Z WARN auth-service request_id=req_500003 user_id=anon latency_ms=71 msg="invalid bearer token from ip 185.22.44.91"',
        ])
    elif style == "syslog":
        lines.extend([
            'Mar 31 09:15:07 demo-host kernel[0]: Out of memory: Killed process 2213 (python3) total-vm:2048000kB',
            'Mar 31 09:15:08 demo-host docker[2231]: container checkout-service restarted',
            'Mar 31 09:15:18 demo-host sshd[5122]: Failed password for invalid user admin from 185.22.44.91 port 54822 ssh2',
            'Mar 31 09:15:19 demo-host sshd[5127]: Failed password for invalid user root from 185.22.44.91 port 54840 ssh2',
        ])
    elif style == "kubernetes":
        lines.extend([
            '2026-03-31T09:15:07.330000Z ERROR checkout-pod namespace=prod pod=checkout-pod-3 msg="Liveness probe failed: HTTP probe failed with statuscode: 500"',
            '2026-03-31T09:15:08.551000Z ERROR checkout-pod namespace=prod pod=checkout-pod-3 msg="Back-off restarting failed container"',
            '2026-03-31T09:15:09.100000Z ERROR redis-pod namespace=prod pod=redis-pod-1 msg="OOMKilled"',
        ])


def build_file(filename: str, generator, style: str, count: int = NUM_LINES) -> None:
    lines = []
    current = 0
    for _ in range(count):
        current += random.randint(1, 4)
        lines.append(generator(ts(current)))
    inject_interesting_events(lines, style)
    random.shuffle(lines)
    lines.sort()
    (OUT_DIR / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    build_file("apache_access.log", apache_access_line, "apache_access")
    build_file("apache_error.log", apache_error_line, "apache_error")
    build_file("nginx_access.log", nginx_access_line, "nginx_access")
    build_file("nginx_error.log", nginx_error_line, "nginx_error")
    build_file("app.json.log", app_json_line, "app_json")
    build_file("syslog.log", syslog_line, "syslog")
    build_file("kubernetes.log", kube_line, "kubernetes")
    print(f"Wrote fake logs to: {OUT_DIR.resolve()}")
    for path in sorted(OUT_DIR.iterdir()):
        print(f"- {path.name}")


if __name__ == "__main__":
    main()
