var fs = require("fs");
var formdata = {};

//게시물을 읽어온다.
var articles = JSON.parse( fs.readFileSync("articles.json").toString() );

if( process.env.QUERY_STRING ) {
  var arr = process.env.QUERY_STRING.split("&");
  for(var i=0; i<arr.length; i+=1) {
    formdata[ arr[i].split("=")[0] ] = decodeURIComponent(arr[i].split("=")[1].replace(/\+/g," "));
  }
}

var page = 1; //현재 페이지

if (formdata.page) var page = parseInt(formdata.page);

var pageCnt = 5; //페이지 보일 수
var postCnt = 10; // 게시글 보일 수

var end = page%pageCnt==0 ? page : page-page%pageCnt+pageCnt; //현재 페이지의 마지막 번호
var start = page%pageCnt==0 ? end-(pageCnt-1) : page-page%pageCnt+1; //현재 페이지의 첫 번호
var total = Math.ceil(articles.length/postCnt); //총 페이지
var next = end+1; //다음 페이지
var prev = start-pageCnt; //이전 페이지
var last = page*postCnt; //게시글 마지막
var first = last-postCnt; //게시글 첫번쨰

if(last>articles.length) last = articles.length;
if(end>total) end = total;

//화면을 그린다.
var html = `<!doctype html><html><head><meta charset='utf-8'><title>게시물 목록 화면</title><link rel="stylesheet" href="style.css"></head><body>
<table style = 'width: 40%'>
<colgroup>
    <col width='5%'>
    <col width='75%'>
    <col width='20%'>
</colgroup>
<tr>
    <th>번호</th>
    <th>제목</th>
    <th>작성자</th>
</tr>`;


//게시물을 순회하면서 각 행을 조립한다.
for(var i=first; i<last; i++){
    html += `
    <tr>
        <td style='text-align:center;'>${articles.length-i}</td>
        <td><a href='read.cgi?no=${i}'>${articles[i].subject}</a></td>
        <td style='text-align:center;'>${articles[i].writer}</td>
    </tr>`;
}

html += `</table>
    <a href='list.cgi?page=${prev<0?1:prev}' class='btn'>이전</a>`;

for(var i=start; i<=end; i++){
    var num = (page == i) ? `[${i}]`:i;
    html += `<a href='list.cgi?page=${i}' ${page == i? 'class=active':''}>${num}</a>`;
}

html += `<a href='list.cgi?page=${next>total?total:next}' class='btn'>다음</a><br><a href='write.html'>글 쓰기</a>
</body></html>`;

var buf = Buffer.from(html);

console.log( "Content-Type: text/html" );
console.log( "Content-Length: "+buf.length );
console.log( "" );
console.log( html );
