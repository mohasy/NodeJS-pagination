var fs = require("fs");

//쿼리스트링으로 전달된 데이터를 파싱
var formdata = {};
if( process.env.QUERY_STRING ) {
  var arr = process.env.QUERY_STRING.split("&");
  for(var i=0; i<arr.length; i+=1) {
    formdata[ arr[i].split("=")[0] ] = decodeURIComponent(arr[i].split("=")[1].replace(/\+/g," "));
  }
}

//게시물 읽어오기
var articles = JSON.parse( fs.readFileSync("articles.json").toString() );

html = `<!doctype html><html><head><meta charset='utf-8'><title>게시물 읽기 화면</title></head><body>
<table style = 'width: 40%'>
<tr>
    <th>제목</th>
    <td colspan='3'>${articles[formdata.no].subject}</td>
</tr>
<tr>
    <th>작성자</th>
    <td>${articles[formdata.no].writer}</td>
</tr>
<tr>
    <th>본문</th>
    <td colspan='3' style='min-height:300px;'>${articles[formdata.no].content}</td>
</tr>
</table>
<a href='list.cgi'>목록으로 돌아가기</a>
</body></html>`;


var buf = Buffer.from(html);

console.log( "Content-Type: text/html" );
console.log( "Content-Length: "+buf.length );
console.log( "" );
console.log( html );