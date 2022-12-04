#include"testgraph.h"


int main(int argc, char** argv) {

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE);
	glutInitWindowSize(1000, 300);
	glutCreateWindow("CO2, TEM, HUM");

	glutDisplayFunc(redraw);
	glutKeyboardFunc(key);
	glutReshapeFunc(reshape);
	glutIdleFunc(idle);

	thread thread1(getData);
	glLineWidth(1.0);

	glutMainLoop();
	return 0;
}