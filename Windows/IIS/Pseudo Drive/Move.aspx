<%@ Page Language="C#" %>
<%@ Import Namespace=" System.IO" %>
<script runat="server">
/* Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. */
protected void btnmv_Click(object sender, EventArgs e)
{
   String og_path = ogF.Text;
   String dest_path = destF.Text;

   if(File.Exists(Server.MapPath(og_path)))
   {
      try
      {
         File.Move(Server.MapPath(og_path), Server.MapPath(dest_path));
         mvMessage.Text = "已移动文件";
      } catch (Exception ex) 
      {
         mvMessage.Text = "错误：不能移动本文件";
      }
   }
   else if(Directory.Exists(Server.MapPath(og_path)))
   {
      try
      {
         Directory.Move(Server.MapPath(og_path), Server.MapPath(dest_path));
         mvMessage.Text = "已移动文件夹";
      } catch (Exception ex) 
      {
         mvMessage.Text = "错误：不能移动本文件夹";
      }
   } else
   {
      mvMessage.Text = "错误：请输入正确路径";
   }
}
</script>

<html>
<head>
   <meta charset="UTF-8">
   <meta name="author" content="Frivolous">
   <title>剪切</title>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link href="https://picloud.xyz/Fonts/?%E8%8B%B9%E6%96%B9|%E7%AE%80,400,500" rel="stylesheet">
</head>
<body>
   <form id="form4" runat="server">
   
      <div style="text-align: center; font-family: 苹方简; font-weight: 400; font-size: 1em;">
         <h3 style="font-weight: 500; font-size: 2em;">移动文件及文件夹</h3>
         <br />
         <asp:TextBox id="ogF" placeholder="源文件或文件夹" runat="server" />
         <br />
         <asp:TextBox id="destF" placeholder="目标文件或文件夹" runat="server" />
         <br /><br />
         <asp:Button ID="btnmv" runat="server" onclick="btnmv_Click"  Text="移动" style="width:85px" />
         <br /><br />
         <asp:Label ID="mvMessage" runat="server" />
      </div>
      
   </form>
</body>
</html>
<!-- Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. -->