<%@ Page language="C#" Debug="true"%>
<HTML>
<HEAD>
  <TITLE>PDF File Processing</TITLE>
  <STYLE>
    BODY, TH, TD, INPUT, SELECT, TEXTAREA, PRE { FONT-FAMILY: Tahoma; FONT-SIZE: 8pt }
  </STYLE>
  <SCRIPT SRC="common.js"></SCRIPT>
</HEAD>
<BODY TOPMARGIN=0 LEFTMARGIN=0>
<DIV style='margin:5px'>
<%
  // below is the .Net 2.0 legacy synchronous way to it, should use Request.Content.ReadAsMultipartAsync where possible
  System.Web.HttpFileCollection uploadedFiles = Request.Files;
  for (int i = 0; i < uploadedFiles.Count; i++) {
    if (uploadedFiles[i].ContentLength > 0) {
      Response.Write("[ " + uploadedFiles[i].FileName + " ]<br>");
      string targetPath = HttpContext.Current.Server.MapPath("./upload")
        + "\\" + System.IO.Path.GetFileName(uploadedFiles[i].FileName);
      uploadedFiles[i].SaveAs(targetPath);

      System.Diagnostics.Process si = new System.Diagnostics.Process();
      // si.StartInfo.WorkingDirectory = @"c:\";
      si.StartInfo.UseShellExecute = false;
      si.StartInfo.FileName = @"D:\cronjobs\Python34\python.exe";
      si.StartInfo.Arguments = HttpContext.Current.Server.MapPath("./pdfrw-overlay-rect.py")
                             + " \"" + targetPath + "\"" + " " + Request["x"] + " " + Request["y"] 
                             + " " + Request["w"] + " " + Request["h"];
      si.StartInfo.CreateNoWindow = true;
      si.StartInfo.RedirectStandardInput = true;
      si.StartInfo.RedirectStandardOutput = true;
      si.StartInfo.RedirectStandardError = true;
      si.Start();
      string output = si.StandardOutput.ReadToEnd() + "\n\n" + si.StandardError.ReadToEnd();
      int exitCode = si.ExitCode;
      si.Close();
      Response.Write("ExitCode=" + exitCode + "<br>");
      Response.Write("<pre>" + output + "</pre>");
      if (exitCode!=0) Response.End();

      string outFilePath = System.Text.RegularExpressions.Regex.Replace(
        output, @"^\s+$[\r\n]*", "", System.Text.RegularExpressions.RegexOptions.Multiline
      ).Trim();

      int contentLength = 0;
      byte[] buffer;
      using (System.IO.FileStream fs = System.IO.File.OpenRead(outFilePath)) {
        contentLength = (int)fs.Length;
        using (System.IO.BinaryReader br = new System.IO.BinaryReader(fs)) {
           buffer = br.ReadBytes(contentLength);
        }
      }
      if (contentLength > 0) {
        Response.Clear();
        Response.ClearHeaders();
        Response.Cache.SetCacheability(System.Web.HttpCacheability.NoCache);
        //Response.ContentType = "application/octet-stream";
        //Response.AddHeader("content-disposition", String.Format("attachment; filename={0}", System.IO.Path.GetFileName(outFilePath)));
        Response.ContentType = "application/pdf";
        Response.AddHeader("content-disposition", String.Format("inline; filename={0}", System.IO.Path.GetFileName(outFilePath)));
        Response.AppendHeader("Content-Length", contentLength.ToString());
        Response.BinaryWrite(buffer);
        HttpContext.Current.ApplicationInstance.CompleteRequest();
      }

    }
  }
%>
<br>
<script>
  function validateForm(thisForm) {
    if (! thisForm.file1.value.match(/.pdf$/i) ) {
      alert("Invalid file extension/type! This page only accepts [*.pdf] file.");
      return false;
    }
    return validateAllFormFields(thisForm);
  }
</script>
<FORM ACTION="<%=Request.ServerVariables["SCRIPT_NAME"]%>"
 METHOD="POST" ENCTYPE="multipart/form-data"
 onsubmit="return validateForm(this)"
>
  &nbsp; [PDF] <input type=file name=file1 class=required> &nbsp; &nbsp; <input type=submit>
  <br><br>Cover-up Area:
  x=<input type=text datatype=numeric class=required size=2 name=x value="10">
  y=<input type=text datatype=numeric class=required size=2 name=y value="395">
  w=<input type=text datatype=numeric class=required size=2 name=w value="620">
  h=<input type=text datatype=numeric class=required size=2 name=h value="190">
  <br><br>
</FORM>
</DIV>
</BODY>
</HTML>
