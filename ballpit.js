// NordicWebFlow Ballpit — faithful vanilla JS port of React Bits source
// Uses Three.js r155 + RoomEnvironment + subsurface scattering shader
(function () {
  var canvas = document.getElementById('ballpit-canvas');
  if (!canvas) return;

  function load(src, cb) {
    var s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    s.onerror = function () { console.error('Failed:', src); };
    document.head.appendChild(s);
  }

  // Load Three r155
  load('https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.min.js', function () {
    start();
  });

  function start() {
    var THREE = window.THREE;

    // ── CONFIG (your settings) ──────────────────────────────────────────
    var CONFIG = {
      count:        50,
      colors:       ['#e84400', '#ff4f00', '#ffffff', '#ffffff'],
      ambientColor: 0xffffff,
      ambientIntensity: 1,
      lightIntensity:   200,
      materialParams: {
        metalness:          0.5,
        roughness:          0.5,
        clearcoat:          1,
        clearcoatRoughness: 0.15
      },
      minSize:      0.5,
      maxSize:      1.0,
      size0:        1.0,
      gravity:      0,        // float freely
      friction:     0.9975,
      wallBounce:   0.95,
      maxVelocity:  0.15,
      maxX:         5,
      maxY:         5,
      maxZ:         2,
      controlSphere0: false,
      followCursor:   false   // cursor ball OFF
    };

    // ── RENDERER ─────────────────────────────────────────────────────────
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

    // ── ENV MAP — programmatic neutral studio environment ─────────────────
    // Build a simple HDR-like environment using a CubeRenderTarget
    var pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileEquirectangularShader();

    // Create a neutral grey scene for environment baking
    var envScene = new THREE.Scene();
    // Top light (warm white)
    var eL1 = new THREE.DirectionalLight(0xfff5e0, 3); eL1.position.set(2, 4, 3); envScene.add(eL1);
    // Fill light (cool)
    var eL2 = new THREE.DirectionalLight(0xe0f0ff, 1.5); eL2.position.set(-3, -1, 2); envScene.add(eL2);
    // Back light
    var eL3 = new THREE.DirectionalLight(0xffffff, 2); eL3.position.set(0, -4, -3); envScene.add(eL3);
    // Ambient
    envScene.add(new THREE.AmbientLight(0xffffff, 0.5));

    var envTex = pmrem.fromScene(envScene, 0.04).texture;
    scene.environment = envTex;
    pmrem.dispose();

    // ── CUSTOM MATERIAL with subsurface scattering (port of class Y) ─────
    function createMaterial(envMap, params) {
      var mat = new THREE.MeshPhysicalMaterial(Object.assign({ envMap: envMap }, params));
      mat.envMapRotation = new THREE.Euler(-Math.PI / 2, 0, 0);

      // Subsurface scattering uniforms
      var uniforms = {
        thicknessDistortion: { value: 0.1 },
        thicknessAmbient:    { value: 0 },
        thicknessAttenuation:{ value: 0.1 },
        thicknessPower:      { value: 2 },
        thicknessScale:      { value: 10 }
      };
      mat.defines = mat.defines || {};
      mat.defines.USE_UV = '';

      mat.onBeforeCompile = function (shader) {
        Object.assign(shader.uniforms, uniforms);

        // Inject uniform declarations
        shader.fragmentShader =
          '\nuniform float thicknessPower;\nuniform float thicknessScale;\nuniform float thicknessDistortion;\nuniform float thicknessAmbient;\nuniform float thicknessAttenuation;\n' +
          shader.fragmentShader;

        // Inject scattering function before main()
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

        // Inject scattering call after RE_Direct
        var patched = THREE.ShaderChunk.lights_fragment_begin.replaceAll(
          'RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );',
          'RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );\nRE_Direct_Scattering(directLight, vUv, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, reflectedLight);'
        );
        shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_begin>', patched);
      };

      return mat;
    }

    // ── COLOR GRADIENT HELPER (port of inline function in setColors) ──────
    function makeGradient(hexColors) {
      var colors = hexColors.map(function (h) { return new THREE.Color(h); });
      return function (ratio) {
        var scaled = Math.max(0, Math.min(1, ratio)) * (colors.length - 1);
        var idx    = Math.floor(scaled);
        var start  = colors[idx];
        if (idx >= colors.length - 1) return start.clone();
        var alpha  = scaled - idx;
        var end    = colors[idx + 1];
        var out    = new THREE.Color();
        out.r = start.r + alpha * (end.r - start.r);
        out.g = start.g + alpha * (end.g - start.g);
        out.b = start.b + alpha * (end.b - start.b);
        return out;
      };
    }

    // ── INSTANCED MESH (port of class Z) ──────────────────────────────────
    var geo      = new THREE.SphereGeometry(1, 32, 32);
    var mat      = createMaterial(envTex, CONFIG.materialParams);
    var mesh     = new THREE.InstancedMesh(geo, mat, CONFIG.count);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    scene.add(mesh);

    // Lights
    var ambLight = new THREE.AmbientLight(CONFIG.ambientColor, CONFIG.ambientIntensity);
    mesh.add(ambLight);
    var ptLight  = new THREE.PointLight(0xe84400, CONFIG.lightIntensity);
    mesh.add(ptLight);

    // Set gradient colors
    var gradient = makeGradient(CONFIG.colors);
    for (var ci = 0; ci < CONFIG.count; ci++) {
      mesh.setColorAt(ci, gradient(ci / CONFIG.count));
      if (ci === 0) ptLight.color.copy(gradient(0));
    }
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;

    // ── PHYSICS (port of class W) ─────────────────────────────────────────
    var posData = new Float32Array(CONFIG.count * 3).fill(0);
    var velData = new Float32Array(CONFIG.count * 3).fill(0);
    var sizeData= new Float32Array(CONFIG.count).fill(1);
    var center  = new THREE.Vector3();

    // Init sphere 0 at center, rest random
    center.toArray(posData, 0);
    sizeData[0] = CONFIG.size0;
    for (var i = 1; i < CONFIG.count; i++) {
      posData[i*3]   = (Math.random()-0.5) * 2 * CONFIG.maxX;
      posData[i*3+1] = (Math.random()-0.5) * 2 * CONFIG.maxY;
      posData[i*3+2] = (Math.random()-0.5) * 2 * CONFIG.maxZ;
      sizeData[i]    = CONFIG.minSize + Math.random() * (CONFIG.maxSize - CONFIG.minSize);
    }

    // Give initial random velocities so balls move immediately
    for (var i = 0; i < CONFIG.count; i++) {
      var spd = 0.05 + Math.random() * 0.08;
      var ang = Math.random() * Math.PI * 2;
      velData[i*3]   = Math.cos(ang) * spd;
      velData[i*3+1] = Math.sin(ang) * spd;
      velData[i*3+2] = (Math.random()-0.5) * spd;
    }

    var F=new THREE.Vector3(),I=new THREE.Vector3(),O=new THREE.Vector3(),
        V=new THREE.Vector3(),B=new THREE.Vector3(),N=new THREE.Vector3(),
        _=new THREE.Vector3(),j=new THREE.Vector3(),H=new THREE.Vector3(),T=new THREE.Vector3();

    function updatePhysics(delta) {
      var r0 = CONFIG.controlSphere0 ? 1 : 0;

      if (CONFIG.controlSphere0) {
        F.fromArray(posData, 0);
        F.lerp(center, 0.1).toArray(posData, 0);
        V.set(0,0,0).toArray(velData, 0);
      }

      // Gravity + friction
      for (var idx = r0; idx < CONFIG.count; idx++) {
        var base = idx * 3;
        I.fromArray(posData, base);
        B.fromArray(velData, base);
        B.y -= delta * CONFIG.gravity * sizeData[idx];
        B.multiplyScalar(CONFIG.friction);
        B.clampLength(0, CONFIG.maxVelocity);
        I.add(B);
        I.toArray(posData, base);
        B.toArray(velData, base);
      }

      // Collisions
      for (var idx = r0; idx < CONFIG.count; idx++) {
        var base = idx * 3;
        I.fromArray(posData, base);
        B.fromArray(velData, base);
        var radius = sizeData[idx];

        for (var jdx = idx + 1; jdx < CONFIG.count; jdx++) {
          var otherBase = jdx * 3;
          O.fromArray(posData, otherBase);
          N.fromArray(velData, otherBase);
          var otherRadius = sizeData[jdx];
          _.copy(O).sub(I);
          var dist = _.length();
          var sumR = radius + otherRadius;
          if (dist < sumR) {
            var overlap = sumR - dist;
            j.copy(_).normalize().multiplyScalar(0.5 * overlap);
            H.copy(j).multiplyScalar(Math.max(B.length(), 1));
            T.copy(j).multiplyScalar(Math.max(N.length(), 1));
            I.sub(j); B.sub(H);
            I.toArray(posData, base); B.toArray(velData, base);
            O.add(j); N.add(T);
            O.toArray(posData, otherBase); N.toArray(velData, otherBase);
          }
        }

        // Cursor sphere collision
        if (CONFIG.controlSphere0) {
          _.copy(F).sub(I);
          var d0 = _.length(), sr0 = radius + sizeData[0];
          if (d0 < sr0) {
            var diff = sr0 - d0;
            j.copy(_.normalize()).multiplyScalar(diff);
            H.copy(j).multiplyScalar(Math.max(B.length(), 2));
            I.sub(j); B.sub(H);
          }
        }

        // Wall bounce — all axes (gravity=0)
        if (Math.abs(I.x) + radius > CONFIG.maxX) {
          I.x = Math.sign(I.x) * (CONFIG.maxX - radius);
          B.x = -B.x * CONFIG.wallBounce;
        }
        if (CONFIG.gravity === 0) {
          if (Math.abs(I.y) + radius > CONFIG.maxY) {
            I.y = Math.sign(I.y) * (CONFIG.maxY - radius);
            B.y = -B.y * CONFIG.wallBounce;
          }
        } else if (I.y - radius < -CONFIG.maxY) {
          I.y = -CONFIG.maxY + radius;
          B.y = -B.y * CONFIG.wallBounce;
        }
        var maxBound = Math.max(CONFIG.maxZ, CONFIG.maxSize);
        if (Math.abs(I.z) + radius > maxBound) {
          I.z = Math.sign(I.z) * (CONFIG.maxZ - radius);
          B.z = -B.z * CONFIG.wallBounce;
        }

        I.toArray(posData, base);
        B.toArray(velData, base);
      }
    }

    // ── CURSOR FOLLOW (port of S / onMove / onLeave) ──────────────────────
    var raycaster = new THREE.Raycaster();
    var nPos      = new THREE.Vector2();
    var camPlane  = new THREE.Plane();
    var hitPoint  = new THREE.Vector3();

    canvas.addEventListener('pointermove', function (e) {
      if (!CONFIG.followCursor) return;
      var rect = canvas.getBoundingClientRect();
      nPos.x = ((e.clientX - rect.left) / rect.width)  *  2 - 1;
      nPos.y = ((e.clientY - rect.top)  / rect.height) * -2 + 1;
      raycaster.setFromCamera(nPos, camera);
      camera.getWorldDirection(camPlane.normal);
      raycaster.ray.intersectPlane(camPlane, hitPoint);
      center.copy(hitPoint);
      CONFIG.controlSphere0 = true;
    }, { passive: true });

    canvas.addEventListener('pointerleave', function () {
      CONFIG.controlSphere0 = false;
    });

    // ── RESIZE (port of x.resize + onAfterResize) ─────────────────────────
    function resize() {
      var wrap = canvas.parentElement;
      var W = wrap ? wrap.offsetWidth  : window.innerWidth;
      var H = wrap ? wrap.offsetHeight : 600;
      renderer.setSize(W, H, false);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      canvas.style.width  = W + 'px';
      canvas.style.height = H + 'px';
      camera.aspect = W / H;
      // cameraMaxAspect = 1.5 (from source)
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
    var dummy  = new THREE.Object3D();
    var clock  = new THREE.Clock();
    var paused = false;

    function tick() {
      if (paused) return;
      requestAnimationFrame(tick);
      var delta = clock.getDelta();

      updatePhysics({ delta: delta });

      for (var idx = 0; idx < CONFIG.count; idx++) {
        dummy.position.fromArray(posData, idx * 3);
        // Hide sphere0 when followCursor=false
        if (idx === 0 && !CONFIG.followCursor) {
          dummy.scale.setScalar(0);
        } else {
          dummy.scale.setScalar(sizeData[idx]);
        }
        dummy.updateMatrix();
        mesh.setMatrixAt(idx, dummy.matrix);
        if (idx === 0) ptLight.position.copy(dummy.position);
      }
      mesh.instanceMatrix.needsUpdate = true;
      renderer.render(scene, camera);
    }

    // Pause when off-screen
    new IntersectionObserver(function (entries) {
      paused = !entries[0].isIntersecting;
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
