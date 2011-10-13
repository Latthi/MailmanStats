<html>
<head>
<title>Mailing List Stats</title>
<script src="sorttable.js"></script>
<style>
table.sortable thead
{
    background-color:#eee;
    color:#666666;
    font-weight: bold;
    cursor: default;
}
th
{
     text-align: left;
}
h3
{
	background-color: lightblue;
}
</style>
</head>
<body>
<h1>'@!heading!@' Mailing List Stats</h1>
<h3>@!author.name!@ Stats</h3>
<table>
<tr><td>Author:</td><td>@!author.mail!@</td></tr>
<tr><td>Mails:</td><td>@!author.posts!@</td></tr>
<tr><td>Threads started:</td><td>@!author.started!@</td></tr>
<tr><td>First message:</td><td>@!author.firstmsgdatestr!@</td></tr>
<tr><td>Last message:</td><td>@!author.lastmsgdatestr!@</td></tr>
<tr><td>Average mails sent per day:</td><td>@!author.average!@</td><td></tr>
</table>
</body>
</html>
