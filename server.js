var net = require("net");
var fs = require("fs");
var mt = require("mime-types");
var cp = require("child_process");

var server = net.createServer(function(socket) {
    socket.on("data", function(buf) {
        // 웹브라우저가 보내온 HTTP Request를 해석함
        var RequestLines = buf.toString().split("\r\n");
        var RequestMethod = RequestLines[0].split(" ")[0];
        var RequestResource = RequestLines[0].split(" ")[1];
        // 웹브라우저가 요청해온 리소스내용에 물음표 기호가 있으면 물음표 기호 앞까지가 파일명이고, 뒤로는 쿼리스트링이다.
        var queryString = "";
        if( RequestResource.indexOf("?") != -1 ) {
            queryString = RequestResource.split("?")[1];
            RequestResource = RequestResource.split("?")[0];
        }
        //웹브라우저가 요청해온 리소스가 파일이 아니라 폴더일때
        if(RequestResource[RequestResource.length-1] == "/"){
            //미리 정해둔 기본파일을 요청한 것으로 간주함
            RequestResource += "index.html";
        }
        var RequestVersion = RequestLines[0].split(" ")[2];
        var RequestHeaders = {};
        for(var i=1; ; i++){
            if(RequestLines[i] == "") break;
            RequestHeaders[RequestLines[i].split(": ")[0]] = RequestLines[i].split(": ")[1];
        }

        //웹브라우저가 보내온 요청이 get메서드가 아닌 경우, payload를 분리해낸다.
        var payload = Buffer.from("");
        if( RequestMethod != "GET" && RequestHeaders["Content-Length"] ){
            payload = buf.slice(buf.indexOf("\r\n\r\n") + 4);
            console.log("웹브라우저에서 전달받은 payload", payload.toString());
        }

        //웹브라우저에게 보내줄 HTTP Response를 조립한다.
        // 웹브라우저가 요청해온 리소스(=파일)이 존재하는지 확인한다.
        if(fs.existsSync("./files"+RequestResource)){
            //웹브라우저가 요청해온 파일이 존재하는 경우
            // 요청받은 파일이 CGI프로그램인지 확인한다.
            if( RequestResource.indexOf(".cgi") != -1 ) {
                // 웹브라우저가 CGI프로그램의 실행을 요청해 왔다.
                // CGI프로그램을 실행해서 CGI프로그램이 도출하는 산출물을 웹브라우저에게 보내준다.
                var buf = cp.execSync("node ./files"+RequestResource, {
                    input: payload,
                    env: {
                        QUERY_STRING: queryString,
                        ...RequestHeaders
                    }
                });

                //HTTP Response의 1번행을 조립해서 응답한다.
                socket.write(Buffer.from("HTTP/1.1 200 OK\r\n"));
                // HTTP Response의 필수헤더와 컨텐츠를 응답한다.
                socket.write(buf);
            }
            else {
                // 웹브라우저가 스태틱 파일을 요청해 왔다.
                //파일의 내용을 읽어옴
                var buf = fs.readFileSync("./files"+RequestResource);
                //HTTP Response의 1번행을 조립해서 응답한다.
                socket.write(Buffer.from("HTTP/1.1 200 OK\r\n"));
                //HTTP Response의 필수헤더들을 조립해서 응답해준다.
                socket.write(Buffer.from("Content-Type: "+mt.lookup("./files"+RequestResource)+"\r\n"));
                socket.write(Buffer.from("Content-Length: "+buf.length+"\r\n"));
                socket.write(Buffer.from("\r\n"));
                //파일내용을 응답함
                socket.write(buf);
            }
            console.log("웹브라우저가 "+RequestResource+"를 요청해와서, 올바르게 응답하였음.");
        }else {
            //웹브라우저가 요청해온 파일이 존재하지 않는 경우
            //파일이 존재하지 않을 때 웹브라우저에 보여줄 페이지를 만든다.
            var html = "<!doctype html><html><head><meta charset='utf-8'><title>오류페이지</title></head><body><h1>파일이 존재하지 않습니다.</h1></body></html>";
            var buf = Buffer.from(html);
            socket.write(Buffer.from("HTTP/1.1 404 File not found\r\n"));
            socket.write(Buffer.from("Content-Type: text/html\r\n"));
            socket.write(Buffer.from("Content-Length: "+buf.length+"\r\n"));
            socket.write(Buffer.from("\r\n"));
            socket.write(buf);
            console.log("웹브라우저가 "+RequestResource+"를 요청해와서, 파일이 존재하지 않으므로 404 오류를 응답하였음.");
        }
    });
});

server.listen(3500);