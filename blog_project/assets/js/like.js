
const like_icon=document.getElementById('like-icon');
const like_count=document.getElementById('like-count');

like_icon.onclick =()=>{
    console.log("clicked");
    blog_id=like_icon.getAttribute('data-blog');
    const url=`/likeby_user/${parseInt(blog_id)}/`;

    fetch(url,{
        method:"GET",
        headers:{
            'Content-type':'application/json'
        }
    }).then(response => {
        return response.json();
    })
    .then(data =>{
        console.log(data);
        if(data.liked){
            like_icon.classList.remove("empty-heart");
        }else{
            like_icon.classList.add("empty-heart");
        }
        like_count.innerHTML=data.likes_count;
    }).catch(error =>{
        console.log(error);
    })

}


