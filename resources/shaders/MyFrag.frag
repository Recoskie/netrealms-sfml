uniform vec2 LightPos; // The light's position
uniform float luminosity; //the lights luminosity
uniform float darkness; //how dark the rest of the shader is
uniform vec2 TextureSize; // we use this to invert the Y axis
 
void main() {
 
vec2 PixPos = gl_FragCoord.xy;
 
PixPos.y = TextureSize.y-PixPos.y; // Fixing the reversed Y position
 
//PixPos.y and PixPos.x are the exact pixel position in texture
 
vec2 Difference=LightPos - PixPos; // subtract point x and y into the light x and y giving the X difference and Y difference
 
float Distance = length(Difference); // Calculate math.sqrt( X*X + Y*Y )
 
//the above does the distance formula
 
float shade = (Distance / luminosity);
 
if(shade > darkness) shade = darkness ;
 
vec4 color = vec4( 0, 0, 0, shade );

gl_FragColor=color; // We give our pixel its final colour.
} 
