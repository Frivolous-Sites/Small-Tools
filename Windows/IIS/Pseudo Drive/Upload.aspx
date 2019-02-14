<%@ Page Language="C#" %>
<%@ Import Namespace=" System.IO" %>
<script runat="server">
/* Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. */
protected void btnupload_Click(object sender, EventArgs e)
{
   StringBuilder sb = new StringBuilder();
   
   if (FileUpload1.HasFile)
   {
      try
      {
         lblmessage.Text = "正在上传……";
         
         //saving the file
         FileUpload1.SaveAs(Server.MapPath("upload/") + FileUpload1.FileName);
      
         //Showing the file information
         sb.AppendFormat("<br/>文件已保存！具体信息如下：");
         sb.AppendFormat("<br/>名称：{0}", FileUpload1.PostedFile.FileName);
         sb.AppendFormat("<br/>类型：{0}", FileUpload1.PostedFile.ContentType);
         sb.AppendFormat("<br/>大小：{0} 字节", FileUpload1.PostedFile.ContentLength);
         
      } catch (Exception ex)
      {
         sb.Append("<br/> <strong>错误</strong><br/>");
         sb.AppendFormat("具体信息：{0}", ex.Message);
      }
      lblmessage.Text = sb.ToString();
   } else
   {
      lblmessage.Text = "错误：请选择文件";
   }
}
</script>

<html>
<head>
   <meta charset="UTF-8">
   <meta name="author" content="Frivolous">
   <title>上传文件</title>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link href="https://picloud.xyz/Fonts/?%E8%8B%B9%E6%96%B9|%E7%AE%80,400,500" rel="stylesheet">
</head>
<body>
   <form id="form1" runat="server">
   
      <div style="text-align: center; font-family: 苹方简; font-weight: 400; font-size: 1em;">
         <h3 style="font-weight: 500; font-size: 2em;">文件上传</h3>
         <br />
         <asp:FileUpload ID="FileUpload1" runat="server" />
         <br /><br />
         <asp:Button ID="btnsave" runat="server" onclick="btnupload_Click"  Text="上传" style="width:85px" />
         <br /><br />
         <p><asp:Label ID="lblmessage" runat="server" /></p>
      </div>
      
   </form>
</body>
</html>
<!-- Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. -->