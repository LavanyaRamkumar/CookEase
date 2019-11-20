function multiInit() {
    setTimeout(get_cuisines, 1000);
    // getc
}

function get_cuisines(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
    if(this.readyState == 4 && this.status == 200) {
        var res = JSON.parse(this.responseText);
        var listing = document.getElementById("cuidiv");
        var card_init='<div class="card col-12 col-md-6 col-lg-3"> <div class="icon-block"  style="height:112px; width:315px;"><a href="listing.html" id="'
        var card_mid_1='"></a></div><h5 class="mbr-fonts-style display-5" style="height:112px; width:315px;">'
        var card_end='<br></h5></div>'
        for (x in res){
            var spl=[x,res[x]];
            console.log(spl)
            var content=card_init+spl[0]+card_mid_1+spl[0]+card_end;
            listing.innerHTML+=content;
            setTimeout(get_cuisines_images,1000,spl[0],spl[1]);
        }   
    } else {
        console.log("working on it!");
    }
    }
    req.open('GET', 'http://localhost:5000/get_cuisines', true);
    req.send();
}

function get_cuisines_images(id,img){
    // console.log(img,id)
    var ele=document.getElementById(id);
    // console.log(ele)
    ele.innerHTML+='<img src="../static/assets/images/cuisines/'+img+'" class = "cuisine-images-css"></img>'
}
multiInit();