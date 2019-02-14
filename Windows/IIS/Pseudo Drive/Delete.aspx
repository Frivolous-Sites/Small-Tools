<%@ Page Language="C#" %>
<%@ Import Namespace=" System.IO" %>
<script runat="server">
/* Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. */
protected void btndel_Click(object sender, EventArgs e)
{
   String ogFile = delFile.Text;
   String ogFolder = delFolder.Text;

   if(ogFolder == "")
   {
      if(File.Exists(Server.MapPath(ogFile)))
      {
         System.IO.File.Delete(Server.MapPath(ogFile));
         delFileMessage.Text = "已删除文件";
      } else
      {
         delFileMessage.Text = "错误：请输入文件或文件夹路径";
      }
   } else
   {
      bool exists = System.IO.Directory.Exists(Server.MapPath(ogFolder));
      if(!exists)
      {
         delFolderMessage.Text = "错误：请输入正确文件夹路径";
      } else
      {
         System.IO.Directory.Delete(Server.MapPath(ogFolder), true);
         delFolderMessage.Text = "已删除文件夹";
      }
      if(File.Exists(Server.MapPath(ogFile)))
      {
         System.IO.File.Delete(Server.MapPath(ogFile));
         delFileMessage.Text = "已删除文件";
      } else if(ogFile != "")
      {
         delFileMessage.Text = "错误：请输入正确文件路径";
      }
   }
}
</script>

<html>
<head>
   <meta charset="UTF-8">
   <meta name="author" content="Frivolous">
   <title>删除</title>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link href="https://picloud.xyz/Fonts/?%E8%8B%B9%E6%96%B9|%E7%AE%80,400,500" rel="stylesheet">
</head>
<body>
   <form id="form3" runat="server">
   
      <div style="text-align: center; font-family: 苹方简; font-weight: 400; font-size: 1em;">
         <h3 style="font-weight: 500; font-size: 2em;">删除文件及文件夹</h3>
         <br />
         <asp:TextBox id="delFile" placeholder="要删除的文件" runat="server" />
         <br />
         <asp:TextBox id="delFolder" placeholder="要删除的文件夹" runat="server" />
         <br /><br />
         <asp:Button ID="btndel" runat="server" onclick="btndel_Click"  Text="删除" style="width:85px" />
         <br /><br />
         <asp:Label ID="delFileMessage" runat="server" />
         <br />
         <asp:Label ID="delFolderMessage" runat="server" />
      </div>
      
   </form>
</body>
</html>
<!-- Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. -->