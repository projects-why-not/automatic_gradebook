

function get_look_ui(str) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", str, false ); // false for synchronous request
    xmlHttp.send( null );
    let form_html = xmlHttp.responseText;

    console.log(form_html);
    let body = document.body;
    body.innerHTML = body.innerHTML + form_html;
}