(function(){
  var KEY='nwf-theme';
  function get(){return localStorage.getItem(KEY)||'light';}
  function apply(theme){
    document.documentElement.setAttribute('data-theme',theme);
    localStorage.setItem(KEY,theme);
    var btn=document.getElementById('theme-toggle');
    if(btn)btn.setAttribute('aria-label',theme==='dark'?'Skift til lystema':'Skift til mørkt tema');
  }
  function init(){
    var btn=document.getElementById('theme-toggle');
    if(!btn)return;
    btn.addEventListener('click',function(){
      document.documentElement.classList.add('switching');
      apply(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');
      setTimeout(function(){document.documentElement.classList.remove('switching');},300);
    });
  }
  apply(get());
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',init);
  } else {
    init();
  }
})();
