// Lanyard Card — Vanilla JS Three.js
// NordicWebFlow — Diego Maldonado card
// Physics simulated without Rapier (spring/rope simulation)

(function () {
  var canvas = document.getElementById('lanyard-canvas');
  if (!canvas) return;

  function loadScript(src, cb) {
    var s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    document.head.appendChild(s);
  }

  loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', function () {
    initLanyard(canvas);
  });

  function initLanyard(canvas) {
    var THREE = window.THREE;

    // ── RENDERER ────────────────────────────────────────────────────────
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;

    var scene = new THREE.Scene();
    var W = canvas.parentElement.offsetWidth;
    var H = canvas.parentElement.offsetHeight;
    var camera = new THREE.PerspectiveCamera(20, W / H, 0.1, 100);
    camera.position.set(0, 0, 24);

    function resize() {
      W = canvas.parentElement.offsetWidth;
      H = canvas.parentElement.offsetHeight;
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      renderer.setSize(W, H, false);
      camera.aspect = W / H;
      camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener('resize', function () { clearTimeout(window._lrt); window._lrt = setTimeout(resize, 120); }, { passive: true });

    // ── LIGHTS ──────────────────────────────────────────────────────────
    scene.add(new THREE.AmbientLight(0xffffff, Math.PI));
    var dl = new THREE.DirectionalLight(0xffffff, 3);
    dl.position.set(5, 10, 10);
    scene.add(dl);
    var pl = new THREE.PointLight(0xE84400, 2, 20);
    pl.position.set(-3, 3, 5);
    scene.add(pl);

    // ── CARD TEXTURE (drawn on canvas) ──────────────────────────────────
    var texCanvas = document.createElement('canvas');
    texCanvas.width = 512;
    texCanvas.height = 720;
    var ctx = texCanvas.getContext('2d');

    function drawCard(photoImg) {
      var w = texCanvas.width, h = texCanvas.height;
      var r = 48; // corner radius

      // Background gradient — dark card
      var grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, '#1a1816');
      grad.addColorStop(1, '#0E0D0B');
      roundRect(ctx, 0, 0, w, h, r);
      ctx.fillStyle = grad;
      ctx.fill();

      // Orange top stripe
      ctx.fillStyle = '#E84400';
      roundRect(ctx, 0, 0, w, 14, { tl: r, tr: r, bl: 0, br: 0 });
      ctx.fill();

      // Subtle orange glow top
      var glow = ctx.createRadialGradient(w / 2, 0, 0, w / 2, 0, 300);
      glow.addColorStop(0, 'rgba(232,68,0,0.18)');
      glow.addColorStop(1, 'transparent');
      ctx.fillStyle = glow;
      ctx.fillRect(0, 0, w, 300);

      // NordicWebFlow logo area
      // Orange rounded square
      ctx.fillStyle = '#E84400';
      roundRect(ctx, w / 2 - 36, 40, 72, 72, 18);
      ctx.fill();
      // N letter
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 44px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('N', w / 2, 76);

      // NordicWebFlow text
      ctx.font = 'bold 22px Inter, sans-serif';
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.fillText('NordicWebFlow', w / 2, 134);

      // Divider
      ctx.strokeStyle = 'rgba(232,68,0,0.35)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(40, 158);
      ctx.lineTo(w - 40, 158);
      ctx.stroke();

      // Photo circle
      var cx = w / 2, cy = 280, pr = 88;
      // Orange ring
      ctx.beginPath();
      ctx.arc(cx, cy, pr + 6, 0, Math.PI * 2);
      ctx.strokeStyle = '#E84400';
      ctx.lineWidth = 3;
      ctx.stroke();
      // Dark ring gap
      ctx.beginPath();
      ctx.arc(cx, cy, pr + 3, 0, Math.PI * 2);
      ctx.strokeStyle = '#0E0D0B';
      ctx.lineWidth = 4;
      ctx.stroke();
      // Clip and draw photo
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, pr, 0, Math.PI * 2);
      ctx.clip();
      if (photoImg) {
        ctx.drawImage(photoImg, cx - pr, cy - pr, pr * 2, pr * 2);
      } else {
        ctx.fillStyle = '#2a2724';
        ctx.fillRect(cx - pr, cy - pr, pr * 2, pr * 2);
        ctx.fillStyle = '#E84400';
        ctx.font = 'bold 48px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('D', cx, cy);
      }
      ctx.restore();

      // Name
      ctx.fillStyle = '#F2EDE7';
      ctx.font = 'bold 30px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'alphabetic';
      ctx.fillText('Diego Maldonado', w / 2, 400);

      // Title
      ctx.fillStyle = 'rgba(242,237,231,0.65)';
      ctx.font = '18px Inter, sans-serif';
      ctx.fillText('Stifter & Digital Strateg', w / 2, 430);

      // Orange divider dot
      ctx.fillStyle = '#E84400';
      ctx.beginPath();
      ctx.arc(w / 2, 456, 3, 0, Math.PI * 2);
      ctx.fill();

      // Email
      ctx.fillStyle = '#E84400';
      ctx.font = '16px Inter, sans-serif';
      ctx.fillText('hej@nordicwebflow.com', w / 2, 484);

      // Bottom badge
      ctx.fillStyle = 'rgba(232,68,0,0.15)';
      roundRect(ctx, w / 2 - 80, 510, 160, 34, 17);
      ctx.fill();
      ctx.strokeStyle = 'rgba(232,68,0,0.4)';
      ctx.lineWidth = 1;
      roundRect(ctx, w / 2 - 80, 510, 160, 34, 17);
      ctx.stroke();
      ctx.fillStyle = '#E84400';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.fillText('nordicwebflow.com', w / 2, 532);

      // Card bottom shine
      var shine = ctx.createLinearGradient(0, h - 120, 0, h);
      shine.addColorStop(0, 'transparent');
      shine.addColorStop(1, 'rgba(232,68,0,0.06)');
      roundRect(ctx, 0, h - 120, w, 120, { tl: 0, tr: 0, bl: r, br: r });
      ctx.fillStyle = shine;
      ctx.fill();
    }

    function roundRect(ctx, x, y, w, h, r) {
      if (typeof r === 'number') r = { tl: r, tr: r, bl: r, br: r };
      ctx.beginPath();
      ctx.moveTo(x + r.tl, y);
      ctx.lineTo(x + w - r.tr, y);
      ctx.quadraticCurveTo(x + w, y, x + w, y + r.tr);
      ctx.lineTo(x + w, y + h - r.br);
      ctx.quadraticCurveTo(x + w, y + h, x + w - r.br, y + h);
      ctx.lineTo(x + r.bl, y + h);
      ctx.quadraticCurveTo(x, y + h, x, y + h - r.bl);
      ctx.lineTo(x, y + r.tl);
      ctx.quadraticCurveTo(x, y, x + r.tl, y);
      ctx.closePath();
    }

    // Load photo then draw
    var cardTexture = new THREE.CanvasTexture(texCanvas);
    var photoImg = new Image();
    photoImg.crossOrigin = 'anonymous';
    photoImg.onload = function () {
      drawCard(photoImg);
      cardTexture.needsUpdate = true;
    };
    photoImg.onerror = function () {
      drawCard(null);
      cardTexture.needsUpdate = true;
    };
    photoImg.src = '/images/Homepage/diego-maldonado.png';
    drawCard(null); // draw placeholder immediately

    // ── LANYARD TEXTURE ─────────────────────────────────────────────────
    var lanyardCanvas = document.createElement('canvas');
    lanyardCanvas.width = 64;
    lanyardCanvas.height = 256;
    var lctx = lanyardCanvas.getContext('2d');
    // Orange lanyard with stripe pattern
    var lg = lctx.createLinearGradient(0, 0, 64, 0);
    lg.addColorStop(0, '#C23A00');
    lg.addColorStop(0.3, '#E84400');
    lg.addColorStop(0.5, '#FF6A2A');
    lg.addColorStop(0.7, '#E84400');
    lg.addColorStop(1, '#C23A00');
    lctx.fillStyle = lg;
    lctx.fillRect(0, 0, 64, 256);
    // Subtle pattern lines
    lctx.strokeStyle = 'rgba(255,255,255,0.12)';
    lctx.lineWidth = 2;
    for (var li = 0; li < 256; li += 16) {
      lctx.beginPath();
      lctx.moveTo(0, li);
      lctx.lineTo(64, li);
      lctx.stroke();
    }
    var lanyardTexture = new THREE.CanvasTexture(lanyardCanvas);
    lanyardTexture.wrapS = lanyardTexture.wrapT = THREE.RepeatWrapping;

    // ── CARD MESH ────────────────────────────────────────────────────────
    var cardGeo = new THREE.BoxGeometry(2.2, 3.1, 0.04);
    var cardMat = new THREE.MeshPhysicalMaterial({
      map: cardTexture,
      clearcoat: 1,
      clearcoatRoughness: 0.1,
      roughness: 0.15,
      metalness: 0.05,
    });
    var cardMesh = new THREE.Mesh(cardGeo, cardMat);
    scene.add(cardMesh);

    // Clip/ring at top of card
    var clipGeo = new THREE.TorusGeometry(0.12, 0.025, 8, 24);
    var metalMat = new THREE.MeshPhysicalMaterial({ color: 0xC0C0C0, metalness: 1, roughness: 0.2 });
    var clip = new THREE.Mesh(clipGeo, metalMat);
    clip.position.set(0, 1.65, 0);
    cardMesh.add(clip);

    // ── ROPE PHYSICS (spring simulation) ────────────────────────────────
    // Anchor point at top (fixed)
    var ANCHOR = new THREE.Vector3(0, 5, 0);

    // Rope nodes: anchor → j1 → j2 → j3 → card top
    var nodes = [
      { pos: new THREE.Vector3(0, 5, 0), vel: new THREE.Vector3(), fixed: true },
      { pos: new THREE.Vector3(0.1, 4, 0), vel: new THREE.Vector3() },
      { pos: new THREE.Vector3(0.2, 3, 0), vel: new THREE.Vector3() },
      { pos: new THREE.Vector3(0.1, 2, 0), vel: new THREE.Vector3() },
    ];
    var SEGMENT_LEN = 1.0;
    var GRAVITY = -18;
    var DAMPING = 0.85;
    var STIFFNESS = 0.8;

    // Card physics state
    var cardPos = new THREE.Vector3(0, 0.3, 0);
    var cardVel = new THREE.Vector3();
    var cardRot = new THREE.Euler();
    var cardAngVel = new THREE.Vector3();

    // Mouse/touch drag
    var isDragging = false;
    var dragOffset = new THREE.Vector3();
    var mouse2D = new THREE.Vector2();
    var raycaster = new THREE.Raycaster();
    var dragPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    var hitPoint = new THREE.Vector3();

    function getPointerNDC(e) {
      var rect = canvas.getBoundingClientRect();
      var cx = e.clientX != null ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      var cy = e.clientY != null ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
      mouse2D.x = ((cx - rect.left) / rect.width) * 2 - 1;
      mouse2D.y = -((cy - rect.top) / rect.height) * 2 + 1;
    }

    canvas.addEventListener('pointerdown', function (e) {
      getPointerNDC(e);
      raycaster.setFromCamera(mouse2D, camera);
      if (raycaster.intersectObject(cardMesh).length > 0) {
        isDragging = true;
        canvas.style.cursor = 'grabbing';
        raycaster.ray.intersectPlane(dragPlane, hitPoint);
        dragOffset.copy(hitPoint).sub(cardPos);
        e.preventDefault();
      }
    }, { passive: false });

    window.addEventListener('pointermove', function (e) {
      if (!isDragging) return;
      getPointerNDC(e);
      raycaster.setFromCamera(mouse2D, camera);
      raycaster.ray.intersectPlane(dragPlane, hitPoint);
      var target = hitPoint.clone().sub(dragOffset);
      cardVel.copy(target.clone().sub(cardPos)).multiplyScalar(12);
      cardPos.copy(target);
    });

    window.addEventListener('pointerup', function () {
      isDragging = false;
      canvas.style.cursor = 'grab';
    });

    canvas.addEventListener('touchstart', function (e) {
      getPointerNDC(e);
      raycaster.setFromCamera(mouse2D, camera);
      if (raycaster.intersectObject(cardMesh).length > 0) {
        isDragging = true;
        raycaster.ray.intersectPlane(dragPlane, hitPoint);
        dragOffset.copy(hitPoint).sub(cardPos);
        e.preventDefault();
      }
    }, { passive: false });

    canvas.addEventListener('touchmove', function (e) {
      if (!isDragging) return;
      getPointerNDC(e);
      raycaster.setFromCamera(mouse2D, camera);
      raycaster.ray.intersectPlane(dragPlane, hitPoint);
      var target = hitPoint.clone().sub(dragOffset);
      cardVel.copy(target.clone().sub(cardPos)).multiplyScalar(12);
      cardPos.copy(target);
      e.preventDefault();
    }, { passive: false });

    canvas.addEventListener('touchend', function () { isDragging = false; });

    // Hover cursor
    canvas.addEventListener('pointermove', function (e) {
      if (isDragging) return;
      getPointerNDC(e);
      raycaster.setFromCamera(mouse2D, camera);
      canvas.style.cursor = raycaster.intersectObject(cardMesh).length > 0 ? 'grab' : 'default';
    });

    // ── ROPE TUBE MESH ────────────────────────────────────────────────────
    var ropePoints = [];
    for (var ri = 0; ri < 20; ri++) ropePoints.push(new THREE.Vector3(0, 5 - ri * 0.25, 0));
    var ropeCurve = new THREE.CatmullRomCurve3(ropePoints);
    var ropeGeo = new THREE.TubeGeometry(ropeCurve, 32, 0.025, 8, false);
    var ropeMat = new THREE.MeshPhysicalMaterial({
      color: 0xE84400,
      metalness: 0.1,
      roughness: 0.4,
      map: lanyardTexture,
    });
    var ropeMesh = new THREE.Mesh(ropeGeo, ropeMat);
    scene.add(ropeMesh);

    // Fixed pin at top
    var pinGeo = new THREE.SphereGeometry(0.06, 8, 8);
    var pin = new THREE.Mesh(pinGeo, metalMat);
    pin.position.copy(ANCHOR);
    scene.add(pin);

    // ── SIMULATE ─────────────────────────────────────────────────────────
    var lastTime = performance.now();
    var clock = { elapsed: 0 };

    function simulate(dt) {
      dt = Math.min(dt, 0.05);

      // Card physics (gravity + drag)
      if (!isDragging) {
        cardVel.y += GRAVITY * dt;
        cardVel.multiplyScalar(DAMPING);
        cardPos.add(cardVel.clone().multiplyScalar(dt));

        // Soft boundary
        var bounds = 3;
        if (Math.abs(cardPos.x) > bounds) { cardVel.x *= -0.5; cardPos.x = Math.sign(cardPos.x) * bounds; }
        if (cardPos.y < -3.5) { cardVel.y *= -0.4; cardPos.y = -3.5; }
        if (cardPos.y > 3) { cardVel.y *= -0.5; cardPos.y = 3; }
      }

      // Gentle auto-sway when not dragged
      if (!isDragging) {
        var t = clock.elapsed;
        cardVel.x += Math.sin(t * 0.4) * 0.004;
        cardAngVel.z += (Math.sin(t * 0.35) * 0.008 - cardRot.z * 0.15);
      }

      // Card angular damping
      cardAngVel.multiplyScalar(0.92);
      cardRot.x += cardAngVel.x * dt * 8;
      cardRot.y += cardAngVel.y * dt * 8;
      cardRot.z += cardAngVel.z * dt * 8;
      cardRot.x = Math.max(-0.4, Math.min(0.4, cardRot.x));
      cardRot.z = Math.max(-0.5, Math.min(0.5, cardRot.z));

      // Rope nodes — simple verlet/spring
      var cardTop = cardPos.clone().add(new THREE.Vector3(0, 1.65, 0));
      var targets = [ANCHOR, null, null, null, cardTop];

      // Solve rope iteratively
      nodes[0].pos.copy(ANCHOR);
      for (var iter = 0; iter < 8; iter++) {
        for (var ni = 1; ni < nodes.length; ni++) {
          var prev = nodes[ni - 1].pos;
          var curr = nodes[ni].pos;
          var diff = curr.clone().sub(prev);
          var d = diff.length();
          if (d > 0.001) {
            var correction = diff.multiplyScalar((d - SEGMENT_LEN) / d * STIFFNESS);
            nodes[ni].pos.sub(correction);
          }
          // Gravity on node
          nodes[ni].pos.y -= GRAVITY * dt * dt * 0.05;
          nodes[ni].pos.y = Math.max(nodes[ni].pos.y, cardTop.y + 0.01);
        }
        // Constrain last node toward cardTop
        nodes[nodes.length - 1].pos.lerp(cardTop, 0.6);
      }

      // Build rope curve from anchor through nodes to card top
      var pts = [ANCHOR.clone()];
      for (var ni = 1; ni < nodes.length; ni++) pts.push(nodes[ni].pos.clone());
      pts.push(cardTop.clone());

      ropeCurve.points = pts;
      var newGeo = new THREE.TubeGeometry(ropeCurve, 32, 0.025, 8, false);
      ropeMesh.geometry.dispose();
      ropeMesh.geometry = newGeo;

      // Apply to card
      cardMesh.position.copy(cardPos);
      cardMesh.rotation.copy(cardRot);
    }

    // ── RENDER LOOP ───────────────────────────────────────────────────────
    var raf;
    var paused = false;

    function tick() {
      if (paused) return;
      raf = requestAnimationFrame(tick);
      var now = performance.now();
      var dt = (now - lastTime) / 1000;
      lastTime = now;
      clock.elapsed += dt;

      simulate(dt);
      renderer.render(scene, camera);
    }

    var obs = new IntersectionObserver(function (entries) {
      paused = !entries[0].isIntersecting;
      if (!paused) { lastTime = performance.now(); tick(); }
    });
    obs.observe(canvas);
    document.addEventListener('visibilitychange', function () {
      paused = document.hidden;
      if (!paused) { lastTime = performance.now(); tick(); }
    });

    tick();
  }
})();
