/*
  1. Create WebGL Renderer.
  2. Create scene and lights.
  3. Create and add camera.
  4. Add spotlights.
  5. Add text geometry.
  6. Bind interactions.
  7. Request animation frame.
  8. Update scene on resize.
*/
let text_3D = "Welcome " + userName;
const { FontLoader, OrbitControls, TextGeometry } = THREE;
const container = document.querySelector('#container-text-three-js');

// 1. Create WebGL Renderer.

const renderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: true,
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x000000, 0);
container.appendChild(renderer.domElement);

// 2. Create scene and lights.

const scene = new THREE.Scene();
addSpotlight(-200, 100, 100);
addSpotlight(100, -200, 100);
addSpotlight(100, 100, -200);

// 3. Create and add camera.

const initialPosition = new THREE.Vector3(0, 0, 100);
const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000,
);
camera.position.copy(initialPosition);
scene.add(camera);

// 4. Add spotlights.

function addSpotlight(x, y, z) {
    const spotLight = new THREE.SpotLight(0xffffff);
    spotLight.position.set(x, y, z);
    spotLight.castShadow = true;
    scene.add(spotLight);
}

// 5. Add text geometry.
const texts = [];
const fontSize = container.clientWidth / 90;
addText(text_3D, fontSize, new THREE.Vector3(0, 25, -5));
function addText(text3D, fontSize, position) {
    const fontLoader = new FontLoader().load('https://threejs.org/examples/fonts/helvetiker_bold.typeface.json', (font) => {
        const words = text3D.split(' '); // Split the text into words
        let currentY = position.y;
        words.forEach((word) => {
            const textGeometry = new TextGeometry(word, {
                font,
                size: fontSize,
                height: 6,
                curveSegments: 12,
                bevelEnabled: true,
                bevelThickness: 0.5,
                bevelSize: 0.2,
                bevelSegments: 3,
            });
            textGeometry.center();
            const text = new THREE.Mesh(textGeometry, new THREE.MeshPhongMaterial({
                color: '#e2d2fc',
                emissive: '#00005f',
                specular: '#0000ff',
                shininess: 0,
            }));
            text.position.set(position.x, currentY, position.z);
            scene.add(text);
            texts.push(text)
            // Increase the Y position for the next word
            currentY -= fontSize * 1.5; // Adjust the factor as needed for spacing
        });
    });
}

camera.aspect = window.innerWidth / window.innerHeight;
camera.updateProjectionMatrix();
renderer.setSize(window.innerWidth, window.innerHeight);

//6. Bind interactions.
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enableZoom = false;
// controls.minPolarAngle = Math.PI / 2;
// controls.maxPolarAngle = Math.PI / 2;

// 7. Request animation frame.
function animate() {
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}
animate();

// 8. Update scene on resize.
window.addEventListener('resize', () => {
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;
    camera.aspect = containerWidth / containerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(containerWidth, containerHeight);
    const fontSize = container.clientWidth / 90;
    for(const text of texts)
    {
        scene.remove(text);
    }
    texts.length = 0
    addText(text_3D, fontSize, new THREE.Vector3(0, 25, -5));
});
