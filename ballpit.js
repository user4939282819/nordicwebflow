// NordicWebFlow Ballpit — Three.js r134 with inline env map
(function () {
  var canvas = document.getElementById('ballpit-canvas');
  if (!canvas) return;

  function loadScript(src, cb) {
    var s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    s.onerror = function() { console.error('Failed to load', src); };
    document.head.appendChild(s);
  }

  // Use Three.js r134 — stable, has PMREMGenerator
  loadScript('https://cdn.jsdelivr.net/npm/three@0.134.0/build/three.min.js', function () {
    if (!window.THREE) { console.error('Three not loaded'); return; }
    initBallpit();
  });

  function initBallpit() {
    var THREE = window.THREE;

    // ── CONFIG ──────────────────────────────────────────────
    var COUNT      = 50;
    var COLORS_HEX = [0xe84400, 0xff4f00, 0xffffff, 0xffffff];
    var GRAVITY    = 0;        // zero gravity — float freely
    var FRICTION   = 0.9975;
    var WALL_BOUNCE= 0.95;
    var MAX_VEL    = 0.15;
    var MIN_SIZE   = 0.5;
    var MAX_SIZE   = 1.0;
    var SIZE0      = 1.0;

    // ── RENDERER ────────────────────────────────────────────
    var renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1;
    renderer.outputEncoding = THREE.sRGBEncoding;

    var scene  = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 20);
    camera.lookAt(0, 0, 0);

    // ── ENV MAP — hand-crafted PMREMGenerator from neutral grey scene ──
    // Generates a simple studio-like environment for reflections
    var pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileEquirectangularShader();

    // Build a minimal env scene — neutral white room
    var envScene = new THREE.Scene();
    envScene.background = new THREE.Color(0x444444);
    var envLight1 = new THREE.DirectionalLight(0xffffff, 2);
    envLight1.position.set(1, 1, 1);
    envScene.add(envLight1);
    var envLight2 = new THREE.DirectionalLight(0xffffff, 1);
    envLight2.position.set(-1, -1, 1);
    envScene.add(envLight2);

    var envMap = pmrem.fromScene(envScene, 0.04).texture;
    scene.environment = envMap;
    pmrem.dispose();
    envScene.clear();

    // ── LIGHTS ──────────────────────────────────────────────
    scene.add(new THREE.AmbientLight(0xffffff, 1));
    var ptLight = new THREE.PointLight(0xE84400, 200);
    scene.add(ptLight);

    // ── MATERIAL ────────────────────────────────────────────
    var mat = new THREE.MeshPhysicalMaterial({
      metalness:          0.5,
      roughness:          0.5,
      clearcoat:          1,
      clearcoatRoughness: 0.15,
      envMap:             envMap,
      envMapIntensity:    1,
    });

    // ── INSTANCED MESH ───────────────────────────────────────
    var geo  = new THREE.SphereGeometry(1, 32, 32);
    var mesh = new THREE.InstancedMesh(geo, mat, COUNT);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    // Assign colors
    var col = new THREE.Color();
    for (var ci = 0; ci < COUNT; ci++) {
      col.setHex(COLORS_HEX[ci % COLORS_HEX.length]);
      mesh.setColorAt(ci, col);
    }
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;

    // ── PHYSICS ──────────────────────────────────────────────
    var MAX_X = 5, MAX_Y = 5, MAX_Z = 2;

    var pos  = new Float32Array(COUNT * 3);
    var vel  = new Float32Array(COUNT * 3);
    var size = new Float32Array(COUNT);

    function rnd(lo, hi)  { return lo + Math.random() * (hi - lo); }
    function spread(max)  { return (Math.random() - 0.5) * 2 * max; }

    size[0] = SIZE0;
    for (var i = 1; i < COUNT; i++) {
      size[i]     = rnd(MIN_SIZE, MAX_SIZE);
      pos[i*3]    = spread(MAX_X * 0.8);
      pos[i*3+1]  = spread(MAX_Y * 0.8);
      pos[i*3+2]  = spread(MAX_Z);
    }

    var center       = new THREE.Vector3();
    var controlSph0  = false;

    // Temp vectors
    var vA = new THREE.Vector3(), vB = new THREE.Vector3(),
        vC = new THREE.Vector3(), vD = new THREE.Vector3(),
        vE = new THREE.Vector3(), vF = new THREE.Vector3(),
        vG = new THREE.Vector3(), vH = new THREE.Vector3();

    function physics(dt) {
      var r0 = controlSph0 ? 1 : 0;

      // Move sphere-0 toward cursor
      if (controlSph0) {
        vA.fromArray(pos, 0).lerp(center, 0.1).toArray(pos, 0);
        vel[0] = vel[1] = vel[2] = 0;
      }

      // Apply gravity (0) + friction + clamp velocity
      for (var i = r0; i < COUNT; i++) {
        var b = i * 3;
        vA.fromArray(pos, b);
        vB.fromArray(vel, b);
        vB.y -= dt * GRAVITY * size[i];
        vB.multiplyScalar(FRICTION);
        if (vB.length() > MAX_VEL) vB.setLength(MAX_VEL);
        vA.add(vB);
        vA.toArray(pos, b);
        vB.toArray(vel, b);
      }

      // Sphere-sphere collisions
      for (var i = r0; i < COUNT; i++) {
        var b  = i * 3;
        vA.fromArray(pos, b);
        vB.fromArray(vel, b);
        var ri = size[i];
        for (var j = i + 1; j < COUNT; j++) {
          var jb = j * 3;
          vC.fromArray(pos, jb);
          vD.fromArray(vel, jb);
          var rj = size[j];
          vE.copy(vC).sub(vA);
          var d   = vE.length();
          var sum = ri + rj;
          if (d < sum && d > 0.0001) {
            var half = (sum - d) * 0.5;
            vE.normalize().multiplyScalar(half);
            vF.copy(vE).multiplyScalar(Math.max(vB.length(), 1));
            vG.copy(vE).multiplyScalar(Math.max(vD.length(), 1));
            vA.sub(vE); vB.sub(vF); vA.toArray(pos, b);  vB.toArray(vel, b);
            vC.add(vE); vD.add(vG); vC.toArray(pos, jb); vD.toArray(vel, jb);
          }
        }

        // Cursor-sphere push
        if (controlSph0) {
          vH.fromArray(pos, 0);
          vE.copy(vH).sub(vA);
          var d0 = vE.length(), s0 = ri + size[0];
          if (d0 < s0 && d0 > 0.0001) {
            vE.normalize().multiplyScalar(s0 - d0);
            vF.copy(vE).multiplyScalar(Math.max(vB.length(), 2));
            vA.sub(vE); vB.sub(vF);
          }
        }

        // Wall bounce — all 6 faces (gravity=0)
        var b = i * 3;
        if (Math.abs(pos[b])   + ri > MAX_X) {
          pos[b]   = Math.sign(pos[b])   * (MAX_X - ri);
          vel[b]   = -vel[b]   * WALL_BOUNCE;
        }
        if (Math.abs(pos[b+1]) + ri > MAX_Y) {
          pos[b+1] = Math.sign(pos[b+1]) * (MAX_Y - ri);
          vel[b+1] = -vel[b+1] * WALL_BOUNCE;
        }
        if (Math.abs(pos[b+2]) + ri > MAX_Z) {
          pos[b+2] = Math.sign(pos[b+2]) * (MAX_Z - ri);
          vel[b+2] = -vel[b+2] * WALL_BOUNCE;
        }

        vA.toArray(pos, b);
        vB.toArray(vel, b);
      }
    }

    // ── RESIZE ────────────────────────────────────────────────
    function resize() {
      var wrap = document.getElementById('ballpit-wrap');
      var W = wrap ? wrap.offsetWidth  : window.innerWidth;
      var H = wrap ? wrap.offsetHeight : 600;
      renderer.setSize(W, H, false);
      canvas.style.width  = W + 'px';
      canvas.style.height = H + 'px';
      camera.aspect = W / H;
      camera.updateProjectionMatrix();
      var fov = camera.fov * Math.PI / 180;
      var wH  = 2 * Math.tan(fov / 2) * camera.position.z;
      MAX_X = (wH * camera.aspect) / 2 * 0.92;
      MAX_Y = wH / 2 * 0.92;
    }
    resize();
    window.addEventListener('resize', function () {
      clearTimeout(window._bprt);
      window._bprt = setTimeout(resize, 120);
    }, { passive: true });

    // ── CURSOR FOLLOW ─────────────────────────────────────────
    var ray   = new THREE.Raycaster();
    var mNDC  = new THREE.Vector2();
    var plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    var hitPt = new THREE.Vector3();

    function onMove(e) {
      var rect = canvas.getBoundingClientRect();
      var cx = e.clientX != null ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      var cy = e.clientY != null ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
      mNDC.x = ((cx - rect.left) / rect.width)  *  2 - 1;
      mNDC.y = ((cy - rect.top)  / rect.height) * -2 + 1;
      ray.setFromCamera(mNDC, camera);
      ray.ray.intersectPlane(plane, hitPt);
      center.copy(hitPt);
      controlSph0 = true;
    }
    canvas.addEventListener('pointermove', onMove, { passive: true });
    canvas.addEventListener('touchmove',   onMove, { passive: true });
    canvas.addEventListener('pointerleave', function () { controlSph0 = false; });

    // Give balls a small random initial velocity so they move from start
    for (var i = 0; i < COUNT; i++) {
      var speed = 0.04 + Math.random() * 0.06;
      var angle = Math.random() * Math.PI * 2;
      vel[i*3]   = Math.cos(angle) * speed;
      vel[i*3+1] = Math.sin(angle) * speed;
    }

    // ── RENDER LOOP ───────────────────────────────────────────
    var dummy   = new THREE.Object3D();
    var prevT   = performance.now();
    var paused  = false;

    function tick() {
      if (paused) return;
      requestAnimationFrame(tick);
      var now = performance.now();
      var dt  = Math.min((now - prevT) / 1000, 0.05);
      prevT   = now;

      physics(dt);

      for (var i = 0; i < COUNT; i++) {
        dummy.position.fromArray(pos, i * 3);
        dummy.scale.setScalar(i === 0 && !controlSph0 ? 0 : size[i]);
        dummy.updateMatrix();
        mesh.setMatrixAt(i, dummy.matrix);
        if (i === 0) ptLight.position.copy(dummy.position);
      }
      mesh.instanceMatrix.needsUpdate = true;
      renderer.render(scene, camera);
    }

    // Pause when off screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        paused = !entries[0].isIntersecting;
        if (!paused) { prevT = performance.now(); tick(); }
      }).observe(canvas);
    }
    document.addEventListener('visibilitychange', function () {
      paused = document.hidden;
      if (!paused) { prevT = performance.now(); tick(); }
    });

    tick();
  }
})();
