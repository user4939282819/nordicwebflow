// NordicWebFlow Ballpit — faithful port of React Bits Ballpit
// Uses Three.js r155 + PMREMGenerator + RoomEnvironment for glossy spheres
(function () {
  var canvas = document.getElementById('ballpit-canvas');
  if (!canvas) return;

  // Load Three r155 (has PMREMGenerator, RoomEnvironment built-in addons)
  function load(src, cb) {
    var s = document.createElement('script');
    s.src = src; s.onload = cb; document.head.appendChild(s);
  }

  load('https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.min.js', function () {
    load('https://cdn.jsdelivr.net/npm/three@0.155.0/examples/js/environments/RoomEnvironment.js', function () {
      init();
    });
  });

  function init() {
    var THREE = window.THREE;

    // ── CONFIG (matching React Bits defaults + brand palette) ─────────────
    var COUNT = 60;
    var COLORS = [
      0xE84400, 0xE84400, 0xE84400, 0xE84400, 0xE84400, // heavy orange
      0xFF6A2A, 0xFF6A2A, 0xFF6A2A,                       // light orange
      0xC23A00, 0xC23A00,                                  // dark orange
      0xFF5500,                                            // vivid orange
      0x0E0D0B, 0x1D1B17,                                 // near black
      0xFFD5C0,                                            // orange-light cream
    ];
    var GRAVITY    = 0.5;
    var FRICTION   = 0.9975;
    var WALL_BOUNCE = 0.95;
    var MAX_VEL    = 0.15;
    var MIN_SIZE   = 0.5;
    var MAX_SIZE   = 1.0;
    var SIZE0      = 1.0;
    var MAX_X = 5, MAX_Y = 5, MAX_Z = 2;

    // ── RENDERER ──────────────────────────────────────────────────────────
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 20);

    // ── ENVIRONMENT MAP (RoomEnvironment = glossy reflections) ───────────
    var pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileEquirectangularShader();
    var roomEnv = new THREE.RoomEnvironment(0.04);
    scene.environment = pmrem.fromScene(roomEnv).texture;
    pmrem.dispose();

    // ── LIGHTS ───────────────────────────────────────────────────────────
    scene.add(new THREE.AmbientLight(0xffffff, 1));
    var pointLight = new THREE.PointLight(0xE84400, 200);
    scene.add(pointLight);

    // ── MATERIAL — MeshPhysicalMaterial with clearcoat ───────────────────
    var mat = new THREE.MeshPhysicalMaterial({
      metalness: 0.5,
      roughness: 0.5,
      clearcoat: 1,
      clearcoatRoughness: 0.15,
      envMapIntensity: 1,
    });
    mat.envMap = scene.environment;

    // ── INSTANCED MESH ───────────────────────────────────────────────────
    var geo = new THREE.SphereGeometry(1, 32, 32);
    var mesh = new THREE.InstancedMesh(geo, mat, COUNT);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    // Set colors
    var col = new THREE.Color();
    for (var ci = 0; ci < COUNT; ci++) {
      col.setHex(COLORS[ci % COLORS.length]);
      mesh.setColorAt(ci, col);
    }
    mesh.instanceColor.needsUpdate = true;

    // ── PHYSICS ARRAYS ───────────────────────────────────────────────────
    var pos  = new Float32Array(COUNT * 3);
    var vel  = new Float32Array(COUNT * 3);
    var size = new Float32Array(COUNT);
    var center = new THREE.Vector3();

    // Random spread init
    function randSpread(v) { return (Math.random() - 0.5) * 2 * v; }
    function randFloat(lo, hi) { return lo + Math.random() * (hi - lo); }

    size[0] = SIZE0;
    for (var i = 1; i < COUNT; i++) {
      size[i] = randFloat(MIN_SIZE, MAX_SIZE);
      pos[i*3]   = randSpread(MAX_X);
      pos[i*3+1] = randSpread(MAX_Y);
      pos[i*3+2] = randSpread(MAX_Z);
    }

    // ── PHYSICS UPDATE (exact port of React Bits W class) ─────────────────
    var tA = new THREE.Vector3(), tB = new THREE.Vector3(),
        tC = new THREE.Vector3(), tD = new THREE.Vector3(),
        tE = new THREE.Vector3(), tF = new THREE.Vector3(),
        tG = new THREE.Vector3(), tH = new THREE.Vector3();

    var controlSphere0 = false;

    function updatePhysics(delta) {
      var r0 = controlSphere0 ? 1 : 0;

      if (controlSphere0) {
        tA.fromArray(pos, 0);
        tA.lerp(center, 0.1).toArray(pos, 0);
        vel[0] = vel[1] = vel[2] = 0;
      }

      // Gravity + friction
      for (var i = r0; i < COUNT; i++) {
        var b = i * 3;
        tA.fromArray(pos, b);
        tB.fromArray(vel, b);
        tB.y -= delta * GRAVITY * size[i];
        tB.multiplyScalar(FRICTION);
        if (tB.length() > MAX_VEL) tB.setLength(MAX_VEL);
        tA.add(tB);
        tA.toArray(pos, b);
        tB.toArray(vel, b);
      }

      // Collisions
      for (var i = r0; i < COUNT; i++) {
        var b = i * 3;
        tA.fromArray(pos, b);
        tB.fromArray(vel, b);
        var ri = size[i];

        for (var j = i + 1; j < COUNT; j++) {
          var jb = j * 3;
          tC.fromArray(pos, jb);
          tD.fromArray(vel, jb);
          var rj = size[j];
          tE.copy(tC).sub(tA);
          var d = tE.length();
          var sum = ri + rj;
          if (d < sum && d > 0.001) {
            var overlap = (sum - d) * 0.5;
            tE.normalize().multiplyScalar(overlap);
            tF.copy(tE).multiplyScalar(Math.max(tB.length(), 1));
            tG.copy(tE).multiplyScalar(Math.max(tD.length(), 1));
            tA.sub(tE); tB.sub(tF);
            tA.toArray(pos, b); tB.toArray(vel, b);
            tC.add(tE); tD.add(tG);
            tC.toArray(pos, jb); tD.toArray(vel, jb);
          }
        }

        // Sphere0 collision
        if (controlSphere0) {
          tH.fromArray(pos, 0);
          tE.copy(tH).sub(tA);
          var d0 = tE.length();
          var sum0 = ri + size[0];
          if (d0 < sum0 && d0 > 0.001) {
            var diff = sum0 - d0;
            tE.normalize().multiplyScalar(diff);
            tF.copy(tE).multiplyScalar(Math.max(tB.length(), 2));
            tA.sub(tE); tB.sub(tF);
          }
        }

        // Wall bounce
        if (Math.abs(pos[b]) + ri > MAX_X) {
          pos[b] = Math.sign(pos[b]) * (MAX_X - ri);
          vel[b] = -vel[b] * WALL_BOUNCE;
        }
        if (pos[b+1] - ri < -MAX_Y) {
          pos[b+1] = -MAX_Y + ri;
          vel[b+1] = -vel[b+1] * WALL_BOUNCE;
        }
        if (pos[b+1] + ri > MAX_Y) {
          pos[b+1] = MAX_Y - ri;
          vel[b+1] = -vel[b+1] * WALL_BOUNCE;
        }
        var maxBound = Math.max(MAX_Z, MAX_SIZE);
        if (Math.abs(pos[b+2]) + ri > maxBound) {
          pos[b+2] = Math.sign(pos[b+2]) * (MAX_Z - ri);
          vel[b+2] = -vel[b+2] * WALL_BOUNCE;
        }

        tA.toArray(pos, b);
        tB.toArray(vel, b);
      }
    }

    // ── RESIZE ────────────────────────────────────────────────────────────
    function resize() {
      var wrap = document.getElementById('ballpit-wrap');
      var W = wrap ? wrap.offsetWidth : window.innerWidth;
      var H = wrap ? wrap.offsetHeight : 500;
      renderer.setSize(W, H, false);
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      camera.aspect = W / H;
      camera.updateProjectionMatrix();
      // Recalculate world bounds
      var fov = camera.fov * Math.PI / 180;
      var wH = 2 * Math.tan(fov / 2) * camera.position.z;
      var wW = wH * camera.aspect;
      MAX_X = wW / 2 * 0.92;
      MAX_Y = wH / 2 * 0.92;
    }
    resize();
    window.addEventListener('resize', function () {
      clearTimeout(window._bprt); window._bprt = setTimeout(resize, 100);
    }, { passive: true });

    // ── CURSOR INTERACTION ────────────────────────────────────────────────
    var raycaster = new THREE.Raycaster();
    var mouse = new THREE.Vector2();
    var hitPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    var hitPt = new THREE.Vector3();

    function onMove(e) {
      var rect = canvas.getBoundingClientRect();
      var cx = e.clientX != null ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      var cy = e.clientY != null ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
      mouse.x = ((cx - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((cy - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouse, camera);
      raycaster.ray.intersectPlane(hitPlane, hitPt);
      center.copy(hitPt);
      controlSphere0 = true;
    }
    function onLeave() { controlSphere0 = false; }

    canvas.addEventListener('pointermove', onMove, { passive: true });
    canvas.addEventListener('touchmove', onMove, { passive: true });
    canvas.addEventListener('pointerleave', onLeave);

    // ── RENDER LOOP ───────────────────────────────────────────────────────
    var dummy = new THREE.Object3D();
    var clock = new THREE.Clock();
    var paused = false;
    var raf;

    function tick() {
      if (paused) return;
      raf = requestAnimationFrame(tick);
      var delta = Math.min(clock.getDelta(), 0.05);

      updatePhysics(delta);

      for (var i = 0; i < COUNT; i++) {
        dummy.position.fromArray(pos, i * 3);
        dummy.scale.setScalar(i === 0 && !controlSphere0 ? 0 : size[i]);
        dummy.updateMatrix();
        mesh.setMatrixAt(i, dummy.matrix);
        if (i === 0) pointLight.position.copy(dummy.position);
      }
      mesh.instanceMatrix.needsUpdate = true;
      renderer.render(scene, camera);
    }

    // Pause when off-screen
    new IntersectionObserver(function (e) {
      paused = !e[0].isIntersecting;
      if (!paused) { clock.start(); tick(); }
    }).observe(canvas);
    document.addEventListener('visibilitychange', function () {
      paused = document.hidden;
      if (!paused) { clock.start(); tick(); }
    });

    clock.start();
    tick();
  }
})();
