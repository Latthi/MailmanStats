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
}</style>
</head>
<body>
<h1>Mailing List Stats</h1>
<table class="sortable">
<tr><th>Name</th><th>Mails Sent</th><th>Last Message</th></tr>
<!--(for i in mydic)-->
<tr>
<td>@!mydic[i].mail!@</td><td>@!mydic[i].posts!@</td><td sorttable_customkey="@!int(mydic[i].lastmsgdate)!@">@!mydic[i].lastmsgdatestr!@</td>
</tr>
<!--(end)-->
</table>
</html>
