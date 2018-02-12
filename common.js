function isMSIE() {
  var ua = window.navigator.userAgent;
  if ( ua.indexOf('MSIE ') > 0 || ua.indexOf('Trident/') > 0 || ua.indexOf('Edge/') > 0 ) {
    /*
      Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)
      Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
      Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0 
    */
    return true;
  } else {
    return false;
  }
}

function trim(myString) {   
  myString=myString.replace(/^\s*/, '').replace(/\s*$/, '');
  return myString;
}

function validateNumericList(thisData) {
  var rgExp_numericList, rgExp_blank;
  rgExp_numericList = /^\s*(\d+\s*,\s*)*\d+\s*$/;
  rgExp_blank = /^\s*$/;
  if ( thisData.match(rgExp_blank) || thisData.match(rgExp_numericList) ) {
     return true; 
  } else {
     return false;
  }
}

function validateAllFormFields(thisForm) {
  var count, thisField, datatype, tmpArr, errmsg="";

  for (count=0; count < thisForm.elements.length; count++) {

    thisField=thisForm.elements[count];

    if (thisField.disabled) continue;

    if (thisField.type=="text" || thisField.tagName=="TEXTAREA") {
      thisField.value=trim(thisField.value);
    }

    if (thisField.className=="required") {
      if (thisField.value=="") {
        errmsg = "Please complete this required field.";
        break;
      } else if (thisField.minlength && !isNaN(thisField.minlength)) {
        if (thisField.value.length < Number(thisField.minlength)) {
          errmsg = "Input is too brief. Please re-enter.";
          break;
        }
      }
    }

    if (thisField.maxlength) {
      if (thisField.value.length > thisField.maxlength) {
        errmsg = thisField.name + " contains " + thisField.value.length + " characters. "
               + "It has exceeded the maximum number\nof characters ("
               + thisField.maxlength + ").";
        break;
      }
    }

    if (thisField.getAttribute("datatype") && thisField.value!="") {

      datatype=thisField.getAttribute("datatype").toUpperCase();

      if (datatype == "NUMERIC") {

        if (isNaN(thisField.value)) {
          errmsg = "Please enter a numeric value.";
          break;
        }

      } else if (datatype == "NUMERIC_POSITIVE") {

        if (isNaN(thisField.value)) {
          errmsg = "Please enter a numeric value.";
          break;
        }

        if (Number(thisField.value)<=0) {
          errmsg = "Please enter a numeric value greater than zero.";
          break;
        }

      } else if (datatype == "NUMERIC_MAX") {

        if (isNaN(thisField.value)) {
          errmsg = "Please enter a numeric value.";
          break;
        }

        if (Number(thisField.value)<=0 || Number(thisField.value)>Number(thisField.param)) {
          errmsg = "Please enter a numeric value that greater than zero and not more than " + thisField.param + ".";
          break;
        }

      } else if (datatype == "NUMERICLIST") {

        if (! validateNumericList(thisField.value)) {
          errmsg = "Please enter a list of numeric values separated by commas.";
          break;
        }

      } else if (datatype == "DATE") {

        monthArr=new Array("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC")
        tmpArr=thisField.value.split("-");

        if (tmpArr.length!=3 || isNaN(tmpArr[0]) || isNaN(tmpArr[2]) || tmpArr[0] > 31 || tmpArr[2] > 99 ) {
          errmsg = "Please enter a valid date of DD-MON-YY.";
          break;
        }

        for (i=0; i < 12; i++) {
          if (tmpArr[1].toUpperCase()==monthArr[i])
            break;
        }

        if (i==12) {
          errmsg = "Please enter a valid date of DD-MON-YY.";
          break;
        }

        d=Number(tmpArr[0]);
        m=Number(i+1);
        y=Number(tmpArr[2]);

        if ((((((m%7)?(m%7):1)%2)==0) && (d>30)) || ((m==2) && (d>28+((y%4)?0:1)))) {
          errmsg = "Please enter a valid date of DD-MON-YY.";
          break;
        }

      } // datatype
    } // (thisField.datatype && thisField.value!="")
  } // for

  if (errmsg!="") {
    try { 
      thisField.focus(); 
      alert(errmsg + " [" + thisField.name +"]");
      return(false);
    } catch(e) { }
  }

  return(true);
}

function wget(url, method, timeout) {
  var xmlhttp=null, m="GET", t=0, p=0, pURL=url, pData="", responseText="";
  try {
    xmlhttp = new XMLHttpRequest();
  } catch (e) {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  p = url.indexOf("?");  if (p > 0) {
    pURL = url.substring(0, p);  pData = url.substring(p+1);
  }
  t = parseFloat(timeout);  t = (isNaN(t)) ? 0 : t*1000;  // xmlhttp.timeout = t;
  m = (method=="") ? "GET" : method.toUpperCase();  if (m=="POST") {
    xmlhttp.open(m, pURL, false); // false=>synchronous=>waitForResponse
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  } else {
    pData = "";
    xmlhttp.open(m, url, false); // false=>synchronous=>waitForResponse
  }
  xmlhttp.send(pData); if (xmlhttp.readyState!=4) xmlhttp.waitForResponse(t); // synchronous: with timeout
  //xmlhttp.onreadystatechange = function() { // asynchronous: call a function when the state changes.
   if (xmlhttp.readyState==4 && xmlhttp.status==200) {
     responseText = xmlhttp.responseText;
   } else {
     responseText = "<ERR/>HTTP " + xmlhttp.status
       + " [readyState=" + xmlhttp.readyState + "] "
       + xmlhttp.responseText;
     xmlhttp.abort();
   } 
  //}
  //xmlhttp.send(); // asynchronous
  return responseText;
}
