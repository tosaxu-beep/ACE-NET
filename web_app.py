from flask import Flask, request, render_template_string, redirect
from datetime import datetime
import threading
import webbrowser
import time

from core.nlp_parser import parse_text_to_intent
from core.auto_brain import auto_generate, detect_prefix
from core.device_detector import detect_vendor
from drivers.ssh_driver import analyze_ports, send_config

app = Flask(__name__)

history = []


# ==========================
# AUTO OPEN
# ==========================
def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


# ==========================
# SIMULAÇÃO SHOW VERSION
# ==========================
def fake_show_version(vendor):

    if vendor == "1":
        return "Cisco IOS Software, Catalyst 9300 Switch"

    if vendor == "2":
        return "Huawei Versatile Routing Platform Software VRP"

    return "Cisco IOS Software"


# ==========================
# DEFENDER
# ==========================
def defender_check(intent):

    vlan = intent.get("vlan", 0)

    if vlan <= 0 or vlan > 4094:
        return False

    return True


# ==========================
# PORT MAP SIMULADO
# ==========================
def fake_portmap():

    return {
        "Gi1/0/1":"up",
        "Gi1/0/2":"down",
        "Gi1/0/3":"up",
        "Gi1/0/4":"down",
        "Gi1/0/5":"up",
        "Gi1/0/6":"unknown",
        "Gi1/0/7":"up",
        "Gi1/0/8":"down",
        "Gi1/0/9":"up",
        "Gi1/0/10":"unknown",
        "Gi1/0/11":"up",
        "Gi1/0/12":"down"
    }


# ==========================
# HTML
# ==========================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ACE NET ENTERPRISE TEST BUILD</title>

<style>
body{background:#020617;color:#e5e7eb;font-family:Consolas;margin:0;}
.topbar{padding:15px;border-bottom:1px solid #1f2937;display:flex;justify-content:space-between;}
.container{display:flex;height:95vh;}
.sidebar{width:320px;border-right:1px solid #1f2937;padding:20px;}
.main{flex:1;padding:20px;}

.modules{display:flex;gap:10px;margin-bottom:10px;flex-wrap:wrap;}
.module{flex:1;border:1px solid #1f2937;padding:10px;background:#0f172a;font-size:13px;}

.chatbox{border:1px solid #1f2937;padding:15px;height:35vh;overflow:auto;background:#020617;}

.portmap{
display:grid;
grid-template-columns:repeat(12,1fr);
gap:5px;
margin-top:5px;
}

.port{
padding:8px;
text-align:center;
cursor:pointer;
font-weight:bold;
color:black;
}

.up{background:#22c55e;}
.down{background:#ef4444;}
.unknown{background:#64748b;}

input,select{
width:100%;
padding:8px;
margin-top:6px;
background:black;
color:#22c55e;
border:1px solid #1f2937;
}

button{
margin-top:8px;
padding:8px;
width:100%;
border:none;
color:white;
font-weight:bold;
cursor:pointer;
}

.simular{background:#22c55e;}
.executar{background:#ef4444;}
.limpar{background:#64748b;}
</style>

<script>

function confirmExec(){
    return confirm("⚠ Confirmar execução no dispositivo REAL?");
}

function clickPort(p){

    let num = p.split('/').pop();

    let escolha = prompt(
        "⚙ "+p+"\\n\\n"+
        "1 - VLAN\\n"+
        "2 - shutdown\\n"+
        "3 - no shutdown"
    );

    if(escolha == "1"){
        let vlan = prompt("Digite a VLAN:");
        if(vlan){
            document.querySelector("input[name='texto']").value =
            "porta "+num+" vlan "+vlan;
        }
    }

    if(escolha == "2"){
        document.querySelector("input[name='texto']").value =
        "interface "+num+" shutdown";
    }

    if(escolha == "3"){
        document.querySelector("input[name='texto']").value =
        "interface "+num+" no shutdown";
    }
}

</script>

</head>

<body>

<div class="topbar">
<div>ACE NET ENTERPRISE • TEST BUILD</div>
<div style="color:#22c55e;">● LIVE</div>
</div>

<div class="container">

<div class="sidebar">
<form method="post">

<label>Modo</label>
<select name="modo">
<option value="lab">Laboratório</option>
<option value="prod">Produção</option>
</select>

<label>Vendor</label>
<select name="vendor">
<option value="1">Cisco</option>
<option value="2">Huawei</option>
</select>

<label>IP</label>
<input name="ip"/>

<label>Usuário</label>
<input name="username"/>

<label>Senha</label>
<input type="password" name="password"/>

<label>Comando humano</label>
<input name="texto" required/>

<button name="acao" value="simular" class="simular">SIMULAR</button>
<button name="acao" value="executar" class="executar" onclick="return confirmExec()">EXECUTAR</button>
<button name="acao" value="limpar" class="limpar">🗑 LIMPAR HISTÓRICO</button>

</form>
</div>

<div class="main">

<div class="modules">
<div class="module"><b>HUNTER</b><br>{{hunter}}</div>
<div class="module"><b>PLANNER</b><br>{{planner}}</div>
<div class="module"><b>DEFENDER</b><br>{{defender}}</div>
<div class="module"><b>EXECUTOR</b><br>{{executor}}</div>

<div class="module">
<b>PORT MAP</b>
<div class="portmap">
{% for p,status in portmap.items() %}
<div class="port {{status}}" onclick="clickPort('{{p}}')">
{{p.split('/')[-1]}}
{% if status=='up' %} ↑
{% elif status=='down' %} ↓
{% else %} ↓
{% endif %}
</div>
{% endfor %}
</div>
</div>

<div class="module">
<b>HEALER</b><br>
{% for h in healer %}
{{h}}<br>
{% endfor %}
</div>

</div>

<div class="chatbox">
{% for item in history %}
<div>
<b>{{item.timestamp}}</b><br>
ACE_NET> {{item.command}}<br>
{{item.vendor}}<br>
<pre style="white-space:pre-wrap;">{{item.result}}</pre>
<hr>
</div>
{% endfor %}
</div>

</div>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET","POST"])
def index():

    global history

    hunter="Idle"
    planner="Idle"
    defender="Idle"
    executor="Idle"

    portmap=fake_portmap()
    healer=analyze_ports(portmap)

    if request.method=="POST":

        acao=request.form.get("acao")

        if acao=="limpar":
            history=[]
            return redirect("/")

        texto=request.form.get("texto")
        vendor_select=request.form.get("vendor")

        show_version=fake_show_version(vendor_select)
        vendor=detect_vendor(show_version)
        prefix=detect_prefix(show_version,vendor)

        hunter=f"{vendor} | {prefix}"

        intent=parse_text_to_intent(texto)
        defender="OK" if defender_check(intent) else "ERROR"

        vendor,cmds=auto_generate(show_version,intent)
        planner="OK"

        result_text=""
        for c in cmds:
            result_text+=c+"\\n"

        if acao=="executar":

            ip=request.form.get("ip")
            username=request.form.get("username")
            password=request.form.get("password")

            device={
                "device_type":"cisco_ios",
                "host":ip,
                "username":username,
                "password":password
            }

            send_config(device,cmds)
            executor="EXECUTADO"

        else:
            executor="SIMULAÇÃO"

        history.insert(0,{
            "timestamp":datetime.now().strftime("%H:%M:%S"),
            "command":texto,
            "vendor":vendor,
            "result":result_text
        })

    return render_template_string(
        HTML,
        history=history,
        hunter=hunter,
        planner=planner,
        defender=defender,
        executor=executor,
        portmap=portmap,
        healer=healer
    )


if __name__=="__main__":
    print("\\nACE NET ENTERPRISE TEST BUILD iniciado\\n")
    threading.Thread(target=open_browser).start()
    app.run(debug=False)
