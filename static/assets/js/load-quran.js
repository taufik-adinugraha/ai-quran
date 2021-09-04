function getQuran(){
  ["all_ayat","list_nama_surat","max_ayat","terjemah"].forEach(function(element){
    $.getJSON("/static/info/"+element+".json", function(data){
      sessionStorage.setItem(element, JSON.stringify(data));
    });
  });
}

$(function(){
  if (sessionStorage.getItem("all_ayat") === null) {
    getQuran();
  } else {
    console.log("all_ayat is ready to use, call it with e.g: var all_ayat = JSON.parse(sessionStorage.getItem('all_ayat'))");
  }
});
