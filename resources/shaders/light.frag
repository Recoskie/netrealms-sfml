uniform sampler2D texture;
uniform vec3 light;
uniform vec4 lcolor;

void main() {
    float distance = sqrt(pow(gl_FragCoord.x - light.x, 2) + pow(gl_FragCoord.y - light.y, 2));

    if (floor(light.x) == floor(gl_FragCoord.x) && floor(light.y) == floor (gl_FragCoord.y))
        distance = 0.1;

    if (distance > light.z)
        distance = light.z;

    vec2 pos = gl_TexCoord[0].xy ;
    gl_FragColor = mix(texture2D(texture,pos), lcolor, 1.0-(distance/light.z));

}