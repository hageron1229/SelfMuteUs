html = """<!DOCTYPE html>
<html>
<head>
	<title>SelfMuteUs</title>
	<style type="text/css">
		.user {
			text-align: center;
			padding: 30px;
			margin: 10px;
			width: 100px;
			display: inline-block;
			border: 1px solid black;
			border-radius: 30px;
			background: green;
			color: white;
		}

		.func {
			text-align: center;
			padding: 30px;
			margin: 10px;
			display: inline-block;
			border: 1px solid black;
			border-radius: 30px;
			background: blue;
			color: white;
		}

		.dead {
			background: red;
		}

		.status {
			text-align: center;
			padding: 30px;
			margin: 5px;
			width: 200px;
			display: inline-block;
			border: 1px solid black;
			border-radius: 30px;
			background: gray;
			color: white;
		}

		.selected {
			background: red;
		}
	</style>
</head>
<body>
	<h1>SelfMuteUs</h1>
	<p>
		<h2>Player</h2>
		<div id="users_div"></div>
	</p>
	<p>
		<h2>Status</h2>
		<div class="status selected" id="LOBBY" onclick="change_status('LOBBY');">LOBBY</div>
		<div class="status" id="TASKS" onclick="change_status('TASKS');">TASKS</div>
		<div class="status" id="MEETING" onclick="change_status('MEETING');">MEETING</div>
	</p>
	<p>
		<h2>Settings</h2>
		<div class="func" onclick="location.reload();">全データ再取得</div>
	</p>
	<p style="font-size: 1.2em; font-weight: bold;">接続状況：<span id="connection_status">接続を試みています。</span></p>

<script type="text/javascript">
	/*test = '<div class="user" data-id="123456789">hageron</div><div class="user" data-id="154165411">beef</div>'
	test = [["hageron",12345789],["beef",987654321]]*/

	function get_users(data){
		//console.log("GET USER",data)
		var div = document.getElementById("users_div");
		body = ""
		for(var i=0;i<data.length;i++) {
			if (data[i][2]==1) {
				dead = " dead"
			}else{
				dead = ""
			}
			body += `<div class="user${dead}" onclick="dora('${data[i][1]}');" id="${data[i][1]}">${data[i][0]}</div>`;
		}
		div.innerHTML = body;
	}

	function dora(id) {
		user = document.getElementById(id);
		if (user.className=="user") {
			user.className = "user dead";
			var data = {
				"type": "kill",
				"detail": "dead",
				"name": user.innerHTML,
				"id": user.getAttribute("id"),
			}
		}else{
			var data = {
				"type": "kill",
				"detail": "undead",
				"name": user.innerHTML,
				"id": user.getAttribute("id"),
			}
			user.className = "user";
		}
		send_websocket(data)
	}

	var status = "LOBBY"
	function change_status(new_status) {
		document.getElementById(status).className = "status";
		document.getElementById(new_status).className = "status selected";
		status = new_status;
		var data = {
			"type": "status_change",
			"detail": new_status
		}
		send_websocket(data)
	}

	function get_player_info() {
		var data = {
			"type": "request",
			"detail": "player"
		}
		send_websocket(data);
	}

	function get_status() {
		var data = {
			"type": "request",
			"detail": "status"
		}
		send_websocket(data);
	}

	function send_websocket(data) {
		connection.send(JSON.stringify(data));
	}

	var connection = new WebSocket("ws://127.0.0.1:5000/ws");
	connection.onopen = function(event) {
		document.getElementById("connection_status").innerHTML = "接続中";
		get_player_info()
		get_status()
	}

	connection.onmessage = function(event) {
		//console.log(event.data)
		data = JSON.parse(event.data);
		if (data["type"]=="request"){
			if (data["detail"]=="player") {
				get_users(data["body"]);
			}else if(data["detail"]=="status") {
				change_status(data["body"]["new_status"])
			}
		}
	}

	connection.onclose = function() {
		document.getElementById("connection_status").innerHTML = "切断されました。再読み込みしてください。"
	}
</script>
</body>
</html>
"""