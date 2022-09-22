//EL XMLHTTPREQUEST
let xhr = new XMLHttpRequest();
xhr.responseType= 'json';
url= 'http://localhost:5000/listBandas'
metodo = 'GET'
xhr.open(metodo,url,true)
xhr.send();
xhr.onload = function (){
    debugger;
    if (xhr.status != 200){
        console.log("error");
    }
else{
    console.log(JSON.parse(xhr.response))
 console.table(xhr.response);   
}
};


//FETCH DE JAVASCRIPT
fetch ("http://localhost:5000/listBandas",{method:'GET',mode:'cors',headers: {'Access-Control-Allow-Origin':'*','Accept' : 'application/json','Content-Type':'application/json'}})
.then((data)=> console.log(data));