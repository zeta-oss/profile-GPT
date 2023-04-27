window.onload=()=>{ document.getElementById("btns").onclick=showdata;
document.getElementById("btns").onclick=cleardata;
function cleardata() {
    document.querySelector("#result").setAttribute("src","");
    document.getElementById("pos").innerHTML="";
    document.getElementById("name").innerHTML="";
}
function showdata() {
    /*
    const fetchblog=async (topic)=>{
       const txt= await  fetch(`http://localhost:5000/blog/${topic}`,{
        mode:"cors",
        headers:{
            'Acsess-Control-Allow-Origin' : 'http://localhost:5000'
        }
        }).then((resp)=>{
            if(resp.ok) {
                resp.json().then(data=>console.log(data));
            } else {
                console.log("not ok");
                resp.json().catch(err=>console.log(err));
            }
        });
        document.querySelector("#resp").innerHTML=JSON.stringify(txt);
     };

     
     const fetchsummary=async (blog)=>{
         await fetch(`http://localhost:5000/blogsummary/${blog}`,{
             method:"GET",
             mode:'cors'
            }).then((resp)=>console.log(resp)).then(
             (data)=>{document.querySelector("#summ").innerHTML=data}).catch(err=>console.log(err));
     }
     
     let topic=document.querySelector("#prompt").value;
     console.log(`Topic: ${topic}`);
     
     (async ()=>{await fetchblog(topic)})();
     
     (async ()=>{await fetchsummary(document.querySelector("#resp").value)})();
     */

     let position=document.getElementById("pos").value;
     console.log(position);
     let ref_name=document.getElementById("name").value;
     console.log(ref_name);

//      let blog=jQuery((`http://localhost:5000/blog/${topic}#blog`).replace(/ /g,"%20")).text();

   //  jQuery("#blog").attr("src",`http://localhost:8081/blog/${topic}`);
     //jQuery("#summ").attr("src",`http://localhost:8081/blogsummary?topic=${topic}`);
     if(ref_name.trim()=="" && position.trim()=="") {
        document.querySelector("#result").innerHTML="Please enter the position looking for";
     } else if(ref_name.trim()=="") {
     document.querySelector("#result").setAttribute("src",`http://localhost:8082/search-cand/${position.trim()}`);
     } else {
        document.querySelector("#result").setAttribute("src",`http://localhost:8082/referal-cand/${position.trim()}/${ref_name.trim()}`);
     }
    // document.querySelector("#summ").setAttribute("src",`http://localhost:8081/blogsummary?topic=${topic}`);
    
     
} 
}