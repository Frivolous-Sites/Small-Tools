<%@ Page Language="C#" %>
<%@ Import Namespace=" System.IO" %>
<script runat="server">
/* Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. */
protected void btnnew_Click(object sender, EventArgs e)
{
   String dirPath = newFolder.Text;
   bool exists = System.IO.Directory.Exists(Server.MapPath(dirPath));

   if(!exists)
   {
      System.IO.Directory.CreateDirectory(Server.MapPath(dirPath));
      newMessage.Text = "文件夹已创建";
   } else
   {
      newMessage.Text = "错误：文件夹已存在";
   }
}
</script>

<html>
<head>
   <meta charset="UTF-8">
   <meta name="author" content="Frivolous">
   <title>创建文件夹</title>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link href="https://picloud.xyz/Fonts/?%E8%8B%B9%E6%96%B9|%E7%AE%80,400,500" rel="stylesheet">
</head>
<body>
   <form id="form2" runat="server">
   
      <div style="text-align: center; font-family: 苹方简; font-weight: 400; font-size: 1em;">
         <h3 style="font-weight: 500; font-size: 2em;">创建文件夹</h3>
         <br />
         <asp:TextBox id="newFolder" placeholder="新文件夹路径" runat="server" />
         <br /><br />
         <asp:Button ID="btnnew" runat="server" onclick="btnnew_Click"  Text="创建" style="width:85px" />
         <br /><br />
         <asp:Label ID="newMessage" runat="server" />
      </div>
      
   </form>
</body>
</html>
<!-- Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. -->