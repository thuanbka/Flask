var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(60, 1, 1, 1000);
camera.position.set(-50, 12, 100).setLength(165);
var renderer = new THREE.WebGLRenderer({
  antialias: true
});
renderer.setClearColor(0x888586);
renderer.setPixelRatio(0.5);
var canvas = renderer.domElement;
document.body.appendChild(canvas);

var controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.update();

var light = new THREE.DirectionalLight(0xffffff, 0.5);
light.position.setScalar(100);
scene.add(light);
scene.add(new THREE.AmbientLight(0xffffff, 0.75));

var grid = new THREE.GridHelper(100, 6, 0xeeeeee, 0xeeeeee); 
// grid.position.set(0, -50, 0);
//scene.add(grid);

let xSize = 50;
let ySize = 50;
let zSize = 50;
let n = xSize * ySize * zSize;

let positions = [];
let speed = [];
let sign = [];

for (let i = 0; i < n; i++){
  positions.push(new THREE.Vector3(Math.random(), Math.random(), Math.random()).multiplyScalar(100));
  speed.push(Math.random() * 10 + 5);
}

let pointsGeometry = new THREE.BufferGeometry().setFromPoints(positions);
pointsGeometry.addAttribute("speed", new THREE.BufferAttribute(new Float32Array(speed), 1));
pointsGeometry.center();

let points = new THREE.Points(
  pointsGeometry,
  new THREE.ShaderMaterial({ 
    uniforms:{
      time:{
        value: 0
      },
      size: {
        value: 1.25
      },
      logo: {value: new THREE.TextureLoader().load( "https://cywarr.github.io/small-shop/threejslogo.png" ) }
    },
    vertexShader:`
      #define PI 3.1415926  

      uniform float time;
      uniform float size;
      uniform sampler2D logo;

      attribute float speed;

      varying vec3 vC;
      varying float vDiscard;
      `
      + sdf +
      `
      void main(){
        vec3 pos = position;
       
        float start = position.y - -50.;
        float way = speed * time;
        float totalWay = start + way;
        float modulo = mod(totalWay, 100.);
        pos.y = modulo - 50.;
        
        vec3 vPos = pos;

        vPos *= rotate(vec3(0, time, 0));
        
        // heart https://www.youtube.com/watch?v=aNR4n0i2ZlM
        vec3 h = vPos / 2.5;
        h.y = 4. + 1.2 * h.y - abs(h.x) * sqrt(max((20. - abs(h.x)) / 15., 0.));
        h.z = h.z * (2. - h.y / 15.);
        float r = 15. + 3. * pow(0.5 + 0.5 * sin(2. * PI * time + h.y / 25.), 4.);
        float heart = sdSphere(h, r);        

        bool boolDiscard = heart > 0.0 || heart < -2.;
        
        vec3 c = vec3(1., 0.75, 0.9); // colour of the heart
        if (heart > -0.125) c = vec3(1);

        vC = c;

        float logoPos = sin(time) * 47.5;
        if(position.z > logoPos - 2.5 && position.z < logoPos + 2.5){
          vec2 uv = (pos.xy - vec2(-50))/vec2(100);
          vC = vec3(1.) - texture2D( logo, uv ).xyz; // invert the color
          boolDiscard = boolDiscard && vC.r < 0.75;
          vC += c;
        }
        
        vDiscard = boolDiscard == true ? 1. : 0.;

        vec4 mvPosition = modelViewMatrix * vec4( pos, 1.0 );
        gl_PointSize = size * ( 300.0 / -mvPosition.z );
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      //uniform sampler2D texture;

      varying vec3 vC;
      varying float vDiscard;
     
      void main(){

        if ( vDiscard > 0.5 ) {discard;}
        if (length(gl_PointCoord - 0.5) > 0.5) {discard;}
        gl_FragColor = vec4( vC, 1.0);
        //gl_FragColor = gl_FragColor * texture2D( texture, gl_PointCoord );
      }
    `,
    /*blending: THREE.AdditiveBlending,
    depthTest: false,
    transparent: true*/
  })
);
scene.add(points);

// Box3Helper
var box3 = new THREE.Box3().setFromObject(points);
var box3Helper = new THREE.Box3Helper(box3, "rgb(100%, 92%, 95%)"/*0xeeeeee*/);
scene.add(box3Helper);

var obj = new THREE.Mesh(new THREE.IcosahedronBufferGeometry(10, 0), new THREE.MeshLambertMaterial({color: 0xeefeff}));
scene.add(obj);

var clock = new THREE.Clock();
var time = 0;

renderer.setAnimationLoop(()=>{
  if (resize(renderer)) {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
  }
  
  time += clock.getDelta();
  scene.rotation.y = time * 0.25;
  points.material.uniforms.time.value = time;
  obj.rotation.x = time * 0.1;
  obj.rotation.y = time * 0.314
  
  renderer.render(scene, camera);
});

function resize(renderer) {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const needResize = canvas.width !== width || canvas.height !== height;
  if (needResize) {
    renderer.setSize(width, height, false);
  }
  return needResize;
}



Resources