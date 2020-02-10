// created by florian berger (flockaroo) - 2019
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.

// single pass CFD - with some self consistency fixes

// drawing the liquid

// same fluid as in "Spilled" - https://www.shadertoy.com/view/MsGSRd
// ...but with self-consistent-ish velocity field
// the previous method was just defined implicitely by the rotations on multiple scales
// here the calculated velocity field is put back into the stored field

// use mouse to push fluid, press I to init

#define PI2 6.283185
#define RandTex     iChannel0
#define RandRes     vec2(textureSize(RandTex,0))
#define EnvTex      iChannel1
#define EnvRes      vec2(textureSize(EnvTex,0))
#define BufferTex   iChannel2
#define BufferRes   vec2(textureSize(BufferTex,0))
#define Res  (iResolution.xy)

vec2 scuv(vec2 uv) {
    float zoom=1.;
    #ifdef SHADEROO
    zowom=1.-iMouseData.z/1000.;
    #endif
    return (uv-.5)*1.2*zoom+.5;
}

vec2 uvSmooth(vec2 uv,vec2 res)
{
    // no interpolation
    //return uv;
    // sinus interpolation
    //return uv+.8*sin(uv*res*PI2)/(res*PI2);
    // iq's polynomial interpolation
    vec2 f = fract(uv*res);
    return (uv*res+.5-f+3.*f*f-2.0*f*f*f)/res;
}





vec4 myenv(vec3 pos, vec3 dir, float period)
{
    return texture(EnvTex,dir.xz)+.15;
}

vec4 getCol(vec2 uv) { return
    texture(BufferTex,scuv(uv));
}
float getVal(vec2 uv) { return length(getCol(uv).xyz); }

vec2 getGrad(vec2 uv,float delta)
{
    vec2 d=vec2(delta,0); return vec2( getVal(uv+d.xy)-getVal(uv-d.xy),
                                       getVal(uv+d.yx)-getVal(uv-d.yx) )/delta;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	vec2 uv = fragCoord.xy / iResolution.xy;
	fragColor = texture(RandTex, uv);
	return;
    //vec2 UV = gl_FragCoord.xy / iResolution.xy;
	//fragColor=texture(iChannel0, fragCoord/100);
	//fragColor=texture(iChannel1, fragCoord/1000);
	//fragColor=texture(iChannel2, fragCoord/100);
	//fragColor=vec4(1,0.0,0.5,1);
	//return;

    // calculate normal from gradient (the faster the higher)
    vec3 n = vec3(-getGrad(uv,1.4/iResolution.x)*.02,1.);
    n=normalize(n);

    /*vec3 light = normalize(vec3(-1,1,2));
    float diff=clamp(dot(n,light),0.,1.0);
    float spec=clamp(dot(reflect(light,n),vec3(0,0,-1)),0.0,1.0); spec=exp2(log2(spec)*24.0)*2.5;*/

    // evironmental reflection
    vec2 sc=(fragCoord-Res*.5)/Res.x;
    vec3 dir=normalize(vec3(sc,-1.));
    vec3 R=reflect(dir,n);
    vec3 refl=myenv(vec3(0),R.xzy,1.).xyz;

    // slightly add velocityfield to color - gives it a bit of a 'bismuty' look
    vec4 col=getCol(uv)+.5;
    col=mix(vec4(1),col,.35);
    col.xyz*=.95+-.05*n; // slightly add some normals to color

	//fragColor.xyz = col.xyz*(.5+.5*diff)+.1*refl;
	fragColor.xyz = col.xyz*refl;
	fragColor.w=1.;
	//fragColor=texture(iChannel2, fragCoord/10);
}

