<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">


<title>{{ title }}</title>
<style>
body {
% if itson:
    background-image: url('/static/images/itson.jpg');
% else:
    background-image: url('/static/images/itsoff.jpg');
% end
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
    webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
}
</style>
</head>
<body>
<div class="container">
    <div class="row">&nbsp;</div>
    <div class="row">&nbsp;</div>
    <div class="row">&nbsp;</div>
    <form action="/session" method="POST">
        <h2>{{ title }}</h2>
        <div class="text-center">
            <input type="hidden" name="submited" value="1">
% if itson:
            <input name="comment" placeholder="Comment..."
                   class="form-control" />
            <div class="row">&nbsp;</div>
% for value, label in sizes:
            <div class="form-check form-check-inline btn btn-lg">
                <input type="radio"
                       name="size"
                       id="size_{{value}}"
                       value="{{ value }}"
                       class="form-check-input"
%if value == 1:
                       checked="checked"
% end
                />
                <label class="form-check-label" for="size_{{ value }}">
                    {{ label }}
                </label>
            </div>
% end
            <div class="row">&nbsp;</div>
            <input type="submit" class="btn btn-lg btn-primary"
                   name="stop" value="Stop" />
% else:
            <input type="submit" class="btn btn-lg btn-primary"
                   name="start" value="Start" />
% end
        </div>
    </form>
</div>
</body>
</html>

