<html>
<head>
<title>Mailing List Stats</title>
<script src="sorttable.js"></script>
<style>/* Sortable tables */
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
<tr><td>Name</td><td>Mails Sent</td><td>Last Message</td><td></tr>
<!--(for i in mydic)-->
<tr>
<td>@!mydic[i].mail!@</td><td>@!mydic[i].posts!@</td><td>@!mydic[i].lastmsgdate!@</td>
</tr>
<!--(end)-->
</table>
</html>
