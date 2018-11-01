<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

<link rel="stylesheet" href="/statics/css/main.css">

<title>{{ title }}</title>

<meta name="og:type" content="article" />
<meta name="og:title" content="Is it ON?" />
<meta name="og:description" content=""/>
<meta name="og:url" content="{{ url }}"/>
<meta name="og:image" content="{{ url }}/statics/images/itson.jpg"/>

<meta name="twitter:title" content="Is it ON?" />
<meta name="twitter:description" content=""/>
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:url" content="{{ url }}"/>

<style>
body {
% if itson:
    background-image: url('/statics/images/itson.jpg');
% else:
    background-image: url('/statics/images/itsoff.jpg');
% end
}
</style>
</head>
<body>
<nav class="navbar navbar-light bg-light">
  <a class="navbar-brand mb-0 h1" href="/">{{ title }}</a>
  <ul class="nav">
    <li class="nav-item">
      <a class="nav-link" href="/history">History</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="/session">New Sess</a>
    </li>
  </ul>
</nav>
<div class="container">

<div class="row">&nbsp;</div>
{{!base}}
</div>
</body>
</html>
