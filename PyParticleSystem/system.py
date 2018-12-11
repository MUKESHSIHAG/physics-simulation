import pygame
import PyParticles.environment as Env
def main():
	pygame.display.set_caption("PyParticles")
	(width, height) = (400, 400)
	screen = pygame.display.set_mode((width, height))

	env = Env.Environment((width, height))
	env.add_particles(10)

	selected = None
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				selected = env.find_particle(pygame.mouse.get_pos())
			elif event.type == pygame.MOUSEBUTTONUP:
				selected = None

		if selected:
			selected.mouse_move(pygame.mouse.get_pos())

		screen.fill(env.color)
		for p in env.particles:
			env.update()
			pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.size, p.thickness)

		pygame.display.flip()

if __name__ == '__main__':
	main()
