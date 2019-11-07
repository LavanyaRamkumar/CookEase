function multiInit() {
    setTimeout(get_cuisines, 1000);
    // getc
}

function get_cuisines(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
    if(this.readyState == 4 && this.status == 200) {
        var res = req.responseText;
        var resArr = res.split("$");
        var listing = document.getElementById("cuidiv");
        var card_init='<div class="card col-12 col-md-6 col-lg-3"> <div class="icon-block"><a href="listing.html" id="'
        var card_mid_1='"></a></div><h5 class="mbr-fonts-style display-5">'
        var card_end='<br></h5></div>'
        for (x of resArr){
            var spl=x.split(":");
            console.log(spl)
            var content=card_init+spl[0]+card_mid_1+spl[0]+card_end;
            listing.innerHTML+=content;
            setTimeout(get_cuisines_images,1000,spl[0],spl[1]);
        }   
    } else {
        console.log("working on it!");
    }
    }
    req.open('GET', 'http://localhost:4000/assets/our/msd/cuisines.txt', true);
    req.send();
}

function get_cuisines_images(id,img){
    // console.log(img,id)
    var ele=document.getElementById(id);
    // console.log(ele)
    ele.innerHTML+='<img src="assets/images/cuisines/'+img+'" class = "cuisine-images-css"></img>'
}
multiInit();