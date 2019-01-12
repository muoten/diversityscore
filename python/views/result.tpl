<html>
	<head>
		<title>Diversifynd</title>
		<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
		<style>
			* {
				margin: 0;
				padding: 0;
				box-sizing: border-box;
			}

			body {
				font-family: 'Raleway', sans-serif;
				font-size: 16px;
				padding-bottom: 10vh;
			}

			ul { list-style: none; }

			button {
				display: inline-block;
				vertical-align: top;
				width: auto;
				height: auto;
				padding: 2vh 5vw;
				outline: 0;
				background: #ddd;
				color: #555;
				border: 1px solid #ccc;
				font-size: inherit; 
				text-align: center;
				font-family: 'Raleway', sans-serif;
				transition: all .2s ease-in-out;
				cursor: pointer;
			}

			button:hover, 
			button:active { background: #eee; }

			button.secondary {
				background: transparent;
				border-color: #777;
				color: #777;
			}

			button.secondary:hover,
			button.secondary:active {
				border-color: #444;
				color: #444;
			}

			header {
				display: inline-block;
				vertical-align: top;
				width: 100%;
				height: auto;
				padding: 10vh 0 6vh;
				text-align: center;
			}

			header h2 { color: #777; }

			.result-box {
				display: inline-block;
				vertical-align: top;
				width: 90%;
				height: auto;
				margin: 1vh 5%;
				padding: 1vh 5vw;
				text-align: center;
			}

			.image {
				display: block;
				width: auto;
				margin: 5vh auto;
				height: auto;
				max-width: 50vw;
			}

			.image img {
				display: inline-block;
				vertical-align: top;
				width: 100%;
				height: auto;
				margin: 2vh 0;
			}
		</style>
	</head>

	<body>
		<header>
			<h2>Diversifynd: Gender and race diversity demo</h2>
		</header>

		<div class="result-box">
			<!-- Tell me what you see!! -->
			% if stats=="nothing":
				<h3>I can't see anything. I'm blind!</h3>
			% end
			% if stats!="nothing":
				<h3>Stats: {{ stats["text"] }}</h3>
			% end
		</div>


		<!-- Show me the modified image -->
		<div class="image">
			<img src="{{ image }}" />
		</div>
		<center>
			<button id="btn_submit" class="secondary" onclick="window.location.href='/'">Back home</button>
		</center>
	</body>
</html>
