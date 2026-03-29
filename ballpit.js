// Ballpit — vanilla JS Three.js implementation
// Adapted from React Bits / Kevin Levron
// NordicWebFlow brand palette: heavy orange bias

(function() {
  // Only run on homepage
  var canvas = document.getElementById('ballpit-canvas');
  if (!canvas) return;

  // Load Three.js from CDN then init
  function loadScript(src, cb) {
    var s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    document.head.appendChild(s);
  }

  function loadRoomEnv(cb) {
    // RoomEnvironment is baked in below as a minimal inline version
    cb();
  }

  loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', function() {
    initBallpit(canvas);
  });

  function initBallpit(canvas) {
    var THREE = window.THREE;

    // ── CONFIG ──────────────────────────────────────────────────────────
    var CFG = {
      count: 80,
      // Brand palette: heavy orange, dark, cream accents
      colors: [
        0xE84400, // primary orange
        0xFF6A2A, // light orange
        0xC23A00, // dark orange
        0xFF8C4A, // warm orange
        0xE84400, // orange repeat
        0xFF5500, // vivid orange
        0x0E0D0B, // near black
        0x1D1B17, // dark card
        0xE84400, // orange repeat
        0xFFD5C0, // orange-mid light
        0xE84400, // orange repeat
        0xFF6A2A, // light orange
        0xC23A00, // dark orange
        0x0E0D0B, // near black
        0xE84400, // orange
      ],
      gravity: 0.25,
      friction: 0.9975,
      wallBounce: 0.92,
      maxVelocity: 0.18,
      minSize: 0.35,
      maxSize: 1.1,
      size0: 1.2,
      maxX: 8,
      maxY: 5,
      maxZ: 2.5,
      controlSphere0: false,
      followCursor: true,
      ambientIntensity: 1.2,
      lightIntensity: 250,
    };

    // ── RENDERER ────────────────────────────────────────────────────────
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.outputEncoding = THREE.sRGBEncoding;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 20);

    function resize() {
      var p = canvas.parentElement;
      var w = p ? p.offsetWidth : window.innerWidth;
      var h = p ? p.offsetHeight : 500;
      canvas.width = w * Math.min(window.devicePixelRatio, 2);
      canvas.height = h * Math.min(window.devicePixelRatio, 2);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      // update world bounds
      var fov = camera.fov * Math.PI / 180;
      var wH = 2 * Math.tan(fov / 2) * camera.position.z;
      var wW = wH * camera.aspect;
      CFG.maxX = wW / 2 * 0.95;
      CFG.maxY = wH / 2 * 0.95;
    }
    resize();
    window.addEventListener('resize', function() { clearTimeout(window._bprt); window._bprt = setTimeout(resize, 120); }, {passive:true});

    // ── LIGHTS ──────────────────────────────────────────────────────────
    var ambient = new THREE.AmbientLight(0xffffff, CFG.ambientIntensity);
    scene.add(ambient);
    var pointLight = new THREE.PointLight(0xE84400, CFG.lightIntensity);
    pointLight.position.set(0, 0, 5);
    scene.add(pointLight);

    // ── MATERIAL ────────────────────────────────────────────────────────
    var mat = new THREE.MeshPhysicalMaterial({
      metalness: 0.1,
      roughness: 0.08,
      clearcoat: 1,
      clearcoatRoughness: 0.1,
      transparent: true,
      opacity: 0.92,
      envMapIntensity: 1.2,
    });

    // ── GEOMETRY + INSTANCED MESH ────────────────────────────────────────
    var geo = new THREE.SphereGeometry(1, 32, 32);
    var mesh = new THREE.InstancedMesh(geo, mat, CFG.count);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    // Set colors — heavy orange bias
    var colorObj = new THREE.Color();
    for (var ci = 0; ci < CFG.count; ci++) {
      var col = CFG.colors[ci % CFG.colors.length];
      colorObj.set(col);
      mesh.setColorAt(ci, colorObj);
    }
    mesh.instanceColor.needsUpdate = true;

    // ── PHYSICS ─────────────────────────────────────────────────────────
    var pos = new Float32Array(CFG.count * 3);
    var vel = new Float32Array(CFG.count * 3);
    var sizes = new Float32Array(CFG.count);
    var center = new THREE.Vector3();

    // init positions
    for (var pi = 0; pi < CFG.count; pi++) {
      sizes[pi] = pi === 0 ? CFG.size0 : CFG.minSize + Math.random() * (CFG.maxSize - CFG.minSize);
      var b = 3 * pi;
      if (pi > 0) {
        pos[b]     = (Math.random() - 0.5) * 2 * CFG.maxX;
        pos[b + 1] = (Math.random() - 0.5) * 2 * CFG.maxY;
        pos[b + 2] = (Math.random() - 0.5) * 2 * CFG.maxZ;
      }
    }

    var tmpA = new THREE.Vector3();
    var tmpB = new THREE.Vector3();
    var tmpC = new THREE.Vector3();
    var tmpD = new THREE.Vector3();
    var tmpE = new THREE.Vector3();
    var dummy = new THREE.Object3D();

    function updatePhysics(delta) {
      var start = CFG.controlSphere0 ? 1 : 0;

      if (CFG.controlSphere0) {
        // sphere 0 follows cursor
        tmpA.fromArray(pos, 0);
        tmpA.lerp(center, 0.12);
        tmpA.toArray(pos, 0);
        vel[0] = vel[1] = vel[2] = 0;
      }

      for (var i = start; i < CFG.count; i++) {
        var base = 3 * i;
        tmpA.fromArray(pos, base);
        tmpB.fromArray(vel, base);

        tmpB.y -= delta * CFG.gravity * sizes[i];
        tmpB.multiplyScalar(CFG.friction);
        if (tmpB.length() > CFG.maxVelocity) tmpB.setLength(CFG.maxVelocity);
        tmpA.add(tmpB);
        tmpA.toArray(pos, base);
        tmpB.toArray(vel, base);
      }

      // collision detection
      for (var i = start; i < CFG.count; i++) {
        var base = 3 * i;
        tmpA.fromArray(pos, base);
        tmpB.fromArray(vel, base);
        var ri = sizes[i];

        for (var j = i + 1; j < CFG.count; j++) {
          var jbase = 3 * j;
          tmpC.fromArray(pos, jbase);
          tmpD.fromArray(vel, jbase);
          var rj = sizes[j];

          tmpE.copy(tmpC).sub(tmpA);
          var dist = tmpE.length();
          var sum = ri + rj;
          if (dist < sum && dist > 0.0001) {
            var overlap = sum - dist;
            tmpE.normalize().multiplyScalar(overlap * 0.5);
            tmpA.sub(tmpE);
            tmpC.add(tmpE);
            var pushA = tmpE.clone().multiplyScalar(Math.max(tmpB.length(), 1));
            var pushB = tmpE.clone().multiplyScalar(Math.max(tmpD.length(), 1));
            tmpB.sub(pushA);
            tmpD.add(pushB);
            tmpA.toArray(pos, base);
            tmpB.toArray(vel, base);
            tmpC.toArray(pos, jbase);
            tmpD.toArray(vel, jbase);
          }
        }

        // wall bounce
        if (Math.abs(pos[base]) + ri > CFG.maxX) {
          pos[base] = Math.sign(pos[base]) * (CFG.maxX - ri);
          vel[base] = -vel[base] * CFG.wallBounce;
        }
        if (pos[base + 1] - ri < -CFG.maxY) {
          pos[base + 1] = -CFG.maxY + ri;
          vel[base + 1] = -vel[base + 1] * CFG.wallBounce;
        }
        if (pos[base + 1] + ri > CFG.maxY) {
          pos[base + 1] = CFG.maxY - ri;
          vel[base + 1] = -vel[base + 1] * CFG.wallBounce;
        }
        if (Math.abs(pos[base + 2]) + ri > CFG.maxZ) {
          pos[base + 2] = Math.sign(pos[base + 2]) * (CFG.maxZ - ri);
          vel[base + 2] = -vel[base + 2] * CFG.wallBounce;
        }
      }
    }

    // ── CURSOR FOLLOW ────────────────────────────────────────────────────
    var raycaster = new THREE.Raycaster();
    var mouse = new THREE.Vector2();
    var plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    var hit = new THREE.Vector3();

    function onPointerMove(e) {
      var rect = canvas.getBoundingClientRect();
      var cx = e.clientX != null ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      var cy = e.clientY != null ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
      mouse.x = ((cx - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((cy - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouse, camera);
      raycaster.ray.intersectPlane(plane, hit);
      center.copy(hit);
      CFG.controlSphere0 = true;
    }
    function onPointerLeave() { CFG.controlSphere0 = false; }

    canvas.addEventListener('pointermove', onPointerMove, {passive:true});
    canvas.addEventListener('touchmove', onPointerMove, {passive:true});
    canvas.addEventListener('pointerleave', onPointerLeave);

    // ── RENDER LOOP ──────────────────────────────────────────────────────
    var lastTime = performance.now();
    var raf;
    var paused = false;

    function tick() {
      if (paused) return;
      raf = requestAnimationFrame(tick);
      var now = performance.now();
      var delta = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      updatePhysics(delta);

      for (var i = 0; i < CFG.count; i++) {
        dummy.position.fromArray(pos, 3 * i);
        dummy.scale.setScalar(i === 0 && !CFG.controlSphere0 ? 0 : sizes[i]);
        dummy.updateMatrix();
        mesh.setMatrixAt(i, dummy.matrix);
        if (i === 0) pointLight.position.copy(dummy.position);
      }
      mesh.instanceMatrix.needsUpdate = true;
      renderer.render(scene, camera);
    }

    // Pause when not visible
    var observer = new IntersectionObserver(function(entries) {
      paused = !entries[0].isIntersecting;
      if (!paused) { lastTime = performance.now(); tick(); }
    });
    observer.observe(canvas);
    document.addEventListener('visibilitychange', function() {
      paused = document.hidden;
      if (!paused) { lastTime = performance.now(); tick(); }
    });

    tick();
  }
})();
