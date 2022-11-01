#version 330 core
out vec4 FragColor;

in vec3 TexCoords;

uniform samplerCube box;

void main()
{    
    FragColor = texture(box, TexCoords);
}