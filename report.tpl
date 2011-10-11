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
<h1>@!heading!@ Mailing List Stats</h1>
<table class="sortable">
<tr><th>Name</th><th>Mails Sent</th><th>Threads Started</th><th>Last Message</th></tr>
<!--(for i in sa)-->
<tr>
<td><a href="./ml-files/@!mydic[i].pagename!@">@!mydic[i].mail!@</a></td><td>@!mydic[i].posts!@</td><td>@!mydic[i].started!@</td><td sorttable_customkey="@!int(mydic[i].lastmsgdate)!@">@!mydic[i].lastmsgdatestr!@</td>
</tr>
<!--(end)-->
</table>
</html>
