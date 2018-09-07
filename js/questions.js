(function(){
    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/questions';
    fetch(url)
    .then(function(data) {
        console.log(data);
 
    })
    .catch(function(error) {
    console.log(error);
    });   
}());