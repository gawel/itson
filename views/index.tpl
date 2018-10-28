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
div.back {
    background-color: rgba(255, 255, 255, 0.5);
}
</style>
</head>
<body>
<div class="container">

<div class="row">&nbsp;</div>

<div class="row back">
    <table class="table">
        <tr>
            <th>Date</th>
            <th>Started</th>
            <th>Ended</th>
            <th>Waves</th>
            <th>Duration</th>
            <th>Comment</th>
        </tr>
        % for r in records:
            <tr>
                <td>{{r['date']}}</td>
                <td>{{r['started']}}</td>
                <td>{{r['ended'] or "Its ON!"}}</td>
                <td>{{r['size'] or "Its ON!"}}</td>
                <td>{{r['duration'] or "Its ON!"}}</td>
                <td>{{r['comment'] or ""}}</td>
            </tr>
        % end
        <tr>
            <th>Total</th>
            <th>&nbsp;</th>
            <th>&nbsp;</th>
            <th>{{total}}</th>
            <th>&nbsp;</th>
        </tr>
    </table>
</div>

</div>
</body>
</html>
