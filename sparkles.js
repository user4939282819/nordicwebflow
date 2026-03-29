// Sparkles background effect — works in light & dark mode
(function(){
  if(window.matchMedia('(prefers-reduced-motion:reduce)').matches)return;

  var canvas=document.createElement('canvas');
  canvas.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;';
  canvas.setAttribute('aria-hidden','true');
  document.body.insertBefore(canvas,document.body.firstChild);

  var ctx=canvas.getContext('2d');
  var W,H,dpr=Math.min(window.devicePixelRatio||1,2);
  var sparks=[];
  var MAX=28;

  function resize(){
    W=window.innerWidth;H=window.innerHeight;
    canvas.width=W*dpr;canvas.height=H*dpr;
    ctx.scale(dpr,dpr);
  }
  resize();
  window.addEventListener('resize',resize,{passive:true});

  function isDark(){
    return document.documentElement.getAttribute('data-theme')==='dark';
  }

  function sparkColor(alpha){
    if(isDark())return'rgba(255,240,200,'+alpha+')';
    return'rgba(180,80,0,'+alpha+')';
  }

  // 4-pointed star path
  function drawStar(x,y,r,rot){
    ctx.beginPath();
    for(var i=0;i<8;i++){
      var angle=rot+(i*Math.PI/4);
      var len=i%2===0?r:r*0.38;
      var px=x+Math.cos(angle)*len;
      var py=y+Math.sin(angle)*len;
      if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);
    }
    ctx.closePath();
  }

  function newSpark(i){
    return{
      x:Math.random()*W,
      y:Math.random()*H,
      r:1.2+Math.random()*2.8,         // 1.2–4px radius
      rot:Math.random()*Math.PI,
      life:0,
      lifeMax:80+Math.random()*120,     // frames alive
      phase:Math.random()*Math.PI*2,    // offset for shimmer
      speed:0.018+Math.random()*0.022
    };
  }

  for(var i=0;i<MAX;i++){
    var s=newSpark(i);
    s.life=Math.random()*s.lifeMax;    // stagger initial phases
    sparks.push(s);
  }

  var raf;
  function tick(){
    ctx.clearRect(0,0,W,H);
    for(var i=0;i<sparks.length;i++){
      var s=sparks[i];
      s.life+=1;
      if(s.life>s.lifeMax){
        sparks[i]=newSpark(i);
        continue;
      }
      // bell-curve opacity: ramp in, hold, ramp out
      var t=s.life/s.lifeMax;
      var alpha=Math.sin(t*Math.PI)*0.65;
      // extra shimmer pulse
      alpha*=0.7+0.3*Math.sin(s.phase+s.life*s.speed*6);
      // slight rotation over life
      s.rot+=0.004;

      ctx.save();
      ctx.fillStyle=sparkColor(alpha.toFixed(3));
      drawStar(s.x,s.y,s.r,s.rot);
      ctx.fill();
      ctx.restore();
    }
    raf=requestAnimationFrame(tick);
  }
  tick();

  // Pause when tab hidden
  document.addEventListener('visibilitychange',function(){
    if(document.hidden){cancelAnimationFrame(raf);}
    else{tick();}
  });
})();
