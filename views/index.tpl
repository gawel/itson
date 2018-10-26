<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

<title>{{ title }}</title>
<style>
body {
    background-repeat: no-repeat;
    background-size: cover;
% if itson:
    background-image: url('/static/images/itson.jpg')
% else:
    background-image: url('/static/images/itsoff.jpg')
% end
}
</style>
</head>
<body>
<div class="container">

<div class="row">&nbsp;</div>

<div class="row">
    <table class="table">
        <tr>
            <th>Started</th>
            <th>Ended</th>
            <th>Duration</th>
        </tr>
        % for r in records:
            <tr>
                <td>{{r['started']}}</td>
                <td>{{r['ended'] or "Its ON!"}}</td>
                <td>{{r['duration'] or "Its ON!"}}</td>
            </tr>
        % end
        <tr>
            <th>Total</th>
            <th>&nbsp;</th>
            <th>{{total}}</th>
        </tr>
    </table>
</div>

</div>
</body>
</html>
