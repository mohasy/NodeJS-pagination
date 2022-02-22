var fs = require("fs");

process.stdin.on("data", function(buf) {
    //표준 입력으로 전달된 데이터를 읽어내서 해석한다.
    var postdata = {};
    //Content-Type 헤더가 urlencoded면 &기호로 쪼개는 방식으로 해석한다.
    if( process.env["Content-Type"].indexOf("urlencoded") != -1 ){
        var arr = buf.toString().split("&");
        for(var i=0; i<arr.length; i++){
            postdata[ arr[i].split("=")[0] ] =decodeURIComponent(arr[i].split("=")[1].replace(/\+/g," "));
        }
    }

    //기존에 저장되어 있던 게시물들을 모두 읽어온다.
    var articles = JSON.parse( fs.readFileSync("articles.json").toString() );

    //사용자가 입력한 게시물을 저장한다.
    var article = {subject: postdata.subject, writer: postdata.writer, content: postdata.content};
    articles.unshift(article);

    //사용자가 지금 입력한 게시물을 덧붙인 상태로 다시 저장한다.
    fs.writeFileSync( "articles.json", Buffer.from(JSON.stringify(articles)) );

    //목록화면으로 가는 html을 만들어서 응답
    var html = `<!doctype html><html><head><script>location.href='list.cgi';</script></head></html>`;

    var buf = Buffer.from(html);

    console.log( "Content-Type: text/html" );
    console.log( "Content-Length: "+buf.length );
    console.log( "" );
    console.log( html );
});