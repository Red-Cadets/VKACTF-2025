function runPolymerShaderAnimation() {
    let container = document.getElementById("polymer3d-container");
    container.style.display = "block";
    const canvas = document.getElementById("polymer-shader-canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const gl = canvas.getContext("webgl");

    const vert = `
        attribute vec2 position;
        void main() {
            gl_Position = vec4(position, 0.0, 1.0);
        }
    `;

    const frag = `
        precision highp float;
        uniform float u_time;
        uniform vec2 u_res;
        #define PI 3.1415926

        float circle(vec2 uv, vec2 c, float r) {
            float d = length(uv - c);
            return smoothstep(r, r-0.013, d);
        }

        float glow(vec2 uv, vec2 c, float r, float intensity) {
            float d = length(uv - c);
            return intensity/(d*d*50.0+0.22);
        }

        void main() {
            vec2 uv = gl_FragCoord.xy / u_res.xy;
            uv.y = 1.0-uv.y;
            vec2 c = vec2(0.5, 0.13);

            // Основной поток-полимер
            float y = clamp((uv.y - c.y) / (1.0 - c.y - 0.01), 0.0, 1.0);
            float x = uv.x-0.5;
            float base = exp(-x*x*30.0) * y * 1.18;
            float tube = smoothstep(0.13,0.08,length(uv-c)) * smoothstep(c.y, 1.0, uv.y);

            // Glow вокруг
            float gl1 = glow(uv, c, 0.13, 0.17+0.07*sin(u_time*0.3));
            float gl2 = glow(uv, c, 0.28, 0.19+0.08*sin(u_time*0.11));
            float gl3 = glow(uv, c, 0.38, 0.11+0.09*sin(u_time*0.21));
            float glTot = gl1 + gl2 + gl3;

            // Частицы (спираль + движение вверх)
            float p = 0.0;
            for(int i=0; i<16; ++i){
                float fi = float(i)*PI/8.0 + u_time*0.3;
                vec2 cp = c + vec2(sin(fi), cos(fi)) * (0.09+0.04*sin(u_time*0.6+float(i)*0.4));
                cp.y += mod(u_time*0.09 + float(i)*0.1,0.59);
                p += 0.14 * exp(-dot(uv-cp, uv-cp)/0.0018);
            }

            // Основной поток — плотный столбец
            float poly = smoothstep(0.18,0.07,length(uv-c)) * smoothstep(c.y, 1.0, uv.y);

            // Эффект финального свечения
            float finalGlow = glow(uv, c, 0.12, smoothstep(0.94,1.0,y)*0.32);


            vec3 col = vec3(0.16,0.94,0.96) * (base*0.7 + glTot + p*0.7 + poly*0.14 + finalGlow*1.09);
            col += vec3(0.93,0.98,0.95)*finalGlow*0.13;

            // Доп. sci-fi вспышки на краю
            vec2 c_left  = vec2(0.0, 0.5);
            vec2 c_right = vec2(1.0, 0.5);
            float radius = 0.52;
            float sci_left  = smoothstep(radius, radius-0.17, length((uv - c_left) / vec2(0.54, 1.0)));
            float sci_right = smoothstep(radius, radius-0.17, length((uv - c_right) / vec2(0.54, 1.0)));
            float sci = (sci_left + sci_right) * 0.38;
            col += vec3(0.75, 0.93, 1.0) * sci;


            // Чисто, ярко, volumetric
            gl_FragColor = vec4(col, (base+poly+glTot+finalGlow+sci)*0.86);
        }
    `;

    function createShader(gl, type, src) {
        let shader = gl.createShader(type);
        gl.shaderSource(shader, src);
        gl.compileShader(shader);
        return shader;
    }
    const vs = createShader(gl, gl.VERTEX_SHADER, vert);
    const fs = createShader(gl, gl.FRAGMENT_SHADER, frag);

    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    gl.useProgram(prog);

    const verts = new Float32Array([
        -1, -1,   1, -1,  -1, 1,
        -1, 1,    1, -1,   1, 1
    ]);
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);

    const pos = gl.getAttribLocation(prog, 'position');
    gl.enableVertexAttribArray(pos);
    gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);

    const u_time = gl.getUniformLocation(prog, 'u_time');
    const u_res = gl.getUniformLocation(prog, 'u_res');

    let start = performance.now();

    function render() {
        let now = (performance.now() - start) * 0.001;
        gl.uniform1f(u_time, now);
        gl.uniform2f(u_res, canvas.width, canvas.height);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
    }
    render();

    setTimeout(()=>{
        container.style.display = "none";
        showFlagAfterPolymer();
    }, 8000);
}

function showFlagAfterPolymer() {
    fetch("/get_flag")
      .then(r => r.text())
      .then(flagText => {
        showFormPopup(flagText);
        window.__polymer_animation_ran__ = false;
      });
}
