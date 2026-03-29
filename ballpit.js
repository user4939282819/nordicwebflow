// NordicWebFlow Ballpit — vanilla JS port of ReactBits Ballpit
// Loads Three.js ESM + RoomEnvironment via dynamic import (no bundler needed)
(function () {
  var canvas = document.getElementById('ballpit-canvas');
  if (!canvas) return;

  Promise.all([
    import('https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.module.js'),
    import('https://cdn.jsdelivr.net/npm/three@0.155.0/examples/jsm/environments/RoomEnvironment.js')
  ]).then(function (mods) {
    start(mods[0], mods[1].RoomEnvironment);
  }).catch(function (err) {
    console.error('[Ballpit] Failed to load Three.js:', err);
  });

  function start(THREE, RoomEnvironment) {

    // ── CONFIG ─────────────────────────────────────────────────────────────
    var CONFIG = {
      count:        100,
      colors:       ['#ff6600', '#ffffff', '#ff6600', '#ff7300'],
      ambientColor: 0xffffff,
      ambientIntensity: 1,
      lightIntensity: 200,
      materialParams: {
        metalness:          0.5,
        roughness:          0.5,
        clearcoat:          1,
        clearcoatRoughness: 0.15
      },
      minSize:      0.5,
      maxSize:      1.0,
      size0:        1.0,
      gravity:      0.01,
      friction:     0.9975,
      wallBounce:   0.95,
      maxVelocity:  0.15,
      maxX:         5,
      maxY:         5,
      maxZ:         2,
      controlSphere0: false,
      followCursor: false
    };

    // ── RENDERER ──────────────────────────────────────────────────────────
    var renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;

    var scene  = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
    camera.position.set(0, 0, 20);
    camera.lookAt(0, 0, 0);

    // ── ENV MAP via RoomEnvironment + PMREMGenerator ───────────────────────
    var pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileCubemapShader();
    var envTexture = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environment = envTexture;
    pmrem.dispose();

    // ── MATERIAL — MeshPhysicalMaterial + subsurface scattering shader ────
    var sssUniforms = {
      thicknessDistortion: { value: 0.1 },
      thicknessAmbient:    { value: 0 },
      thicknessAttenuation:{ value: 0.1 },
      thicknessPower:      { value: 2 },
      thicknessScale:      { value: 10 }
    };

    var mat = new THREE.MeshPhysicalMaterial(
      Object.assign({ envMap: envTexture }, CONFIG.materialParams)
    );
    // envMapRotation must be mutated in-place (it's a getter-backed Euler)
    mat.envMapRotation.x = -Math.PI / 2;
    mat.defines = mat.defines || {};
    mat.defines.USE_UV = '';

    mat.onBeforeCompile = function (shader) {
      Object.assign(shader.uniforms, sssUniforms);

      // Prepend uniform declarations
      shader.fragmentShader =
        'uniform float thicknessPower;\n' +
        'uniform float thicknessScale;\n' +
        'uniform float thicknessDistortion;\n' +
        'uniform float thicknessAmbient;\n' +
        'uniform float thicknessAttenuation;\n' +
        shader.fragmentShader;

      // Inject RE_Direct_Scattering function before main()
      shader.fragmentShader = shader.fragmentShader.replace(
        'void main() {',
        [
          'void RE_Direct_Scattering(const in IncidentLight directLight, const in vec2 uv, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, inout ReflectedLight reflectedLight) {',
          '  vec3 scatteringHalf = normalize(directLight.direction + (geometryNormal * thicknessDistortion));',
          '  float scatteringDot = pow(saturate(dot(geometryViewDir, -scatteringHalf)), thicknessPower) * thicknessScale;',
          '  #ifdef USE_COLOR',
          '    vec3 scatteringIllu = (scatteringDot + thicknessAmbient) * vColor;',
          '  #else',
          '    vec3 scatteringIllu = (scatteringDot + thicknessAmbient) * diffuse;',
          '  #endif',
          '  reflectedLight.directDiffuse += scatteringIllu * thicknessAttenuation * directLight.color;',
          '}',
          'void main() {'
        ].join('\n')
      );

      // Patch lights_fragment_begin to also call RE_Direct_Scattering
      var patched = THREE.ShaderChunk.lights_fragment_begin.replaceAll(
        'RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );',
        'RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );\n' +
        'RE_Direct_Scattering(directLight, vUv, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, reflectedLight);'
      );
      shader.fragmentShader = shader.fragmentShader.replace(
        '#include <lights_fragment_begin>', patched
      );
    };

    // ── INSTANCED MESH ────────────────────────────────────────────────────
    var geo  = new THREE.SphereGeometry(1, 32, 32);
    var mesh = new THREE.InstancedMesh(geo, mat, CONFIG.count);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    var ambLight = new THREE.AmbientLight(CONFIG.ambientColor, CONFIG.ambientIntensity);
    mesh.add(ambLight);
    var ptLight  = new THREE.PointLight(0xff6600, CONFIG.lightIntensity);
    mesh.add(ptLight);

    // ── COLOR GRADIENT ────────────────────────────────────────────────────
    (function () {
      var cols = CONFIG.colors.map(function (h) { return new THREE.Color(h); });
      function getColor(ratio) {
        var n = cols.length - 1;
        var scaled = Math.max(0, Math.min(1, ratio)) * n;
        var idx = Math.floor(scaled);
        var s = cols[idx];
        if (idx >= n) return s.clone();
        var a = scaled - idx;
        var e = cols[idx + 1];
        return new THREE.Color(
          s.r + a * (e.r - s.r),
          s.g + a * (e.g - s.g),
          s.b + a * (e.b - s.b)
        );
      }
      for (var ci = 0; ci < CONFIG.count; ci++) {
        mesh.setColorAt(ci, getColor(ci / CONFIG.count));
        if (ci === 0) ptLight.color.copy(getColor(0));
      }
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
    })();

    // ── PHYSICS DATA ──────────────────────────────────────────────────────
    var posData  = new Float32Array(CONFIG.count * 3).fill(0);
    var velData  = new Float32Array(CONFIG.count * 3).fill(0);
    var sizeData = new Float32Array(CONFIG.count).fill(1);

    sizeData[0] = CONFIG.size0;
    for (var i = 1; i < CONFIG.count; i++) {
      posData[i*3]   = (Math.random() - 0.5) * 2 * CONFIG.maxX;
      posData[i*3+1] = (Math.random() - 0.5) * 2 * CONFIG.maxY;
      posData[i*3+2] = (Math.random() - 0.5) * 2 * CONFIG.maxZ;
      sizeData[i] = CONFIG.minSize + Math.random() * (CONFIG.maxSize - CONFIG.minSize);
    }
    // Give all balls an initial random velocity so they move immediately
    for (var i = 0; i < CONFIG.count; i++) {
      var spd = 0.05 + Math.random() * 0.08;
      var ang = Math.random() * Math.PI * 2;
      velData[i*3]   = Math.cos(ang) * spd;
      velData[i*3+1] = Math.sin(ang) * spd;
      velData[i*3+2] = (Math.random() - 0.5) * spd;
    }

    // Pre-allocated Vector3 scratch registers (avoids GC pressure)
    var vA = new THREE.Vector3(), vB = new THREE.Vector3();
    var vC = new THREE.Vector3(), vD = new THREE.Vector3();
    var vE = new THREE.Vector3(), vF = new THREE.Vector3();
    var vG = new THREE.Vector3(), vH = new THREE.Vector3();

    // ── PHYSICS UPDATE (faithful port of class W) ─────────────────────────
    function updatePhysics(delta) {
      var idx, base, jdx, otherBase, dist, sumR, overlap, r2;

      // Step 1: gravity + friction + velocity integration
      for (idx = 0; idx < CONFIG.count; idx++) {
        base = idx * 3;
        vA.fromArray(posData, base);
        vB.fromArray(velData, base);
        vB.y -= delta * CONFIG.gravity * sizeData[idx];
        vB.multiplyScalar(CONFIG.friction);
        vB.clampLength(0, CONFIG.maxVelocity);
        vA.add(vB);
        vA.toArray(posData, base);
        vB.toArray(velData, base);
      }

      // Step 2: ball–ball collisions + wall bounce
      for (idx = 0; idx < CONFIG.count; idx++) {
        base = idx * 3;
        vA.fromArray(posData, base);
        vB.fromArray(velData, base);
        var radius = sizeData[idx];

        for (jdx = idx + 1; jdx < CONFIG.count; jdx++) {
          otherBase = jdx * 3;
          vC.fromArray(posData, otherBase);
          vD.fromArray(velData, otherBase);
          r2 = sizeData[jdx];
          vE.copy(vC).sub(vA);
          dist = vE.length();
          sumR = radius + r2;
          if (dist < sumR && dist > 0.0001) {
            overlap = sumR - dist;
            vF.copy(vE).normalize().multiplyScalar(0.5 * overlap);
            vG.copy(vF).multiplyScalar(Math.max(vB.length(), 1));
            vH.copy(vF).multiplyScalar(Math.max(vD.length(), 1));
            vA.sub(vF); vB.sub(vG);
            vA.toArray(posData, base); vB.toArray(velData, base);
            vC.add(vF); vD.add(vH);
            vC.toArray(posData, otherBase); vD.toArray(velData, otherBase);
          }
        }

        // Wall bounce
        if (Math.abs(vA.x) + radius > CONFIG.maxX) {
          vA.x = Math.sign(vA.x) * (CONFIG.maxX - radius);
          vB.x = -vB.x * CONFIG.wallBounce;
        }
        if (CONFIG.gravity === 0) {
          if (Math.abs(vA.y) + radius > CONFIG.maxY) {
            vA.y = Math.sign(vA.y) * (CONFIG.maxY - radius);
            vB.y = -vB.y * CONFIG.wallBounce;
          }
        } else if (vA.y - radius < -CONFIG.maxY) {
          vA.y = -CONFIG.maxY + radius;
          vB.y = -vB.y * CONFIG.wallBounce;
        }
        var maxB = Math.max(CONFIG.maxZ, CONFIG.maxSize);
        if (Math.abs(vA.z) + radius > maxB) {
          vA.z = Math.sign(vA.z) * (CONFIG.maxZ - radius);
          vB.z = -vB.z * CONFIG.wallBounce;
        }

        vA.toArray(posData, base);
        vB.toArray(velData, base);
      }
    }

    // ── RESIZE ────────────────────────────────────────────────────────────
    function resize() {
      var wrap = canvas.parentElement;
      var W = (wrap && wrap.offsetWidth  > 0) ? wrap.offsetWidth  : window.innerWidth;
      var H = (wrap && wrap.offsetHeight > 0) ? wrap.offsetHeight : 600;
      renderer.setSize(W, H, false);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      camera.aspect = W / H;
      // cameraMaxAspect = 1.5 (matches React source)
      if (camera.aspect > 1.5) {
        var t = Math.tan(THREE.MathUtils.degToRad(50 / 2)) / (camera.aspect / 1.5);
        camera.fov = 2 * THREE.MathUtils.radToDeg(Math.atan(t));
      } else {
        camera.fov = 50;
      }
      camera.updateProjectionMatrix();
      var fovR = camera.fov * Math.PI / 180;
      var wH   = 2 * Math.tan(fovR / 2) * camera.position.z;
      CONFIG.maxX = (wH * camera.aspect) / 2;
      CONFIG.maxY = wH / 2;
    }
    resize();
    window.addEventListener('resize', function () {
      clearTimeout(window._bprt);
      window._bprt = setTimeout(resize, 100);
    }, { passive: true });

    // ── RENDER LOOP ───────────────────────────────────────────────────────
    var dummy = new THREE.Object3D();
    var clock  = new THREE.Clock();
    var rafId  = null;

    function tick() {
      rafId = requestAnimationFrame(tick);
      var delta = clock.getDelta();
      updatePhysics(delta);

      for (var idx = 0; idx < CONFIG.count; idx++) {
        dummy.position.fromArray(posData, idx * 3);
        // Hide sphere 0 when followCursor is off (it's the cursor-tracking ball)
        dummy.scale.setScalar(idx === 0 && !CONFIG.followCursor ? 0 : sizeData[idx]);
        dummy.updateMatrix();
        mesh.setMatrixAt(idx, dummy.matrix);
        if (idx === 0) ptLight.position.copy(dummy.position);
      }
      mesh.instanceMatrix.needsUpdate = true;
      renderer.render(scene, camera);
    }

    function stopLoop() {
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
        rafId = null;
        clock.stop();
      }
    }

    function startLoop() {
      if (rafId !== null) return; // already running
      clock.start();
      tick();
    }

    // Pause when scrolled out of view
    new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { startLoop(); }
      else { stopLoop(); }
    }, { threshold: 0 }).observe(canvas);

    // Pause when tab is hidden
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stopLoop(); } else { startLoop(); }
    });

    startLoop();
  }
})();
