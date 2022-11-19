//let S = null;
const $ = (query) => document.querySelector(query);
const $$ = (query) => document.querySelectorAll(query);

function setItems() {
    // todo
    //console.log(this.response);
    const outType = $('#rsp-type');
    const outCode = $("#rsp-code");
    const outData = $('#rsp-data'); 
    
    outCode.textContent = String(this.status);
    outType.textContent = String(this.responseType);
    outData.textContent = String(this.responseText);
    
    //alert("XHR finished");
}

function makeRequest(){
    // get method
    const outMethod = $('#rsp-method');
    const outURL = $('#rsp-url');
    const outBody = $('#rsp-body');

    let form = $('#req-form');
    let selector = $('#req-method');
    //S = selector;
    //alert(selector);
    let reqmethod = selector.options[selector.selectedIndex].value;

    let requri = $('#req-url').value;
    if (requri === null || requri === '') 
    {
        //alert('ignoring empty message');
        return false;
    }
    let reqbody = $('#req-body').value;
    form.reset();

    // alert(
    //     `Evoke: ${reqmethod}  ${requri} ${reqbody}`
    // );

    let xhr = new XMLHttpRequest();
    
    xhr.open(reqmethod, requri);
    //xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.addEventListener('load', setItems);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");         
    xhr.send(reqbody);

    outMethod.textContent = String(reqmethod);
    outURL.textContent = String(requri);
    outBody.textContent = String(reqbody);

    return false;
}