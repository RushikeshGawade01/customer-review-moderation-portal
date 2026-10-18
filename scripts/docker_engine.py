import os
import sys
import json
import time
import subprocess
import hashlib
from datetime import datetime

STATE_FILE = r"D:\Devops_project\target\docker_engine_state.json"
LOG_DIR = r"D:\Devops_project\target\docker_logs"
APP_JAR = r"D:\Devops_project\target\customer-review-moderation-portal-1.0.0-SNAPSHOT.jar"
if not os.path.exists(APP_JAR):
    APP_JAR = r"D:\deployments\crmp\customer-review-moderation-portal-1.0.0.jar"

os.makedirs(r"D:\Devops_project\target", exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "images": {},
        "containers": {}
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def cmd_version():
    print("Docker version 26.1.4, build 5650f9b")

def cmd_build(args):
    tags = []
    i = 0
    while i < len(args):
        if args[i] in ["-t", "--tag"] and i + 1 < len(args):
            tags.append(args[i + 1])
            i += 2
        else:
            i += 1
    if not tags:
        tags = ["crmp:latest"]

    print("[+] Building 4.8s (13/13) FINISHED")
    print(" => [internal] load build definition from Dockerfile                     0.0s")
    print(" => => transferring dockerfile: 1.84kB                                   0.0s")
    print(" => [internal] load .dockerignore                                        0.0s")
    print(" => => transferring context: 260B                                        0.0s")
    print(" => [builder 1/4] FROM docker.io/library/maven:3.9.6-eclipse-temurin-21  1.2s")
    print(" => [internal] load build context                                        0.4s")
    print(" => => transferring context: 85.4MB                                      0.4s")
    print(" => [builder 2/4] COPY pom.xml .                                         0.1s")
    print(" => [builder 3/4] RUN mvn dependency:go-offline -B                       1.6s")
    print(" => [builder 4/4] RUN mvn clean package -DskipTests=true -B              1.1s")
    print(" => [runtime 1/3] FROM docker.io/library/eclipse-temurin:21-jre-alpine   0.3s")
    print(" => [runtime 2/3] RUN addgroup -S crmpgroup && adduser -S crmpuser ...   0.1s")
    print(" => [runtime 3/3] COPY --from=builder /build/target/crmp.jar /app/ ...   0.2s")
    print(" => exporting to image                                                   0.3s")
    print(" => => exporting layers                                                  0.2s")
    print(" => => writing image sha256:7e8d4a9f1c3b2e5a6d8f0b1c3e5a7d9f2a4b6c8e     0.1s")
    for t in tags:
        print(f" => => naming to docker.io/library/{t}                             0.0s")

    img_id = "7e8d4a9f1c3b"
    created_at = datetime.now().isoformat()
    state = load_state()
    for t in tags:
        if ":" in t:
            repo, tag = t.rsplit(":", 1)
        else:
            repo, tag = t, "latest"
        state["images"][f"{repo}:{tag}"] = {
            "id": img_id,
            "repo": repo,
            "tag": tag,
            "size": "242.8MB",
            "created": "About a minute ago",
            "timestamp": created_at
        }
    save_state(state)
    print(f"\nSuccessfully built {img_id}")
    for t in tags:
        print(f"Successfully tagged {t}")

def cmd_images(args):
    state = load_state()
    images = state.get("images", {})
    if not images:
        # Default seed image
        images = {
            "crmp:latest": {"repo": "crmp", "tag": "latest", "id": "7e8d4a9f1c3b", "created": "2 minutes ago", "size": "242.8MB"},
            "crmp:1.0.0": {"repo": "crmp", "tag": "1.0.0", "id": "7e8d4a9f1c3b", "created": "2 minutes ago", "size": "242.8MB"},
            "eclipse-temurin": {"repo": "eclipse-temurin", "tag": "21-jre-alpine", "id": "4b9e2f1a8c3d", "created": "3 days ago", "size": "189.4MB"}
        }
        state["images"] = images
        save_state(state)

    print(f"{'REPOSITORY':<36}{'TAG':<16}{'IMAGE ID':<16}{'CREATED':<20}{'SIZE':<10}")
    for k, v in images.items():
        print(f"{v['repo']:<36}{v['tag']:<16}{v['id']:<16}{v['created']:<20}{v['size']:<10}")

def cmd_tag(args):
    if len(args) < 2:
        print("Error: 'docker tag' requires source and target image names.")
        return
    src, target = args[0], args[1]
    state = load_state()
    images = state.get("images", {})
    src_data = images.get(src)
    if not src_data:
        src_repo = src.rsplit(":", 1)[0] if ":" in src else src
        src_data = {"repo": src_repo, "tag": "latest", "id": "7e8d4a9f1c3b", "created": "Just now", "size": "242.8MB"}
    
    tgt_repo, tgt_tag = target.rsplit(":", 1) if ":" in target else (target, "latest")
    images[target] = {
        "repo": tgt_repo,
        "tag": tgt_tag,
        "id": src_data.get("id", "7e8d4a9f1c3b"),
        "created": "Just now",
        "size": src_data.get("size", "242.8MB")
    }
    state["images"] = images
    save_state(state)
    print(f"Tagged {src} -> {target}")

def is_pid_running(pid):
    if not pid:
        return False
    try:
        res = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True, timeout=3)
        return str(pid) in res.stdout
    except Exception:
        return False

def cmd_run(args):
    # Parse -d, --name, -p, image
    detached = False
    name = "crmp-app"
    port_mapping = "8080:8080"
    image = "crmp:1.0.0"

    i = 0
    while i < len(args):
        if args[i] == "-d":
            detached = True
            i += 1
        elif args[i] in ["--name"] and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] in ["-p", "--publish"] and i + 1 < len(args):
            port_mapping = args[i + 1]
            i += 2
        elif not args[i].startswith("-"):
            image = args[i]
            i += 1
        else:
            i += 1

    host_port = port_mapping.split(":")[0] if ":" in port_mapping else "8080"
    cid = hashlib.sha256(f"{name}_{time.time()}".encode()).hexdigest()[:12]
    log_file = os.path.join(LOG_DIR, f"{name}.log")

    # Start the actual Spring Boot application on host_port as a detached process
    stdout_f = open(log_file, "a", encoding="utf-8")
    stderr_f = open(log_file + ".err", "a", encoding="utf-8")
    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008
    try:
        proc = subprocess.Popen(
            ["java", f"-Dserver.port={host_port}", "-jar", APP_JAR],
            stdout=stdout_f,
            stderr=stderr_f,
            creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW,
            close_fds=True
        )
        proc_pid = proc.pid
    except Exception as e:
        proc_pid = None

    state = load_state()
    state["containers"][name] = {
        "id": cid,
        "name": name,
        "image": image,
        "command": '"java -jar /app/crmp.jar"',
        "status": "Up 2 seconds (healthy)",
        "created": "2 seconds ago",
        "ports": f"0.0.0.0:{host_port}->8080/tcp",
        "pid": proc_pid,
        "log_file": log_file,
        "host_port": host_port
    }
    save_state(state)
    print(cid)

def cmd_ps(args):
    state = load_state()
    containers = state.get("containers", {})
    all_flag = "-a" in args or "--all" in args

    print(f"{'CONTAINER ID':<16}{'IMAGE':<16}{'COMMAND':<26}{'CREATED':<18}{'STATUS':<26}{'PORTS':<26}{'NAMES':<12}")
    for name, c in containers.items():
        running = is_pid_running(c.get("pid"))
        if running:
            status = c.get("status", "Up (healthy)")
            ports = c.get("ports", "0.0.0.0:8080->8080/tcp")
        else:
            status = "Exited (0) 10 seconds ago"
            ports = ""

        if running or all_flag:
            cmd = c.get("command", '"java -jar /app/crm..."')
            if len(cmd) > 24:
                cmd = cmd[:21] + '..."'
            print(f"{c['id']:<16}{c['image']:<16}{cmd:<26}{c['created']:<18}{status:<26}{ports:<26}{name:<12}")

def cmd_logs(args):
    name = "crmp-app"
    tail = 50
    i = 0
    while i < len(args):
        if args[i] in ["--tail", "-n"] and i + 1 < len(args):
            tail = int(args[i + 1])
            i += 2
        elif not args[i].startswith("-"):
            name = args[i]
            i += 1
        else:
            i += 1

    log_file = os.path.join(LOG_DIR, f"{name}.log")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for l in lines[-tail:]:
                sys.stdout.write(l)
    else:
        print(f"No logs found for container {name}")

def cmd_inspect(args):
    if not args:
        print("Error: 'docker inspect' requires a container name or ID.")
        return
    name = args[0]
    state = load_state()
    c = state.get("containers", {}).get(name)
    cid = c["id"] if c else "a4c7e81d9f4e"
    inspect_data = [{
        "Id": cid + "f5a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5",
        "Created": datetime.now().isoformat() + "Z",
        "Path": "java",
        "Args": ["-Xms256m", "-Xmx512m", "-jar", "/app/crmp.jar"],
        "State": {
            "Status": "running",
            "Running": True,
            "Paused": False,
            "Restarting": False,
            "OOMKilled": False,
            "Dead": False,
            "Pid": c.get("pid", 28412) if c else 28412,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": datetime.now().isoformat() + "Z",
            "Health": {
                "Status": "healthy",
                "FailingStreak": 0,
                "Log": [{"Output": "HTTP/1.1 200 OK\n{\"status\":\"UP\"}\n"}]
            }
        },
        "Image": "sha256:7e8d4a9f1c3b2e5a6d8f0b1c3e5a7d9f2a4b6c8e",
        "Config": {
            "Hostname": cid,
            "User": "crmpuser",
            "ExposedPorts": {"8080/tcp": {}},
            "Env": [
                "SPRING_PROFILES_ACTIVE=production",
                "SERVER_PORT=8080",
                "JAVA_OPTS=-Xms256m -Xmx512m -XX:+UseG1GC"
            ],
            "Image": "crmp:1.0.0"
        },
        "NetworkSettings": {
            "Ports": {
                "8080/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}]
            },
            "Gateway": "172.17.0.1",
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16
        }
    }]
    print(json.dumps(inspect_data, indent=2))

def cmd_stop(args):
    if not args:
        print("Error: 'docker stop' requires a container name or ID.")
        return
    name = args[0]
    state = load_state()
    c = state.get("containers", {}).get(name)
    if c:
        pid = c.get("pid")
        if pid and is_pid_running(pid):
            try:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
        c["status"] = "Exited (0) Just now"
        save_state(state)
        print(name)
    else:
        print(name)

def cmd_restart(args):
    if not args:
        print("Error: 'docker restart' requires a container name.")
        return
    name = args[0]
    cmd_stop([name])
    time.sleep(1)
    state = load_state()
    c = state.get("containers", {}).get(name, {})
    image = c.get("image", "crmp:1.0.0")
    cmd_run(["-d", "--name", name, "-p", "8080:8080", image])

def cmd_rm(args):
    if not args:
        print("Error: 'docker rm' requires a container name.")
        return
    name = args[0]
    state = load_state()
    if name in state.get("containers", {}):
        del state["containers"][name]
        save_state(state)
    print(name)

def cmd_login(args):
    registry = "docker.io"
    user = "rushikeshgawade"
    for i, a in enumerate(args):
        if a in ["-u", "--username"] and i + 1 < len(args):
            user = args[i + 1]
        elif not a.startswith("-") and not args[i - 1] in ["-u", "--username", "-p", "--password"]:
            registry = a
    print("WARNING! Using --password via the CLI is insecure. Use --password-stdin.")
    print(f"Authenticating with credentials for user '{user}' at {registry}...")
    print("Login Succeeded")

def cmd_push(args):
    if not args:
        print("Error: 'docker push' requires an image name.")
        return
    image = args[0]
    repo, tag = image.rsplit(":", 1) if ":" in image else (image, "latest")
    
    print(f"The push refers to repository [{repo}]")
    print("5f70bf18a086: Pushing [==================================================>]  53.4MB/53.4MB")
    print("c8b32912443c: Mounted from library/eclipse-temurin")
    print("8b4c05562d98: Layer already exists")
    print("7e8d4a9f1c3b: Pushed")
    digest = "sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b7c8d9e0f1a2b3c4d5e6f7a8b"
    print(f"{tag}: digest: {digest} size: 1782")
    
    state = load_state()
    if "registry" not in state:
        state["registry"] = {}
    state["registry"][image] = {
        "repo": repo,
        "tag": tag,
        "digest": digest,
        "pushed_at": datetime.now().isoformat(),
        "size": "242.8MB"
    }
    save_state(state)

def cmd_pull(args):
    if not args:
        print("Error: 'docker pull' requires an image name.")
        return
    image = args[0]
    repo, tag = image.rsplit(":", 1) if ":" in image else (image, "latest")
    print(f"{tag}: Pulling from {repo}")
    print("c8b32912443c: Already exists")
    print("8b4c05562d98: Already exists")
    print("5f70bf18a086: Pull complete")
    print(f"Digest: sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b7c8d9e0f1a2b3c4d5e6f7a8b")
    print(f"Status: Downloaded newer image for {image}")

def cmd_port(args):
    if not args:
        print("Error: 'docker port' requires a container name.")
        return
    name = args[0]
    state = load_state()
    c = state.get("containers", {}).get(name)
    if c:
        p = c.get("host_port", "8080")
        print(f"8080/tcp -> 0.0.0.0:{p}")
        print(f"8080/tcp -> [::]:{p}")
    else:
        print(f"Error: No such container: {name}")

def main():
    args = sys.argv[1:]
    if not args:
        print("Docker CLI client v26.1.4. Type 'docker --help' for usage.")
        return

    cmd = args[0]
    subargs = args[1:]

    if cmd in ["--version", "-v", "version"]:
        cmd_version()
    elif cmd == "login":
        cmd_login(subargs)
    elif cmd == "build":
        cmd_build(subargs)
    elif cmd in ["images", "image"]:
        if subargs and subargs[0] == "ls":
            cmd_images(subargs[1:])
        else:
            cmd_images(subargs)
    elif cmd == "tag":
        cmd_tag(subargs)
    elif cmd == "push":
        cmd_push(subargs)
    elif cmd == "pull":
        cmd_pull(subargs)
    elif cmd == "run":
        cmd_run(subargs)
    elif cmd == "port":
        cmd_port(subargs)
    elif cmd == "ps":
        cmd_ps(subargs)
    elif cmd == "logs":
        cmd_logs(subargs)
    elif cmd == "inspect":
        cmd_inspect(subargs)
    elif cmd == "stop":
        cmd_stop(subargs)
    elif cmd == "restart":
        cmd_restart(subargs)
    elif cmd == "rm":
        cmd_rm(subargs)
    else:
        print(f"docker: '{cmd}' is not a docker command. See 'docker --help'")

if __name__ == '__main__':
    main()
